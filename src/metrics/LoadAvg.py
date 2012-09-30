import os
from Metric import Metric

'''
 Library to get a systems average load
'''
class LoadAvg(Metric):

  def requirements(self):
    if hasattr(os, 'getloadavg') and callable(getattr(os, 'getloadavg')):
      return True;
    else:
      self.messages.append('getloadavg() method not found in package os')
      return False

  def run(self):
    load = os.getloadavg()
    self.data = {'one': load[0], 'five': load[1], 'fifteen': load[2]}

  def validate(self):
    if len(self.data) is not 3:
      self.messages.append('Data length was not expected, expected 3, got ' + str(len(self.data)))

    if float(self.data["one"]) < 0.0 or float(self.data["one"]) > 9999:
      self.messages.append('The value of 1 minute load average appears wrong')
    
    if float(self.data["five"]) < 0.0 or float(self.data["five"]) > 9999:
      self.messages.append('The value of 5 minute load average appears wrong')
    
    if float(self.data["fifteen"]) < 0.0 or float(self.data["fifteen"]) > 9999:
      self.messages.append('The value of 15 minute load average appears wrong')
    
    if len(self.messages) is 0:
      return True
    else:
      return False
