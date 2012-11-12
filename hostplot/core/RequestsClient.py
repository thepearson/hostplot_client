try:
  import requests
except:
  raise Exception("Requests library not installed")

try:
  import json
except:
  try:
    import simplejson as json
  except:
    raise Exception("No JSON parser")

class RequestsClient:

  def __init__(self, host, protocol = 'http', root_path = '', debug = False):
    self.debug = debug
    self.host = host
    self.root_path = root_path
    self.protocol = protocol

  def getRequest(self, action, args=None):
    """ GET request to a server """
    response = requests.get(self.protocol + '://' + self.host + self.root_path + action, params=args)
    if str(response.status_code)[:1] == '2':
      try:
        return response.json
      except:
        try:
          import json
        except:
          import simplejson as json
        return json.loads(response.content)
    else:
      return None

  def postRequest(self, action, args=None):
    """ GET request to a server """
    response = requests.post(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    if str(response.status_code)[:1] == '2':
      return True
    else:
      return None

  def putRequest(self, action, args=None):
    """ GET request to a server """
    response = requests.put(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    if str(response.status_code)[:1] == '2':
      return True
    else:
      return None

  def deleteRequest(self, action, args=None):
    """ GET request to a server """
    response = requests.delete(self.protocol + '://' + self.host + self.root_path + action)
    if str(response.status_code)[:1] == '2':
      return True
    else:
      return None

  def decodeResponse(self, response):
    return response
