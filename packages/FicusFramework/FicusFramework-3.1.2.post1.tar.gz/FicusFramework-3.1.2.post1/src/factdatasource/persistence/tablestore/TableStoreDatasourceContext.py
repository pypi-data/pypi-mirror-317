import json
import logging
import math

import tablestore
from munch import Munch
from tablestore import TableMeta, TableOptions, CapacityUnit, ReservedThroughput, Row, OTSClientError, OTSServiceError, \
    SingleColumnCondition, CompositeColumnCondition, ComparatorType, RowExistenceExpectation, \
    BatchWriteRowRequest, TableInBatchWriteRowItem, PutRowItem, UpdateRowItem, BatchGetRowRequest, \
    TableInBatchGetRowItem

from api.model.Condition import ConditionGroup, Condition, LogicalOperator, CalculationOperator
from api.model.MetaModelField import MetaModelField, DataTypeEnum
from api.model.Page import Page
from factdatasource.dao.tablestore.TableStoreDatasourceDao import TableStoreDatasourceDao
from factdatasource.persistence.AbstractFactDatasourceContext import AbstractFactDatasourceContext
from factdatasource.dao.FactDatasource import customer_dao_context_holder as costomer_context
from factdatasource.execptions import NotSupportedFDException, FDExecuteException

log = logging.getLogger('Ficus')


def get_column_type(data_type: DataTypeEnum) -> str:
    """
        根据ficus DataTypeEnum字段数据类型返回对应tablestore预定义字段（非主键字段）数据类型
    """
    if data_type == DataTypeEnum.STRING:
        return 'STRING'
    elif data_type == DataTypeEnum.INTEGER:
        return 'INTEGER'
    elif data_type == DataTypeEnum.BOOLEAN:
        return 'BOOLEAN'
    elif data_type == DataTypeEnum.DOUBLE:
        return 'DOUBLE'
    elif data_type == DataTypeEnum.BLOB:
        return 'BINARY'
    else:
        raise FDExecuteException(f'tablestore预设字段暂不支持' + data_type.name + '数据类型')


def get_primary_type(data_type: DataTypeEnum) -> str:
    """
        根据ficus DataTypeEnum字段数据类型返回对应tablestore主键字段数据类型
    """
    if data_type == DataTypeEnum.STRING:
        return 'STRING'
    elif data_type == DataTypeEnum.INTEGER:
        return 'INTEGER'
    elif data_type == DataTypeEnum.BLOB:
        return 'BINARY'
    else:
        raise FDExecuteException(f'tablestore主键暂不支持' + data_type.name + '数据类型')


def check_condition(table_meta: TableMeta, condition_group: ConditionGroup):
    """
        对请求条件进行检查
    """
    schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
    defined_columns = [x[0] for x in table_meta.defined_columns]
    all_columns = []
    all_columns.extend(schema_of_primary_key)
    all_columns.extend(defined_columns)
    # 条件字段必须是数据表中字段，预设字段(非主键字段)的逻辑操作符只能是AND或者OR,同时所有的预设字段逻辑操作符必须一致
    logical_operator: LogicalOperator = None
    for index, condition in enumerate(condition_group.conditions):
        if isinstance(condition, Condition):
            column = condition.key
            if column not in all_columns:
                raise FDExecuteException(json.dumps(condition_group) + '中' + column + '条件字段中数据表中没有对应字段')
            elif column in defined_columns:
                if logical_operator is None:
                    logical_operator = condition.logical_operator
                elif logical_operator != condition.logical_operator:
                    raise FDExecuteException(json.dumps(condition_group) + '中所有非主键字段的逻辑操作符必须一致')
    key_condition_map = dict()
    for index, condition in enumerate(condition_group.conditions):
        if isinstance(condition, Condition):
            key_condition_map[condition.key] = condition
    # 条件中必须包含主键同时的计算条件必须是等于
    for primary_key in schema_of_primary_key:
        if key_condition_map[primary_key] is None:
            raise FDExecuteException(json.dumps(condition_group) + '中' + primary_key + '主键字段不存在')
        elif key_condition_map[primary_key].calculation_operator != CalculationOperator.EQUAL:
            raise FDExecuteException(
                json.dumps(condition_group) + '中' + primary_key + '主键主键字段的计算条件必须是 EQUAL')


def get_compare_operator(cal_op: CalculationOperator) -> ComparatorType:
    """
        根据ficus的CalculationOperator类型返回tablestore中对应的CompareOperator类型
    """
    if cal_op == CalculationOperator.EQUAL:
        return ComparatorType.EQUAL
    elif cal_op == CalculationOperator.NOTEQUAL:
        return ComparatorType.NOT_EQUAL
    elif cal_op == CalculationOperator.GT:
        return ComparatorType.GREATER_THAN
    elif cal_op == CalculationOperator.GTE:
        return ComparatorType.GREATER_EQUAL
    elif cal_op == CalculationOperator.LT:
        return ComparatorType.LESS_THAN
    elif cal_op == ComparatorType.GREATER_EQUAL:
        return ComparatorType.GREATER_EQUAL
    else:
        raise FDExecuteException(f'tablestore不支持' + cal_op.name + '操作')


def transform_map_to_condition_group_obj(condition_group_map) -> ConditionGroup:
    """
        将dict类型的条件转化成ConditionGroup对象
    """
    if not isinstance(condition_group_map, dict):
        raise FDExecuteException("查询条件格式错误")
    else:
        operator = LogicalOperator(condition_group_map['operator'])
        conditions = []
        if condition_group_map['conditions'] is not None and len(condition_group_map['conditions']) > 0:
            for index, condition_map in enumerate(condition_group_map['conditions']):
                condition = Condition(condition_map['logicalOperator'], condition_map['key'], condition_map['value'],
                                      condition_map['calculationOperator'])
                conditions.append(condition)
        condition_group = ConditionGroup(operator, conditions)
        return condition_group


def check_primary_key_value(table_meta: TableMeta, result_list: list) -> list:
    """
        检查插入或者修改数据是否设置主键对应的值，tablestore中主键值不能为空，预定义字段（非主键字段）可以为空
    """
    modify_result = []
    delete_result = []
    schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
    for result in result_list:
        # 将对象转成dict类型
        if not isinstance(result, dict):
            result = vars(result)
        for primary_key in schema_of_primary_key:
            if not (primary_key in result.keys()):
                message = "必填字段：" + primary_key + "未填!"
                modify_result.append(Munch({"success": False, "error": message, "content": result}))
                delete_result.append(result)
            elif result[primary_key] is None:  # ""字符串沒有去除
                message = "必填字段：" + primary_key + "未填!"
                modify_result.append(Munch({"success": False, "error": message, "content": result}))
                delete_result.append(result)
    # 清除缺失主键的result
    for result in delete_result:
        result_list.remove(result)
    return modify_result


def get_row_put_change(table_meta: TableMeta, result) -> Row:
    """
        构建tablestore 通过sdk方式插入数据的Row对象,主要是构建主键字段或非主键字段的字段名与值的元组
    """
    schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
    primary_key_list = []
    attribute_columns_list = []
    if not isinstance(result, dict):
        result = vars(result)
    for filed in result:
        primary_value = result[filed]
        if filed in schema_of_primary_key:
            primary_key_list.append((filed, primary_value))
        elif primary_value is not None:
            attribute_columns_list.append((filed, primary_value))
    return Row(primary_key_list, attribute_columns_list)


def get_row_update_change(table_meta: TableMeta, result) -> Row:
    """
        构建tablestore 通过sdk方式更新数据的Row对象,主要是构建主键字段或非主键字段的字段名与值的元组
    """
    schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
    primary_key_list = []
    attribute_columns_list = []
    if not isinstance(result, dict):
        result = vars(result)
    for filed in result:
        primary_value = result[filed]
        if filed in schema_of_primary_key:
            primary_key_list.append((filed, primary_value))
        elif primary_value is not None:
            attribute_columns_list.append((filed, primary_value))
    update_of_attribute_columns = dict()
    update_of_attribute_columns['PUT'] = attribute_columns_list
    return Row(primary_key_list, update_of_attribute_columns)


def handle_error_message(error_message: str, condition_type: str) -> str:
    if error_message.find("Condition check failed.") >= 0:
        if "insert" == condition_type:
            return "data row is exist"
        elif "update" == condition_type:
            "data row is not exist"
    return error_message


def _compute_and_partition_datas(data: list, partition_size: int) -> list:
    """
    计算,并尽量均分的分片 数据小于 partition_size 就不分片了
    :param data:
    :return: list<result_list>
    """
    if not data:
        return None

    if len(data) <= partition_size:
        return [data]
    # 共分多少片
    n = math.ceil(len(data) / partition_size)
    # 每片多少个
    num = math.ceil(len(data) / n)
    return [data[i:i + num] for i in range(0, len(data), num)]


def row_resul_to_list(source_name: str, table_result: list) -> list:
    """
        将collect_condition查询到的结果转化成list(dict) 形式数据
    """
    row_map_list = []
    for item in table_result:
        if item.is_ok:
            if item.row is not None:
                row_map = dict()
                for primary_key in item.row.primary_key:
                    row_map[primary_key[0]] = primary_key[1]
                for column in item.row.attribute_columns:
                    row_map[column[0]] = column[1]
                row_map_list.append(row_map)
        else:
            log.warning(f'事实库{source_name} collect_condition 操作结果集异常，异常信息：' + item.error_message)
    return row_map_list


class TableStoreDatasourceContext(AbstractFactDatasourceContext):

    @property
    def dao(self) -> TableStoreDatasourceDao:
        return TableStoreDatasourceDao.instance()

    def table_store_row_put_or_update(self, table_meta: TableMeta, result_list: list, condition_type: str) -> list:
        """
            tablestore 批量插入或者更新数据操作，insert时要求原来数据行不存在，update时要求原来数据行存在，insertOrUpdate没有要求
        """
        modify_result = []
        row_list = []
        for result in result_list:
            if "insert" == condition_type:
                row = get_row_put_change(table_meta, result)
                condition = tablestore.Condition(RowExistenceExpectation.EXPECT_NOT_EXIST)
                put_row = PutRowItem(row, condition)
                row_list.append(put_row)
            elif "update" == condition_type:
                row = get_row_update_change(table_meta, result)
                condition = tablestore.Condition(RowExistenceExpectation.EXPECT_EXIST)
                update_row = UpdateRowItem(row, condition)
                row_list.append(update_row)
            else:
                row = get_row_put_change(table_meta, result)
                condition = tablestore.Condition(RowExistenceExpectation.IGNORE)
                put_row = PutRowItem(row, condition)
                row_list.append(put_row)
        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(self.fd().get_target_with_schema(), row_list))
        try:
            costomer_context.set_source(self.fd().get_source_name())
            response = self.dao.client.batch_write_row(request)
            if "insert" == condition_type or "none" == condition_type:
                success, fail = response.get_put()
                for item in success:
                    modify_result.append(Munch({"success": True}))
                for item in fail:
                    modify_result.append(Munch(
                        {"success": False, "error": handle_error_message(item.error_message, condition_type),
                         "content": result}))
            else:
                success, fail = response.get_update()
                for item in success:
                    modify_result.append(Munch({"success": True}))
                for item in fail:
                    modify_result.append(Munch(
                        {"success": False, "error": handle_error_message(item.error_message, condition_type),
                         "content": result}))
            return modify_result
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            log.error(e.get_error_message())
            for result in result_list:
                modify_result.append(Munch({"success": False, "error": e.get_error_message(), "content": result}))
            return modify_result
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            log.error(e.get_error_message())
            for result in result_list:
                modify_result.append(Munch({"success": False, "error": e.get_error_message(), "content": result}))
            return modify_result
        finally:
            costomer_context.clear_source()

    def _single_thread_inserts(self, table: str, result_list: list) -> list:
        """
            tablestore 批量操作一次只能操作200条数据，所以需要通过inserts方法对数据进行分片，然后再批量插入
        """
        modify_result = []
        table_meta = self.check_table()
        check_primary_modify_result = check_primary_key_value(table_meta, result_list)
        modify_result.extend(check_primary_modify_result)
        if result_list is not None and len(result_list) > 0:
            inner_insert_modify_result = self.inner_insert(table_meta, result_list)
            modify_result.extend(inner_insert_modify_result)
        return modify_result

    def inner_insert(self, table_meta: TableMeta, result_list: list) -> list:
        return self.table_store_row_put_or_update(table_meta, result_list, "insert")

    def _single_thread_updates(self, table: str, result_list: list) -> list:
        """
            tablestore 批量操作一次只能操作200条数据，所以需要通过updates方法对数据进行分片，然后再批量更新
        """
        modify_result = []
        table_meta = self.check_table()
        check_primary_modify_result = check_primary_key_value(table_meta, result_list)
        modify_result.extend(check_primary_modify_result)
        if result_list is not None and len(result_list) > 0:
            inner_insert_modify_result = self.inner_update(table_meta, result_list)
            modify_result.extend(inner_insert_modify_result)
        return modify_result

    def inner_update(self, table_meta: TableMeta, result_list: list) -> list:
        return self.table_store_row_put_or_update(table_meta, result_list, "update")

    def _single_thread_inserts_or_updates(self, table: str, result_list: list) -> list:
        """
            tablestore 批量操作一次只能操作200条数据，所以需要通过inserts_or_updates方法对数据进行分片，然后再批量插入或者更新
        """
        modify_result = []
        table_meta = self.check_table()
        check_primary_modify_result = check_primary_key_value(table_meta, result_list)
        modify_result.extend(check_primary_modify_result)
        if result_list is not None and len(result_list) > 0:
            inner_insert_modify_result = self.inner_insert_or_update(table_meta, result_list)
            modify_result.extend(inner_insert_modify_result)
        return modify_result

    def inner_insert_or_update(self, table_meta: TableMeta, result_list: list) -> list:
        return self.table_store_row_put_or_update(table_meta, result_list, "none")

    def size(self) -> int:
        """
        返回数据总长度
        :return: 数据条数:long
        """
        raise NotSupportedFDException('tablestore不支持该操作')

    def is_empty(self) -> bool:
        """
        返回是否存在数据
        :return: boolean
        """
        raise NotSupportedFDException('tablestore不支持该操作')

    def collect(self, size: int) -> list:
        """
        返回指定条数的数据
        :param size: 返回的条数
        :return: list
        """
        raise NotSupportedFDException('tablestore不支持该操作')

    def _single_thread_collect_conditions(self, condition_groups: list) -> list:
        table_meta = self.check_table()
        schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
        batch_primary_key_list = []
        for index, condition_group in enumerate(condition_groups):
            if not isinstance(condition_group, ConditionGroup):
                # 转换condition_group为ConditionGroup对象
                condition_group = transform_map_to_condition_group_obj(condition_group)
            check_condition(table_meta, condition_group)
            primary_key_list = []
            for index1, condition in enumerate(condition_group.conditions):
                if isinstance(condition, Condition):
                    key = condition.key
                    value = condition.value
                    if value is None:
                        raise FDExecuteException(json.dumps(condition_group) + '中' + key + '条件字段的值为空')
                    if key in schema_of_primary_key:
                        t = (key, value)
                        primary_key_list.append(t)
            batch_primary_key_list.append(primary_key_list)
        request = BatchGetRowRequest()
        table_name = self.fd().get_target_with_schema()
        request.add(TableInBatchGetRowItem(table_name, batch_primary_key_list, None, None, 1))
        return self.table_store_batch_get_row(request)

    def collect_conditions(self, size: int, condition_groups: list) -> list:
        """
        通过主键查询数据
        :param size: 查询中未使用
        :param condition_groups: 主键条件列表
        :return: list
        """
        if not condition_groups:
            return
        if not isinstance(condition_groups, list):
            condition_groups = [condition_groups]
        # 批量获取数据有100条限制
        partition = _compute_and_partition_datas(condition_groups, 100)

        if len(partition) == 1:
            return self._single_thread_collect_conditions(condition_groups)
        else:
            result = []
            # 目前没有使用多线程方式
            for data in partition:
                row_list = self._single_thread_collect_conditions(data)
                result.extend(row_list)
            return result

    def table_store_batch_get_row(self, request: BatchGetRowRequest) -> list:
        try:
            costomer_context.set_source(self.fd().get_source_name())
            result = self.dao.client.batch_get_row(request)
            table_result = result.get_result_by_table(self.fd().get_target_with_schema())
            return row_resul_to_list(self.fd().get_source_name(), table_result)
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            error = f'事实库{self.fd().get_source_name()}执行collect_conditions操作发生异常,可能是数据源连接断开,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            error = f'事实库{self.fd().get_source_name()}执行collect_conditions操作发生异常,异常信息：,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        finally:
            costomer_context.clear_source()

    def query(self, query: str, parameters: dict = None) -> Page:
        """
        使用查询语句查询数据
        :param query: 查询语句
        :param parameters: 查询参数
        :return: Page
        """
        raise NotSupportedFDException('tablestore不支持该操作')

    def delete_all(self):
        self.drop_target()
        self.create_target()

    def delete(self, query: str):
        table_meta = self.check_table()
        schema_of_primary_key = table_meta.schema_of_primary_key
        primary_key_map = json.loads(query)
        if not isinstance(primary_key_map, dict):
            raise FDExecuteException(query + '没有JSON化')
        primary_key_list = []
        for primary_key in schema_of_primary_key:
            if not primary_key_map[primary_key[0]]:
                raise FDExecuteException(f'必填字段：' + primary_key + '未填!')
            else:
                t = (primary_key[0], primary_key_map[primary_key[0]])
                primary_key_list.append(t)
        row = Row(primary_key_list)
        self.table_store_delete_row(self.fd().get_target_with_schema(), row, None)

    def delete_conditions(self, condition_groups: list):
        table_meta = self.check_table()
        schema_of_primary_key = [x[0] for x in table_meta.schema_of_primary_key]
        for index, condition_group in enumerate(condition_groups):
            if not isinstance(condition_group, ConditionGroup):
                # 转换condition_group为ConditionGroup对象
                condition_group = transform_map_to_condition_group_obj(condition_group)
            check_condition(table_meta, condition_group)
            primary_key_list = []
            table_store_condition: tablestore.Condition = tablestore.Condition(RowExistenceExpectation.IGNORE)
            composite_column_condition: CompositeColumnCondition = None
            for index1, condition in enumerate(condition_group.conditions):
                if isinstance(condition, Condition):
                    key = condition.key
                    value = condition.value
                    if value is None:
                        raise FDExecuteException(json.dumps(condition_group) + '中' + key + '条件字段的值为空')
                    if key in schema_of_primary_key:
                        t = (key, value)
                        primary_key_list.append(t)
                    else:
                        cal_op: CalculationOperator = condition.calculation_operator
                        single_column_condition = SingleColumnCondition(key, value, get_compare_operator(cal_op))
                        single_column_condition.set_pass_if_missing(True)
                        if len(condition_group.conditions) - len(schema_of_primary_key) > 1:
                            if composite_column_condition is None:
                                c_log_op = condition.logical_operator
                                log_op: tablestore.LogicalOperator = tablestore.LogicalOperator.AND if c_log_op == LogicalOperator.AND else tablestore.LogicalOperator.OR
                                composite_column_condition = CompositeColumnCondition(log_op)
                            composite_column_condition.add_sub_condition(single_column_condition)
                        else:
                            table_store_condition.set_column_condition(single_column_condition)
            row = Row(primary_key_list)
            if len(condition_group.conditions) - len(schema_of_primary_key) > 1:
                table_store_condition.set_column_condition(composite_column_condition)
            self.table_store_delete_row(self.fd().get_target_with_schema(), row, table_store_condition)

    def table_store_delete_row(self, table_name: str, row: Row, table_store_condition: tablestore.Condition):
        try:
            costomer_context.set_source(self.fd().get_source_name())
            self.dao.client.delete_row(table_name, row, table_store_condition)
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            error = f'事实库{self.fd().get_source_name()}执行delete操作发生异常,可能是数据源连接断开,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            if str(e.get_error_message()).find("Condition check failed.") >= 0:
                error = f'事实库{self.fd().get_source_name()}执行delete操作发生异常,异常信息：,{str(e.get_error_message())}'
                log.error(error)
                raise FDExecuteException(error)
        finally:
            costomer_context.clear_source()

    def drop_target(self):
        """
            删除数据表
        """
        try:
            costomer_context.set_source(self.fd().get_source_name())
            self.dao.client.delete_table(self.fd().get_target_with_schema())
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            error = f'事实库{self.fd().get_source_name()}执行deleteAll操作发生异常,可能是数据源连接断开,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            if str(e.get_error_message()).find("Requested table does not exist.") >= 0:
                error = f'事实库{self.fd().get_source_name()}执行deleteAll操作发生异常,异常信息：,{str(e.get_error_message())}'
                log.error(error)
                raise FDExecuteException(error)
        finally:
            costomer_context.clear_source()

    def create_target(self):
        """
            创建数据表
        """
        table_name = self.fd().get_target_with_schema()
        meta_model_fields = self.fd().model.fields
        if len(table_name.strip()) == 0 or meta_model_fields is None:
            #  没有表名或者没得字段,无法后续操作
            raise FDExecuteException(f'事实库{self.fd().get_source_name()}没有定义表名或者没有定义表字段')
        schema_of_primary_key = []
        defined_columns = []
        for field in meta_model_fields:
            if isinstance(field, MetaModelField):
                field_name = field.fieldName
                data_type = DataTypeEnum(field.dataType)
                is_primary_key = field.primaryKey
                if is_primary_key:
                    t = (field_name, get_primary_type(data_type))
                    schema_of_primary_key.append(t)
                else:
                    t = (field_name, get_column_type(data_type))
                    defined_columns.append(t)
        size = len(schema_of_primary_key)
        if size < 1 or size > 4:
            raise FDExecuteException(f'tablestore 主键个数在1~4之间')
        table_meta = TableMeta(table_name, schema_of_primary_key, defined_columns)
        # 一些默认配置，如数据存活周期以及数据版本数
        table_options = TableOptions(-1, 1)
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        try:
            costomer_context.set_source(self.fd().get_source_name())
            self.dao.client.create_table(table_meta, table_options, reserved_throughput)
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            error = f'事实库{self.fd().get_source_name()}执行deleteAll操作发生异常,可能是数据源连接断开,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            if str(e.get_error_message()).find("Requested table already exists.") >= 0:
                error = f'事实库{self.fd().get_source_name()}执行deleteAll操作发生异常,异常信息：,{str(e.get_error_message())}'
                log.error(error)
                raise FDExecuteException(error)
        finally:
            costomer_context.clear_source()

    def check_table(self) -> TableMeta:
        try:
            table_name = self.fd().get_target_with_schema()
            costomer_context.set_source(self.fd().get_source_name())
            tables = self.dao.client.list_table()
            if table_name not in tables:
                self.create_target()
            costomer_context.set_source(self.fd().get_source_name())
            describe_table_response = self.dao.client.describe_table(table_name)
            return describe_table_response.table_meta
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            error = f'事实库{self.fd().get_source_name()}执行check_table操作发生异常,可能是数据源连接断开,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            error = f'事实库{self.fd().get_source_name()}执行check_table操作发生异常,异常信息：,{str(e.get_error_message())}'
            log.error(error)
            raise FDExecuteException(error)
        finally:
            costomer_context.clear_source()
