import unittest
import os
from hostplot.metrics.Metric import Metric

class MetricMetricTestCase(unittest.TestCase):

  def setUp(self):
    self.metric = Metric()

  def test_runnable(self):
    self.assertTrue(self.metric.runnable(), 'Metric interface runnable() should return True')

  def test_pre(self):
    self.assertTrue(self.metric.pre(), 'Metric interface pre() interface should return True')

  def test_requirements(self):
    self.assertTrue(self.metric.requirements(), 'Metric interface requirements() interface should return True')

  def test_run(self):
    self.assertTrue(self.metric.run(), 'Metric interface run() interface should return True')

  def test_validate(self):
    self.assertTrue(self.metric.validate(), 'Metric interface validate() interface should return True')

  def test_post(self):
    self.assertTrue(self.metric.post(), 'Metric interface posts() interface should return True')

if __name__ == '__main__':
  unittest.main()
