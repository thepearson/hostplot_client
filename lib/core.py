import urllib
import urllib2
import ConfigParser

class JsonClient():
    
    def __init__(self, host, root_path = '/', port = 80):
        self.host = host
        self.root_path = root_path
        self.port = port
        
    def getRequest(self, action, args=None):
        if args is not None:
            encoded_args = urllib.urlencode(args)
            return urllib2.urlopen(self.host + ':' + self.port + self.root_path + action + '?' + encoded_args).read()
        else:
            return urllib2.urlopen(self.host + ':' + self.port + self.root_path + action).read()
        
    def postRequest(self, action, args=None):
        if args is not None:
            encoded_args = urllib.urlencode(args)
            return urllib2.urlopen(self.host + ':' + self.port + self.root_path + action, encoded_args).read()
        else:
            return urllib2.urlopen(self.host + ':' + self.port + self.root_path + action).read()

class Core():

    def __init__(self, config):
        self.config = config
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(self.config)
        
    def saveConfig(self):
        #parser.set('main', 'key', key)
        print 'Writing new config'
        f = open(self.config, 'w')
        self.parser.write(f)
        f.close()
        
    def initialise(self, key):
        uuid = self.confirmServerKey(key)
        print 'Initializing new uuid for server [' + uuid +']'
        self.parser.add_section('main')
        self.parser.set('main', 'uuid', uuid)
        self.saveConfig()
    
    def run(self):
        print 'Getting check configs'
        print 'Running'
        print 'Sending data and/or errors'
        
    def update(self):
        print 'Checking for plugin updates'
        
        print 'Checking for config changes'
        # config = self.getServerConfig()
        
        print 'Updating local config' 
        
    def confirmServerKey(self, key):
        # TODO: Confirm with rest api that this server is real
        return 'e7d97b22-c9b7-11e1-9a78-639ef6174f7d'
    
    def getServerConfig(self):
        uuid = self.parser.get('main', 'uuid')
        # TODO get check info
        # return {'module': 'AvgLoad'}
    
    
    