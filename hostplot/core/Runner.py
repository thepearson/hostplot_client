import time
from metrics.Metric import Metric
from metrics.HostDetails import HostDetails
from metrics.LoadAvg import LoadAvg
from metrics.DiskFree import DiskFree

class Runner():
  '''
  Runner to run things
  '''
  def __init__(self, metrics):
    #self.config = config
    self.metrics = metrics
    
  def run(self):
    response = {}
    for m in self.metrics:
      c = m['key']
      if c is 'HostDetails':
        data = {'ttl': 3600, 'last_run': 0}
        if m['data'] is not None:
          data = m['data']
        metric = HostDetails(data)
      elif c is 'LoadAvg':
        if m['data'] is not None:
          data = m['data']
        else:
          data = None
        metric = LoadAvg(data)
      elif c is 'DiskFree':
        data = {'path': '/'}
        if m['data'] is not None:
          data = m['data']
        metric = DiskFree(data)
      if metric.runnable() is True:
        metric.pre()
        if metric.requirements() is True:
          data = metric.run()
          if metric.validate(data) is True:
            response[c] = data
          else:
            print 'Data validation failed'
        else:
          print 'System requirements failed'
        metric.post()
    return {str(int(time.time())): response}
