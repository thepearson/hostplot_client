import optparse
import sys, os
from core import Config
from core import Client
from core.Runner import Runner

DEFAULT_APP_NAME="hostplot"
DEFAULT_METRIC_NAME="metrics"
DEFAULT_CONFIG_FILE="/etc/" + DEFAULT_APP_NAME + ".conf"
DEFAULT_LIBRARY_PATH="/usr/local/lib/" + DEFAULT_APP_NAME
DEFAULT_API_PROTOCOL='http'
DEFAULT_API_SERVER="api.thepearson.co"
#DEFAULT_API_PORT='80'
DEFAULT_API_PATH=''
SERVER_INIT_PATH='/host/activate'

###
def main(config):
  print 'Running'
  # check config for metrics to run
  #   get metrics from server
  #   update config

  metrics = [{'key': 1, 'class': 'HostDetails', 'data': {'last_run': 1345245683, 'ttl': 3600}}, {'key': 2, 'class': 'LoadAvg', 'data': None}, {'key': 3, 'class': 'DiskFree', 'data': {'path': '/'}}]
  
  r = Runner(config, metrics)
  response = r.run()
  print response

    
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
  json = client.getRequest(SERVER_INIT_PATH + '/' + code)
    
  obj = client.decodeResponse(json)
  if obj['status'] is 0:
    print 'Success'
    host_uuid = obj['result']['uuid']
    config.add('uuid', host_uuid)
  else:
    print 'Failed: ' + obj['message']
    exit()
    
  print 'Host is now active, please set up the following cron job:\n\n\n'
  print '*\t*\t*\t*\t*\tpython ' +  os.getcwd() + '/' + DEFAULT_APP_NAME + ' -c ' + config_file
  config.save()
  exit()

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
      print "Updating code not implemented yet"
    else:
      main(opts.config)
  exit()