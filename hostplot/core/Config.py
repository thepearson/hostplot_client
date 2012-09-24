import ConfigParser
import json
from compiler.pycodegen import EXCEPT


'''
Wrapper around ConfigParser
complicates things slightly but I wanted to abstract this
out as this may change at a later date
'''
class Config():
  
  '''
  Construct, takes a file path
  '''
  def __init__(self, file):
    self.file = file
    self.load()

  '''
  Load the config file
  '''
  def load(self):
    self.parser = ConfigParser.SafeConfigParser()
    self.parser.read(self.file)

  '''
  adds a variable and value to a section, creates 
  the section if it doesn't exists
  '''
  def add(self, variable, value, section = 'main'):
    if self.parser.has_section(section) == False:
      self.parser.add_section(section)
    self.parser.set(section, variable, value)

  '''
  Writes the config to the file
  '''
  def save(self):
    f = open(self.file, 'w')
    self.parser.write(f)
    f.close()

  '''
  Wrapper around parser.getint()
  '''
  def getint(self, variable, section = 'main'):
    try:
      return self.parser.getint(section, variable)
    except:
      return None;
  
  '''
  Wrapper around parser.get()
  '''
  def get(self, variable, section = 'main'):
    try:
      return self.parser.get(section, variable)
    except:
      return None;
    
  '''
  returns all items and values given a section
  '''
  def getSection(self, section):
    try:
      return self.parser.items(section)
    except:
      return None;