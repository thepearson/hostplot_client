import subprocess
import time
import psutil
import platform
import multiprocessing
import socket
from Metric import Metric

'''
 Retrieves some basic host details
'''
class HostDetails(Metric):
    
  def runnable(self):
    update = int(time.time()) - self.data['ttl']
    if self.data['last_run'] < update:
      return True
    else:
      return False
  
  def run(self):
    uname = platform.uname()
    data = {
            'system': uname[0],
            'node': uname[1],
            'release': uname[2],
            'version': uname[3],
            'machine': uname[4],
            'processor': uname[5],
            'cpu_count': psutil.NUM_CPUS, 
            'memory': int(psutil.virtual_memory().total)}
    return data
      
  def validate(self, result):
    messages = []
    if len(messages) is 0:
      return True
    else:
      return messages