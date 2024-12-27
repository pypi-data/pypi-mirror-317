from api.model.FactDatasource import FactDatasourceTypeEnum
from factdatasource.dao.FactDatasource import Datasource
from factdatasource.dao.MultipleDatasourceHolder import get_multiple_datesource
from libs.utils import Singleton
from tablestore import OTSClient


class TableStoreDatasourceDao(Singleton):

    @property
    def datasource(self) -> Datasource:
        data_source = get_multiple_datesource(FactDatasourceTypeEnum.TABLESTORE)
        return data_source

    @property
    def client(self) -> OTSClient:
        return self.datasource.get_client()
