import os
from Metric import Metric

'''
 Library to get a systems average load
'''
class Memory(Metric):

  def requirements(self):
    """ Check that the psutil library exists """
    try:
      import psutil
      return True
    except ImportError:
      self.messages.append('psutil not found, please ensure it is installed')

  def run(self):
    """ import psutil and get bith vmem and swap info to return """
    import psutil
    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()
    self.data = {'ptotal': int(virt.total), 'pused': int(virt.used), 'stotal': int(swap.total), 'sused': int(swap.used), 'buffers': int(virt.buffers), 'cached': int(virt.cached)}

  def validate(self):
    """ TODO: Validate the data """
    return True
