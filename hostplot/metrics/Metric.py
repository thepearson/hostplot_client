'''
Base class for all metrics
'''
class Metric:

  """ any messages to be aware of """
  messages = []


  """ data from metric """
  data = None

  '''
  Apply any data if required
  '''
  def __init__(self, data = None):
    self.data = data

  '''
  helper function to see if we should run this check
  '''
  def runnable(self):
    return True


  '''
  run any set up for this check
  '''
  def pre(self):
    return True

  '''
  Check system requirements
  Should return True if requirements pass
  of a List of messages of any errors
  '''
  def requirements(self):
    return True

  '''
  Run the script and return the data to be serialized
  Data should be ready to pass right into the Json handler
  '''
  def run(self):
    return True

  '''
  Supplied funciton used to validate the output from the script
  Should return True if data passes validation or a list of errors
  if data fails validation
  '''
  def validate(self):
    return True

  '''
  Run any post functions, clean ups etc. this is run
  regardless of the success of failure of the
  requirements, run or validate function
  '''
  def post(self):
    return True
