import ConfigParser
from compiler.pycodegen import EXCEPT

class Config():
  def __init__(self, file):
    self.file = file
    self.load()

  def load(self):
    self.parser = ConfigParser.SafeConfigParser()
    self.parser.read(self.file)

  def add(self, variable, value, section = 'main'):
    if self.parser.has_section(section) == False:
      self.parser.add_section(section)
    self.parser.set(section, variable, value)

  def save(self):
    f = open(self.file, 'w')
    self.parser.write(f)
    f.close()
    
  def get(self, variable, section = 'main'):
    try:
      return self.parser.get(section, variable)
    except:
      return None;