try:
  from hostplot.core.RequestsClient import RequestsClient as Client
except:
  from hostplot.core.Client import Client

class Api:
  def __init__(self, config):
    self.config = config
    self.client = Client(protocol = self.config.get('protocol', 'api'), host = self.config.get('host', 'api'), debug=True)


class HostApi(Api):

  def getHostInfo(self, uuid):
    """ gets the host info from the server """
    return self.client.getRequest(self.config.get('host_path', 'api') + '/' + uuid)

  def updateHostInfo(self, host_model):
    """ updates host info at the server """
    return self.client.putRequest(self.config.get('host_path', 'api') + '/' + str(host_model['id']), host_model)

  def activateHost(self, host_id):
    """ activate a host """
    return self.client.getRequest(self.config.get('host_path', 'api') + '/' + host_id + '/activate')

  def getHostConfig(self):
    """ returns the latest host config from the server """
    return self.client.getRequest(self.config.get('host_path', 'api') + '/' + self.config.get('uuid') + '/config')

  def saveHostMetrics(self, data):
    """ saves metrics to the api """
    return self.client.postRequest(action = self.config.get('metric_path', 'api'), args=data)

