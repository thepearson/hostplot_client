import os
from Metric import Metric

'''
 Library to get a systems average load
'''
class LoadAvg(Metric):

  def requirements(self):
    messages = []
    if hasattr(os, 'getloadavg') and callable(getattr(os, 'getloadavg')):
      return True;
    else:
      messages.append('getloadavg() method not found in package os')
      return messages

  def run(self):
    load = os.getloadavg()
    data = {'one': load[0], 'five': load[1], 'fifteen': load[2]}
    return data

  def validate(self, result):
    messages = []
    if len(result) is not 3:
      messages.append('Data length was not expected, expected 3, got ' + str(len(result)))

    if float(result["one"]) < 0.0 or float(result["one"]) > 9999:
      messages.append('The value of 1 minute load average appears wrong')
    
    if float(result["five"]) < 0.0 or float(result["five"]) > 9999:
      messages.append('The value of 5 minute load average appears wrong')
    
    if float(result["fifteen"]) < 0.0 or float(result["fifteen"]) > 9999:
      messages.append('The value of 15 minute load average appears wrong')
    
    if len(messages) is 0:
      return True
    else:
      return messages
