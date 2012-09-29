import os
from Metric import Metric
try:
  import psutil
  has_psutil = True
except ImportError:
  import subprocess
  has_psutil = False

'''
 Library to get a systems average load
'''
class Memory(Metric):

  def requirements(self):
    """ Check that the psutil library exists """
    return True

  def run(self):
    """ import psutil and get bith vmem and swap info to return """
    if has_psutil is True:
      self.data = self.get_data_with_psutil()
    else:
      self.data = self.get_data_no_psutil()

  def get_data_no_psutil(self):
    """ Method for getting memory data without using psutil """
    free = subprocess.Popen(["free", "-b"], stdout=subprocess.PIPE)
    output = free.communicate()[0].split("\n")[1:]
    return {'ptotal': int(output[0].split()[1]), 'pused': int(output[0].split()[2]), 'stotal': int(output[2].split()[1]), 'sused': int(output[2].split()[2]), 'buffers': int(output[0].split()[5]), 'cached': int(output[0].split()[6])}

  def get_data_with_psutil(self):
    """ returns memory data using psutil """
    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {'ptotal': int(virt.total), 'pused': int(virt.used), 'stotal': int(swap.total), 'sused': int(swap.used), 'buffers': int(virt.buffers), 'cached': int(virt.cached)}

  def validate(self):
    """ TODO: Validate the data """
    return True
