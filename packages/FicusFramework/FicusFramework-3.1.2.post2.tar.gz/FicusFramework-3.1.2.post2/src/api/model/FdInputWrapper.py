from api.exceptions import IllegalArgumentException
from factdatasource import FactDatasourceProxyServiceV2


class FdInputWrapper:
    """
    fd输入的一个包装
    """
    _site = None
    _project_code = None
    _fact_datasource_code = None
    _join_fd_codes = set()
    _join_fd_targets = set()

    def fd_code(self):
        return self._fact_datasource_code

    def __init__(self, site: str, project_code: str, fd_code):
        self._fact_datasource_code = fd_code
        self._site = site
        self._project_code = project_code
        self._join_fd_codes.add(fd_code)

    def join(self, other_fd_input):
        """
        合并两个fd的查询
        :param other_fd_input:
        :return:
        """
        # 1.check 两个fd的 链接是不是同一个,只能是同一个的才能链接
        this_fact_datasource = FactDatasourceProxyServiceV2.fd_client_proxy().fd(self._site, self._project_code, self._fact_datasource_code)
        other_fact_datasource = FactDatasourceProxyServiceV2.fd_client_proxy().fd(self._site,self._project_code, other_fd_input.fd_code())

        if this_fact_datasource is None or other_fact_datasource is None:
            raise IllegalArgumentException(
                f"无法联合两个FD({self._fact_datasource_code},{other_fd_input.fd_code()}),无法查询到FD数据")

        if this_fact_datasource.type != other_fact_datasource.type:
            raise IllegalArgumentException(
                f"无法联合两个FD({self._fact_datasource_code},{other_fd_input.fd_code()}),两个FD的类型不相同")

        if this_fact_datasource.connection != other_fact_datasource.connection:
            raise IllegalArgumentException(
                f"无法联合两个FD({self._fact_datasource_code},{other_fd_input.fd_code()}),两个FD的连接不相同")

        self._join_fd_codes.add(other_fd_input.fd_code())
        self._join_fd_targets.add(self.get_target_with_schema(other_fact_datasource.get("schema"),other_fact_datasource.target))
        return self

    def query(self, query, parameters={}):
        """
        对fd进行查询, 已被废弃,请使用 query_data
        :param query: 查询语句
        :param parameters: 上下文参数
        :return: Munch对象数据
        """
        # TODO 这个地方需要对query进行校验.验证他涉及的表是不是都是fd里面的

        if self._fact_datasource_code not in self._join_fd_codes:
            raise IllegalArgumentException(f"来源FD不存在:{self._fact_datasource_code()}")

        if len(self._join_fd_codes)>0:
            parameters = parameters if parameters is not None else {}
            parameters["__joinFdCodes__"] = list(self._join_fd_codes)
            parameters["__joinFdTargets__"] = list(self._join_fd_targets) if len(self._join_fd_targets) > 0 else list()

        return FactDatasourceProxyServiceV2.fd_client_proxy().query(self._site, self._project_code, self._fact_datasource_code, query, parameters)

    def query_data(self, query, parameters={}):
        """
        对fd进行查询与上面query方法功能相同，解决其远程调用query参数过长导致查询失败问题
        :param query: 查询语句
        :param parameters: 上下文参数
        :return: Munch对象数据
        """
        # TODO 这个地方需要对query进行校验.验证他涉及的表是不是都是fd里面的

        if self._fact_datasource_code not in self._join_fd_codes:
            raise IllegalArgumentException(f"来源FD不存在:{self._fact_datasource_code()}")

        if len(self._join_fd_codes)>0:
            parameters = parameters if parameters is not None else {}
            parameters["__joinFdCodes__"] = list(self._join_fd_codes)
            parameters["__joinFdTargets__"] = list(self._join_fd_targets) if len(self._join_fd_targets) > 0 else list()

        return FactDatasourceProxyServiceV2.fd_client_proxy().query_data(self._site,self._project_code,self._fact_datasource_code, query, parameters)

    def info(self):
        """
        获取fd的信息
        :return:
        """
        return FactDatasourceProxyServiceV2.fd_client_proxy().fd(self._site,self._project_code,self._fact_datasource_code)

    def get_target_with_schema(self,schema:str,target:str) -> str:
        if  schema is None or len(schema)==0:
            return target
        else:
            return f"{schema}.{target}"
