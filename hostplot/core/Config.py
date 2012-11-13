import ConfigParser

class Config:
  """
  Wrapper around ConfigParser
  complicates things slightly but I wanted to abstract this
  out as this may change at a later date
  """

  def __init__(self, file):

    # set the file name
    self.file = file

    # lets check that the file exists and that it is writable, or
    # if it doesn't exist we can write to the location specified.
    if self.exists() is False:
      if self.is_writable() is False:
        raise Exception("Config file location doesn't exist and is not writable")
    else:
      if self.is_writable() is False:
        raise Exception("Config file exists but is not writable")

    # load the file
    self.load()

  def exists(self):
    """
    Ensures that the config file exists
    """
    try:
      fp = open(self.file, 'r')
      fp.close()
      return True
    except:
      return False

  def is_writable(self):
    """
    Ensures that the config file is writeable
    """
    try:
      fp = open(self.file, 'a')
      fp.close()
      return True
    except:
      return False

  def load(self):
    """
    Load the config file
    """
    try:
      self.parser = ConfigParser.SafeConfigParser()
      self.parser.read(self.file)
    except:
      raise

  def add(self, variable, value, section = 'main'):
    """
    adds a variable and value to a section, creates
    the section if it doesn't exists
    """

    # we must define a veriable
    if variable.strip() == '':
      raise Exception("A variable name must be defined")

    # if a bad section is defined default to 'main'
    if section.strip() == '':
      section = 'main'

    # if the section doesn't exist then create it
    if self.parser.has_section(section) == False:
      self.parser.add_section(section)

    # now add the variable
    try:
      self.parser.set(section, variable, value)
      return True
    except:
      raise

  def save(self):
    """
    Writes the config to the file
    """
    try:
      f = open(self.file, 'w')
      self.parser.write(f)
      f.close()
      return True
    except IOError:
      raise
    except:
      raise

  def getint(self, variable, section = 'main'):
    """
    Wrapper around parser.getint()
    """
    try:
      return self.parser.getint(section, variable)
    except:
      return None

  def get(self, variable, section = 'main'):
    """
    Wrapper around parser.get()
    """
    try:
      return self.parser.get(section, variable)
    except:
      return None

  def getSection(self, section):
    """
    returns all items and values given a section
    """
    try:
      return self.parser.items(section)
    except:
      return None
