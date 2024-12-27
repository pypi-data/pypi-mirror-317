class FactDatasourceQueryParameter(object):
    """
       封装FactDatasourceProxyServiceV2.query中query和parameter两个参数
    """
    def __init__(self, query, parameters):
        self.query = query
        self.parameters = parameters

    def keys(self):
        return ('query','parameters')

    def __getitem__(self, item):
        return getattr(self, item)
