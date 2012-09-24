import json
import time
from core.Api import *
from core.Config import Config

'''
This is a wrapper around the metrics
configuration, abstrcted out into
this class for now as we may want to change 
how all this is managed at a later date
'''
class Metrics():
  
  '''
  Takes a config object
  '''
  def __init__(self, config):
    self.config = config
    self.update()
    
  '''
  Check to see if we should update the metrics
  '''
  def update(self):
    last_updated = self.config.getint('metrics_last', 'config')
    ttl = self.config.getint('metrics_ttl', 'config')
    if last_updated + ttl < int(time.time()):
      
      config_api = ConfigApi(self.config) 
      new_config = json.loads(config_api.getLatestConfig())

      if new_config.has_key('metrics'):

        # remove existing metrics config
        self.config.parser.remove_section('metrics');
        self.config.save()
                
        for m,d in new_config['metrics'].items():
          self.config.add(m, json.dumps(d), 'metrics')

      self.config.add('metrics_last', str(int(time.time())), 'config')
      self.config.save()
      return True

    # up to date
    return True
    
  '''
  get the metrics to run and the associated data
  '''
  def get(self):
    metrics = []
    items = self.config.getSection('metrics');
    for i in items:
      item = {}
      item['key'] = i[0]
      item['data'] = i[1]
      metrics.append(item)
    return metrics
  
  
  '''
  Set the metrics that we are to run
  '''
  def set(self, metrics):
    return True;