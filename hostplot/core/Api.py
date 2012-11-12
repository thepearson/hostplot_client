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
    return self.client.getRequest(SERVER_HOST_PATH + '/' + self.config.get('uuid') + '/config')

class HostApi(Api):
  def getHostInfo(self, uuid):
    """ gets the host info from the server """
    return self.client.getRequest(SERVER_HOST_PATH + '/' + uuid)

  def updateHostInfo(self, host_model):
    """ updates host info at the server """
    return self.client.putRequest(SERVER_HOST_PATH + '/' + str(host_model['id']), host_model)

class InitApi(Api):
  def activateHost(self, host_id):
    """ activate a host """
    return self.client.getRequest(SERVER_HOST_PATH + '/' + host_id + '/activate')

class MetricsApi(Api):
  def saveHostMetrics(self, data):
    """ saves metrics to the api """
    return self.client.postRequest(action = self.config.get('metric_path', 'api'), args=data)
