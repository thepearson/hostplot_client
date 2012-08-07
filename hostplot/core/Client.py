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
    if args is not None:
      encoded_args = urllib.urlencode(args)
      return urllib2.urlopen(self.protocol + '://' + self.host + self.root_path + action, encoded_args).read()
    else:
      return urllib2.urlopen(self.protocol + '://' + self.host + self.root_path + action).read()
    
  def decodeResponse(self, response):
    return json.loads(response)