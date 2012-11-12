try:
  from hostplot.core.RequestsClient import RequestsClient as Client
except:
  from hostplot.core.Client import Client

SERVER_HOST_PATH='/host'

class Api():
  def __init__(self, config):
    self.config = config
    self.client = Client(protocol = self.config.get('protocol', 'api'), host = self.config.get('host', 'api'), debug=True)

class ConfigApi(Api):
  def getLatestConfig(self):
    """ returns the latest host config from the server """
    uuid = self.config.get('uuid')
    return self.client.getRequest(SERVER_HOST_PATH + '/' + uuid + '/config')

class InitApi(Api):
  def activateHost(self, host_id):
    return self.client.getRequest(SERVER_HOST_PATH + '/' + host_id + '/activate')

class MetricsApi(Api):
  def saveHostMetrics(self, data):
    """ saves metrics to the api """
    return self.client.postRequest(action = self.config.get('metric_path', 'api'), args=data)
