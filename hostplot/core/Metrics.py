import time
from hostplot.core.Api import *
from hostplot.core.Config import Config

try:
  import json
except:
  import simplejson as json

class Metrics():
  """
  This is a wrapper around the metrics
  configuration, abstrcted out into
  this class for now as we may want to change
  how all this is managed at a later date
  """

  def __init__(self, config, dry=False):
    """
    Takes a config object
    """
    self.config = config
    if dry is False:
      self.update()

  def update(self):
    """
    Check to see if we should update the stored metric config
    """
    if self.update_required(self.config.getint('metrics_last', 'config'),
                            self.config.getint('metrics_ttl', 'config'),
                            int(time.time())):

      config_api = ConfigApi(self.config)
      new_config_json = config_api.getLatestConfig()

      if new_config_json is not None:
        new_config = new_config_json

        if new_config.has_key('metrics'):

          # remove existing metrics config
          self.config.parser.remove_section('metrics');
          self.config.save()

          for m,d in new_config['metrics'].items():
            if m.strip() != "":
              self.config.add(m, json.dumps(d), 'metrics')

      self.config.add('metrics_last', str(int(time.time())), 'config')
      self.config.save()
      return True

    # up to date
    return True


  def update_required(self, last_run, ttl, time_now = None):
    """
    Retruns bool if metric config needs updating, false otherwise
    """
    if last_run is None:
      return True

    if time_now is None:
      time_now = int(time.time())

    if (last_run + ttl) < time_now:
      return True

    return False


  def get(self):
    """
    get the metrics to run and the associated data
    """
    metrics = []
    items = self.config.getSection('metrics');
    for i in items:
      item = {}
      if i[0] is not None:
        item['key'] = i[0]
        try:
          item['data'] = json.loads(i[1])
        except ValueError:
          item['data'] = None

        metrics.append(item)
    return metrics

  def set(self, metrics):
    """
    Set the metrics that we are to run
    """
    return True;
