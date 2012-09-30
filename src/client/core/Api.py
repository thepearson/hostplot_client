from core.Client import Client

class Api():
  def __init__(self, config):
    self.config = config
    self.client = Client(protocol = self.config.get('protocol', 'api'), host = self.config.get('host', 'api'))


class ConfigApi(Api):
  def getLatestConfig(self):
    """ returns the latest host config from the server """
    uuid = self.config.get('uuid')
    return self.client.getRequest('/host/' + uuid + '/config')

class MetricsApi(Api):
  def saveHostMetrics(self, data):
    """ saves metrics to the api """
    return self.client.postRequest(action = self.config.get('metric_path', 'api'), args=data)
