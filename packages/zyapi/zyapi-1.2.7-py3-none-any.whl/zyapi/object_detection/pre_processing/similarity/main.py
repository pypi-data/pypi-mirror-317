from ...utils.workspace import AttrDict
from .utils import phash, distance


class Similarity:
    def __init__(self):
        self.dev_id = AttrDict()
        self._flag = False

    def compute(self, im, dev_id, thr):
        self._flag = False
        hash1 = phash(im)
        hash2 = self.dev_id.get(dev_id, hash1[::-1])
        count = distance(hash1, hash2)
        if count + 10 >= int(thr): self._flag = True
        self.dev_id[dev_id] = hash1

        return self._flag
