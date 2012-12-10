import os
from Metric import Metric

class Disk(Metric):

  def requirements(self):
    """
    Ensure os.statvfs
    """
    if hasattr(os, 'statvfs') and callable(getattr(os, 'statvfs')):
      return True;
    else:
      self.messages.append('statvfs() method not found in package os')
      return False

  def pre(self):
    """
    Here we default the path to / if none is specified
    """
    if self.data is None:
      self.data = [{'path':'/'},{'path':'/root'}]

  def run(self):
    r = []
    for i in self.data:
      vol = os.statvfs(i['path'])
      d = {}
      d['path'] = i["path"]
      d['total'] = vol.f_bsize * vol.f_blocks
      d['used'] = d['total'] - d['free']
      r.append(d)
    self.data = r

  def validate(self):
    if self.data is None:
      self.messages.append('Data has not been set')

    if len(self.messages) is 0:
      return True
    else:
      return False
