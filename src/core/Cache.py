import os
import pickle

class Cache():

  def __init__(self, cache_file):
    self.cache_file = cache_file

  def has_cache(self):
    try:
      open(self.cache_file)
      return True
    except:
      return False

  def cache_save(self, data):
    pickle.dump(data, open(self.cache_file, "wb"))

  def cache_get(self):
    data = pickle.load(open(self.cache_file))
    return data

  def cache_clear(self):
    return os.unlink(self.cache_file)
