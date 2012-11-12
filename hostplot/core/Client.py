import urllib
import urllib2

class Client:
  def __init__(self, host, protocol = 'http', root_path = '', debug = False):
    self.debug = debug
    self.host = host
    self.root_path = root_path
    self.protocol = protocol

  def getRequest(self, action, args=None):
    """ GET request to a server """
    url = self.protocol + '://' + self.host + self.root_path + action
    if args is not None:
      encoded_args = urllib.urlencode(args)
      url = url + '?' + encoded_args

    if self.debug is True:
      print url

    try:
      response = urllib2.urlopen(url, timeout=5).read()
      try:
        import json
      except:
        import simplejson as json

      return json.loads(response)

    except urllib2.HTTPError:
      return None
    except urllib2.URLError:
      return None
    except:
      return None

  def postRequest(self, action, args=None):
    """ POST a request to a server """
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'POST'
    try:
      response = opener.open(request, timeout=5)
      response.read()
      return True
    except urllib2.HTTPError:
      return None
    except:
      return None

  def putRequest(self, action, args=None):
    """ PUT request to a server """
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'PUT'
    try:
      response = opener.open(request, timeout=5)
      response.read()
      return True
    except urllib2.HTTPError:
      return None

  def deleteRequest(self, action, args=None):
    """ DELETE request to a server """
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'DELETE'
    try:
      response = opener.open(request, timeout=5)
      response.read()
      return True
    except urllib2.HTTPError:
      return None

  def decodeResponse(self, response):
    """ json decodes a response """
    return response;
