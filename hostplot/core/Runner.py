import time

try:
  import json
except:
  import simplejson as json

from hostplot.metrics.Metric import Metric
from hostplot.metrics.LoadAvg import LoadAvg
from hostplot.metrics.Memory import Memory
from hostplot.metrics.Disk import Disk

class Runner:
  '''
  Runner to run things
  '''
  def __init__(self, metrics):
    #self.config = config
    self.metrics = metrics

  def get_metric(self, metric_string, data = None):
    if metric_string.lower() == 'loadavg':
      return LoadAvg(data)
    elif metric_string.lower() == 'memory':
      return Memory(data)
    elif metric_string.lower() == 'disk':
      return Disk(data)
    else:
      raise Exception("Unknown metric" + metric_string)

  def run(self):
    response = {}
    for m in self.metrics:
      c = m['key']
      if m['data'] is not None:
        data = json.loads(m['data'])
      else:
        data = None

      metric = self.get_metric(c, data)

      if metric.runnable() is True:
        metric.pre()

        if metric.requirements() is True:
          metric.run()
          if metric.validate() is not True:
            print 'Data validation failed'
        else:
          print 'System requirements failed'

        metric.post()

      if len(metric.messages) is not 0:
        response[c] = metric.messages
      else:
        response[c] = metric.data

    return {str(int(time.time())): response}
