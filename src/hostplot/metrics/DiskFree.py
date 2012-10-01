import subprocess
import psutil
from Metric import Metric

class DiskFree(Metric):
  
  def run(self):
    r = {}
    df = psutil.disk_usage(self.data['path'])
    r['total'] = df.total
    r['used'] = df.used
    r['free'] = df.free
    r['percent'] = df.percent
    return r