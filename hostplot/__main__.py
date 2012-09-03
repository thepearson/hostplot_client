import sys
import os
import time
import platform
import optparse
from core import Config
from core import Client
from core.Runner import Runner

APP_VERSION = 0.1
DEFAULT_APP_NAME="hostplot"
DEFAULT_METRIC_NAME="metrics"
DEFAULT_CONFIG_FILE="/etc/hostplot/" + DEFAULT_APP_NAME + ".conf"
DEFAULT_LIBRARY_PATH="/usr/local/lib/" + DEFAULT_APP_NAME
DEFAULT_API_PROTOCOL='http'
DEFAULT_API_SERVER="hostplot.api.local"
#DEFAULT_API_PORT='80'
DEFAULT_API_PATH=''
SERVER_INIT_PATH='/host'

###
def main(config_file):
  config = Config.Config(config_file) 
  # check config for metrics to run
  #   get metrics from server
  #   update config
  metrics = [{'key': 'LoadAvg', 'data': None}]
  r = Runner(metrics)
  data = {"metrics": r.run(), "uuid": config.get('uuid')}
  client = Client.Client(protocol = config.get('protocol', 'api'), host = config.get('host', 'api'))
  client.postRequest(action=config.get('metric_path', 'api'), args=data)

    
def initialize(code):
  print "Initializing " + code

  while True:
    sys.stdout.write('Config file path?: [' + DEFAULT_CONFIG_FILE + '] ')
    config_file = raw_input().lower()
    if str(config_file).strip() == '':
      config_file = DEFAULT_CONFIG_FILE
      break
    else:
      try:
        # see if it's writable
        update = open(config_file, 'w')
        update.close()
      except:
        print 'Error creating config file! Check permissions.'
        exit()
      break

  # open config file and add api defaults
  config = Config.Config(config_file)
  config.add('protocol', DEFAULT_API_PROTOCOL, 'api')
  config.add('host', DEFAULT_API_SERVER, 'api')
  config.add('path', DEFAULT_API_PATH, 'api')
  config.add('code', code)
  
  print 'Initializing host with code "' + code +'"'
  client = Client.Client(protocol = DEFAULT_API_PROTOCOL, host = DEFAULT_API_SERVER)
  # 'system': uname[0],
  # 'node': uname[1],
  json = client.getRequest(SERVER_INIT_PATH + '/' + code + '/activate')  
  obj = client.decodeResponse(json)
  
  if obj['status'] is 0:
    print 'Success'
    host_uuid = obj['result']['uuid']
    config.add('uuid', host_uuid)
    updateHostInfo(obj['result'])
  else:
    print 'Failed: ' + obj['message']
    exit()
    
  print 'Host is now active, please set up the following cron job:\n\n\n'
  print '*\t*\t*\t*\t*\tpython ' +  os.getcwd() + '/' + DEFAULT_APP_NAME + ' -c ' + config_file
  config.save()
  exit()
  
  
def update(config_file):
  config = Config.Config(config_file)
  uuid = config.get('uuid')
  client = Client.Client(protocol = DEFAULT_API_PROTOCOL, host = DEFAULT_API_SERVER)
  json = client.getRequest(SERVER_INIT_PATH + '/' + uuid)  
  obj = client.decodeResponse(json)
  updateHostInfo(obj['result'])
  
  
def updateHostInfo(model):
  model['client_version'] = APP_VERSION
  model['hostname'] = platform.node()
  model['platform'] = platform.system()
  client = Client.Client(protocol = DEFAULT_API_PROTOCOL, host = DEFAULT_API_SERVER, debug = True)
  json = client.putRequest(SERVER_INIT_PATH + '/' + str(model['id']), model)
  obj = client.decodeResponse(json)
  print obj
  return
  

if __name__ == "__main__":
  # parse cmd line arguments
  parser = optparse.OptionParser()
  parser.add_option('-i', '--init', help='Install and initialise host', dest='init')
  parser.add_option('-c', '--config', help='Config file to use', dest='config')
  parser.add_option('-u', '--update', action="store_true",  dest='update', help='Check for updates')
  parser.add_option('-d', '--dry-run', action="store_true", dest='dry', help='Dry run (no communication with server)')
  (opts, args) = parser.parse_args()
  
  if opts.init is not None:
    initialize(opts.init)
  else:
    if opts.update is True:
      if opts.config is not None:
        update(opts.config)
      else:
        update(DEFAULT_CONFIG_FILE)
    else:
      if opts.config is not None:
        main(opts.config)
      else:
        main(DEFAULT_CONFIG_FILE)
      
  exit()