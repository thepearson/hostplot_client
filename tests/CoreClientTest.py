import unittest
from hostplot.core.Client import Client

class CoreClientTestCase(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    self.client = Client('api.hostplot.me')

  def test_get(self):
    data = self.client.getRequest('/testing')
    self.assertEqual(data, '1', 'GET response equals 1')

  def test_put(self):
    data = self.client.putRequest('/testing/1', {'dummy':'data'})
    self.assertTrue(data, 'PUT response is True')

  def test_post(self):
    data = self.client.postRequest('/testing', {'dummy':'data'})
    self.assertTrue(data, 'POST response equals True')

  def test_delete(self):
    data = self.client.deleteRequest('/testing/1', {'dummy':'data'})
    self.assertTrue(data, 'DELETE response equals True')

if __name__ == '__main__':
  unittest.main()
