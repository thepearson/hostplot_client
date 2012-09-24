import urllib
import urllib2
import json

class Client():
  def __init__(self, host, protocol = 'http', root_path = '', debug = False):
    self.debug = debug
    self.host = host
    self.root_path = root_path
    self.protocol = protocol  
      
  def getRequest(self, action, args=None):
    url = self.protocol + '://' + self.host + self.root_path + action
    if args is not None:
      encoded_args = urllib.urlencode(args)
      url = url + '?' + encoded_args

    if self.debug is True:
      print url

    return urllib2.urlopen(url).read()
      
  def postRequest(self, action, args=None):
    # encoded_args = urllib.urlencode(args)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'POST'
    return opener.open(request).read()
    

  def putRequest(self, action, args=None):
    # encoded_args = urllib.urlencode(args)
    '''
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    request.add_header('Accept', 'application/json')
    request.add_header('Content-Type', 'application/json')
    f = urllib2.urlopen(request)
    response = f.read()
    f.close()
    return response
    '''
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action, data=json.dumps(args))
    request.add_header('Accept', 'application/json')
    request.get_method = lambda: 'PUT'
    return opener.open(request).read()

  def deleteRequest(self, action, args=None):
    # encoded_args = urllib.urlencode(args)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(self.protocol + '://' + self.host + self.root_path + action)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'DELETE'
    return opener.open(request).read()
    
  def decodeResponse(self, response):
    return json.loads(response)