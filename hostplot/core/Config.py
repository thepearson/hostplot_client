import ConfigParser

class Config:
  """
  Wrapper around ConfigParser
  complicates things slightly but I wanted to abstract this
  out as this may change at a later date
  """

  def __init__(self, file):
    self.file = file
    self.load()

  def exists(self):
    """
    Ensures that the config file exists and is writeable
    """
    try:
      open(self.file, 'rw')
      return True
    except:
      return False

  def load(self):
    """
    Load the config file
    """
    self.parser = ConfigParser.SafeConfigParser()
    try:
      self.parser.read(self.file)
    except:
      print "Config file doesn't exist"

  def add(self, variable, value, section = 'main'):
    """
    adds a variable and value to a section, creates
    the section if it doesn't exists
    """
    if section.strip() == '':
      return None

    if variable.strip() == '':
      return None

    if self.parser.has_section(section) == False:
      self.parser.add_section(section)

    self.parser.set(section, variable, value)
    return True

  def save(self):
    """
    Writes the config to the file
    """
    f = open(self.file, 'w')
    self.parser.write(f)
    f.close()
    return True

  def getint(self, variable, section = 'main'):
    """
    Wrapper around parser.getint()
    """
    try:
      return self.parser.getint(section, variable)
    except:
      return None;

  def get(self, variable, section = 'main'):
    """
    Wrapper around parser.get()
    """
    try:
      return self.parser.get(section, variable)
    except:
      return None;

  def getSection(self, section):
    """
    returns all items and values given a section
    """
    try:
      return self.parser.items(section)
    except:
      return None;
