import unittest
import os
from hostplot.core.Cache import Cache

class CoreCacheTestCase(unittest.TestCase):

  def setUp(self):

    # set up some starting points
    unittest.TestCase.setUp(self)
    self.data = {'TestCacheData': 1}
    self.cache = Cache('/tmp/hostplot-testing-cache')

    # remove any test files left lying around
    try:
      os.unlink(self.cache.cache_file)
    except:
      True

  def test_hascache(self):
    """
    Test that the has_cache() methods are
    functioning correctly.
    """
    # file should be empty
    cache = self.cache.has_cache()
    self.assertFalse(cache, 'has_cache() should return False')

    # create a file
    file = open(self.cache.cache_file, 'w')
    file.write('')
    file.close()

    cache = self.cache.has_cache()
    self.assertTrue(cache, 'has_cache() should return True')

    os.unlink(self.cache.cache_file)



  def test_cachesave(self):
    """
    test that the cache_save() method is actually saving data to a file
    """
    cache = self.cache.has_cache()
    self.assertFalse(cache, 'Cache should not exist')

    # save cache
    self.cache.cache_save(self.data)

    # lets check the size
    size = os.path.getsize(self.cache.cache_file)
    self.assertGreater(size, 0, 'cache_save() should save data to the file. File is 0 length')

    # clear the cache
    self.cache.cache_clear()



  def test_cacheget(self):
    # save cache
    self.cache.cache_save(self.data)

    cache = self.cache.has_cache()
    self.assertTrue(cache, 'has_cache() should return True')

    cache_data = self.cache.cache_get()
    self.assertDictEqual(cache_data, self.data, 'cache_get() should return the same data as saved into it')



if __name__ == '__main__':
  unittest.main()
