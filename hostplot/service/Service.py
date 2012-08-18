class Service():
  
  '''
    Init a service
  '''
  def __init__(self, config = None):
    self.config = config

  '''
    
  '''
  def shouldRun(self):
    return True