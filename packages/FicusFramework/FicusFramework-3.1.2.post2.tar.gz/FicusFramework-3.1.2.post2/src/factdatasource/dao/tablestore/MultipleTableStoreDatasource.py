from urllib.parse import quote_plus, unquote
from api.model.FactDatasource import FactDatasourceTypeEnum
from factdatasource.dao.FactDatasource import DatasourceListener, MultipleBaseDatasource, BaseDatasource
from factdatasource.execptions import DatasourceNotFoundException, FDExecuteException
from libs.utils import Singleton
from tablestore import OTSClient
from api.exceptions import IllegalArgumentException


class MultipleTableStoreDatasource(DatasourceListener, MultipleBaseDatasource, Singleton):

    def __init__(self):
        # source_name --> TableStoreDatasource
        self._target_dataSources = dict()

    def get_datasource_type(self):
        """
        获取数据源类型
        :return:
        """
        return FactDatasourceTypeEnum.TABLESTORE

    def add_datasource_type(self, source_name: str, url: str, credentials: str):
        """
        添加一个数据源
        :param source_name:
        :param url:
        :param credentials:
        :return:
        """
        if not source_name or not url:
            raise IllegalArgumentException(f'添加数据源参数错误:source_name、url都不能为空')

        for target in self._target_dataSources.values():
            if target.url == url and target.credentials == credentials:
                # url 和 credentials 都相同，说明是同一个数据库连接就不再重复创建数据源了
                target.add_source_name(source_name)
                self._target_dataSources[source_name] = target
                return

        # 开始创建数据源
        table_store_datasource = TableStoreDatasource(source_name, url, credentials)
        table_store_datasource.start()
        self._target_dataSources[source_name] = table_store_datasource

    def update_datasource_type(self, source_name: str, url: str, credentials: str):
        """
        修改一个数据源
        :param source_name:
        :param url:
        :param credentials:
        :return:
        """
        if not source_name or not url:
            raise IllegalArgumentException(f'修改数据源参数错误:source_name、url都不能为空')

        self.delete_datasource_type(source_name)
        self.add_datasource_type(source_name, url, credentials)

    def delete_datasource_type(self, source_name: str):
        """
        删除一个数据源
        :param source_name:
        :return:
        """
        target: TableStoreDatasource = self._target_dataSources.pop(source_name, None)
        if target:
            if target.only_one_source():
                target.close_client()
            else:
                target.remove_source_name(source_name)

    def get_data_source(self):
        """
        获取数据源的基本信息
        :return:
        """
        source_name = self.determine_current_lookup_key()
        if not source_name:
            raise FDExecuteException('未设置操作源,无法获取数据源信息。')

        if source_name in self._target_dataSources.keys():
            return self._target_dataSources[source_name]
        raise DatasourceNotFoundException('未发现数据源%s。' % source_name)

    def get_client(self):
        """
        获取数据库操作的client
        :return:
        """
        target: TableStoreDatasource = self.get_data_source()
        return target.get_client()

    def close_client(self):
        """
        关闭客户端，关闭连接
        :return:
        """
        target: TableStoreDatasource = self.get_data_source()
        return target.close_client()


class TableStoreDatasource(BaseDatasource):
    """
        credentials: access_key_id:access_key_secret@instance_name
    """

    def __init__(self, source_name, url, credentials):
        self.init(source_name, url, credentials)
        self.access_key_id = None
        self.access_key_secret = None
        self.instance_name = None
        self.client: OTSClient = None

    def _parse_url(self):
        """
        按照java版本进行解析
        :return:
        """
        if self.credentials:
            try:
                size = len(self.credentials)
                first = self.credentials.find(':')
                if first <= 0 or first >= (size - 1):
                    raise Exception()
                last = self.credentials.find('@')
                if last <= 0 or last >= (size - 1):
                    raise Exception()
                self.access_key_id = self.credentials[0:first]
                self.access_key_secret = self.credentials[first + 1:last]
                self.instance_name = self.credentials[last + 1:]
            except Exception:
                raise IllegalArgumentException(f'credentials格式不对，应该是：[accessKeyId:accessKeySecret@instanceName]的形式')

    def start(self):
        self._parse_url()
        self.client = OTSClient(self.url, self.access_key_id, self.access_key_secret, self.instance_name)

    def get_client(self):
        return self.client

    def close_client(self):
        """
        OTSClient 没有关闭连接的方法
        """
        self.client = None
