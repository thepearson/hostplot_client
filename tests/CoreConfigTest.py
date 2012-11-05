import unittest
import os
from hostplot.core.Config import Config

class CoreConfigTestCase(unittest.TestCase):

  def setUp(self):
    """
    Uses the file io library to manually create a .ini file
    which is used for the tests
    """

    self.file = '/tmp/testing.cfg'

    # set up some starting points
    unittest.TestCase.setUp(self)

    # create the config manually
    string = "[main]" + os.linesep
    string += "TestMainVar1 = TestMainVal1" + (os.linesep * 2)
    string += "[TestSection1]" + os.linesep
    string += "TestVar1 = TestVal1" + os.linesep
    string += "TestVar2 = TestVal2" + (os.linesep * 2)
    string += "[TestSection2]" + os.linesep
    string += "TestVar1 = TestVal1" + os.linesep
    string += "TestVar2 = TestVal2" + (os.linesep * 2)
    string += "[TestSection3]" + os.linesep
    string += "TestVar1 = " + os.linesep
    string += "TestVar2 = 1"

    try:
      fp = open(self.file, 'w')
      fp.write(string)
      fp.close()
    except:
      True

  def test_getsection_false(self):
    """
    Test if a fake section returns None
    """
    config = Config(self.file)
    non_existant = config.getSection('FakeSection')
    self.assertIsNone(non_existant, 'getSection() should return None for non-sections')

  def test_getsection_true(self):
    """
    Test if a known section is returned
    """
    config = Config(self.file)
    should_exist = config.getSection('TestSection3')
    self.assertIsNotNone(should_exist, 'getSection() should not return None for valid sections')

  def test_getvar_false(self):
    """
    Test if a fake variable returns None
    """
    config = Config(self.file)
    non_existant = config.get('blah', 'FakeSection')
    self.assertIsNone(non_existant, 'get() should return None for non-sections')

  def test_getvar_true(self):
    """
    Test if a known variable is returned
    """
    config = Config(self.file)
    main_var = config.get('TestMainVar1')
    self.assertEqual(main_var, 'TestMainVal1', 'get() should return TestMainVal1 for TestMainVar1')

  def test_getvar_int(self):
    """
    Test if a known int is returned as an int
    """
    config = Config(self.file)
    int_var = config.getint("TestVar2", 'TestSection3')
    self.assertEqual(int_var, 1, 'Variable should be an integer')

  def test_addvar_existing_string(self):
    """
    Test adding a variable, validating with get()
    """
    config = Config(self.file)
    var = 'TESTv1'
    config.add('NewVar1', var, 'TestSection2')
    check_var = config.get('NewVar1', 'TestSection2')
    self.assertEqual(check_var, var, 'Value added and value returned should be equal')

  def test_addvar_existing_int(self):
    """
    test adding a variable validating with getint()
    """
    config = Config(self.file)
    var = '1234'
    config.add('NewVar1', var, 'TestSection2')
    check_var = config.getint('NewVar1', 'TestSection2')
    self.assertEqual(check_var, 1234, 'Value added and value returned should be integer and equal')

  def test_save(self):
    """
    Test adding a variable checking with external method
    """
    config = Config(self.file)
    var = 'TESTv1'
    config.add('NewVar1', var, 'TestSection2')
    config.save()

    file = open(self.file, 'r')
    contents = file.read()
    file.close()
    val = None

    for line in contents.split(os.linesep):
      if line.startswith('NewVar1'.lower()):
        var, val = line.split(" = ")

    self.assertIsNotNone(val, 'Val should exist in the file')

  def test_no_variable(self):
    """
    We don't allow empty variables
    """
    config = Config(self.file)
    data = config.add('   ', 'value')
    self.assertIsNone(data, 'Add should return None for empty variables')

  def test_no_section(self):
    """
    We don't allow empty section names
    """
    config = Config(self.file)
    data = config.add('valid', 'value', '    ')
    self.assertIsNone(data, 'Add should return None for empty sections')

  def test_no_value(self):
    """
    We allow variables to have empty values, test this
    """
    config = Config(self.file)
    data = config.add('valid', '')
    self.assertTrue(data, 'Add should return True for empty values')

  def tearDown(self):
    unittest.TestCase.tearDown(self)
    # remove the temp file
    os.unlink(self.file)


if __name__ == '__main__':
  unittest.main()
