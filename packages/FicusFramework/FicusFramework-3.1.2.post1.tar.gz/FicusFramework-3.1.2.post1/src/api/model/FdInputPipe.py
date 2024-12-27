from api.model.FdInputWrapper import FdInputWrapper
from api.model.AlgorithmFdInputWrapper import AlgorithmFdInputWrapper
from factdatasource import FactDatasourceProxyServiceV2
from api.exceptions import IllegalArgumentException
from api.model.FactDatasource import FactDatasourceTypeEnum


class FdInputPipe:
    """
    输入包装
    """
    __source_fd_codes = None

    def __init__(self, site: str, project_code: str, source_fd_codes):
        self.__site = site
        self.__project_code = project_code
        self.__source_fd_codes = source_fd_codes

    def list_source_fd_codes(self):
        """
        列出所有与之关联的来源FD的code
        :return:
        """
        return self.__source_fd_codes

    def get_fd(self, fd_code, site: str = None, project_code: str = None):
        """
        返回一个Fd的输入代理对象
        :param site:
        :param project_code:
        :param fd_code:
        :return: FdInputWrapper对象
        """
        inner_site = site if site is not None else self.__site
        inner_project = project_code if project_code is not None else self.__project_code

        fd = FactDatasourceProxyServiceV2.fd_client_proxy().fd(inner_site, inner_project, fd_code)
        if fd is None:
            raise IllegalArgumentException(f"无法查询到FD:{fd_code}的数据")
        if fd.type == FactDatasourceTypeEnum.ALGORITHM:
            return AlgorithmFdInputWrapper(inner_site, inner_project, fd_code, None)
        else:
            return FdInputWrapper(inner_site, inner_project, fd_code)
