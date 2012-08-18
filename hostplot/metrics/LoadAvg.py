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
    data = {'1_min': load[0], '5_min': load[1], '15_min': load[2]}
    return data

  def validate(self, result):
    messages = []
    if len(result) is not 3:
      messages.append('Data length was not expected, expected 3, got ' + str(len(result)))

    if float(result["1_min"]) < 0.0 or float(result["1_min"]) > 9999:
      messages.append('The value of 1 minute load average appears wrong')
    
    if float(result["5_min"]) < 0.0 or float(result["5_min"]) > 9999:
      messages.append('The value of 5 minute load average appears wrong')
    
    if float(result["15_min"]) < 0.0 or float(result["15_min"]) > 9999:
      messages.append('The value of 15 minute load average appears wrong')
    
    if len(messages) is 0:
      return True
    else:
      return messages
