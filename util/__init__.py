from multiprocessing import Pool
from tqdm import tqdm

class ValueWindow():
  def __init__(self, window_size=100):
    self._window_size = window_size
    self._values = []

  def append(self, x):
    self._values = self._values[-(self._window_size - 1):] + [x]

  @property
  def sum(self):
    return sum(self._values)

  @property
  def count(self):
    return len(self._values)

  @property
  def average(self):
    return self.sum / max(1, self.count)

  def reset(self):
    self._values = []

def parallel_run(fn, items, desc="", parallel=True):
    results = []

    if parallel:
        with closing(Pool()) as pool:
            for out in tqdm(pool.imap_unordered(
                    fn, items), total=len(items), desc=desc):
                if out is not None:
                    results.append(out)
    else:
        for item in tqdm(items, total=len(items), desc=desc):
            out = fn(item)
            if out is not None:
                results.append(out)

    return results

def add_postfix(path, postfix):
    path_without_ext, ext = path.rsplit('.', 1)
    return "{}.{}.{}".format(path_without_ext, postfix, ext)
