import time
from metrics.Metric import Metric
from metrics.LoadAvg import LoadAvg
from metrics.Memory import Memory

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
      if m['data'] is not None:
        data = m['data']
      else:
        data = None

      if c.lower() == 'loadavg':
        metric = LoadAvg(data)
      elif c.lower() == 'memory':         
        metric = Memory(data)
      else:
        print 'unknown metric'

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
