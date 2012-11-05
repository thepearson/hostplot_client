import unittest
import os
from hostplot.core.Metrics import Metrics
from hostplot.core.Config import Config

class CoreMetricsTestCase(unittest.TestCase):

  def setUp(self):
    """
    Uses the file io library to manually create a .ini file
    which is used for the tests
    """
    # set up some starting points
    unittest.TestCase.setUp(self)

    # config file name
    self.file = '/tmp/testing.cfg'

    # create the config manually
    string = "[metrics]" + os.linesep
    string += "metric = {}" + os.linesep
    string += "metric_nodata = " + os.linesep

    try:
      fp = open(self.file, 'w')
      fp.write(string)
      fp.close()
    except:
      True


  def test_update_required_less(self):
    """
    Test that an update isn't required when time.time() < (ttl+last_run)
    """
    metrics = Metrics(config=Config(self.file), dry=True)
    no_update = metrics.update_required(100, 10, 100)
    self.assertFalse(no_update, 'Update required should return false for values less than last_run+TTL')

  def test_update_required_equal(self):
    """
    Test that an update isn't required when time.time() == (ttl+last_run)
    """
    metrics = Metrics(config=Config(self.file), dry=True)
    no_update = metrics.update_required(100, 10, 110)
    self.assertFalse(no_update, 'Update required should return False for values the same as last_run+TTL')

  def test_update_required_more(self):
    """
    Test that an update will be required when time.time() > (ttl+last_run)
    """
    metrics = Metrics(config=Config(self.file), dry=True)
    no_update = metrics.update_required(100, 10, 111)
    self.assertTrue(no_update, 'Update required should return true for values greater than last_run+TTL')

  def test_get_metrics(self):
    """
    Test that an update will be required when time.time() > (ttl+last_run)
    """
    metrics = Metrics(config=Config(self.file), dry=True)
    m = metrics.get()
    self.assertLessEqual(m, [{'data': {}, 'key': 'metric'}, {'data': None, 'key': 'metric_nodata'}], 'Metrics loaded from file should be equal')

if __name__ == '__main__':
  unittest.main()
