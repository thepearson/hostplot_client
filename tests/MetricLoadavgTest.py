import unittest
import os
from hostplot.metrics.LoadAvg import LoadAvg

class MetricLoadavgTestCase(unittest.TestCase):

  def test_runnable(self):
    metric = LoadAvg()
    self.assertTrue(metric.runnable(), 'Metric runnable() should return True')

  def test_pre(self):
    metric = LoadAvg()
    self.assertTrue(metric.pre(), 'Metric pre() interface should return True')

  def test_requirements(self):
    metric = LoadAvg()
    self.assertTrue(metric.requirements(), 'Metric requirements() interface should return True')

  def test_run(self):
    metric = LoadAvg()
    metric.run()
    self.assertIsNotNone(metric.data, 'Metric should populate data property with load data')

  def test_validate_valid(self):
    metric = LoadAvg()
    metric.data = {'fifteen': 0.0, 'five': '0.0', 'one': '0.0'}
    result = metric.validate()
    print result

    self.assertTrue(result, 'Metric validate() should return True on successful validation')

  def test_validate_invalid1(self):
    metric = LoadAvg()
    metric.data = None
    self.assertFalse(metric.validate(), 'Metric validate() should return False if data is None')

  def test_validate_invalid2(self):
    metric = LoadAvg()
    metric.data = {'fifteen': "asa", 'five': 0.0, 'one': 0.0}
    self.assertFalse(metric.validate(), 'Metric validate() should not allow alpha characters')

  def test_post(self):
    metric = LoadAvg()
    self.assertTrue(metric.post(), 'Metric posts() interface should return True')

if __name__ == '__main__':
  unittest.main()
