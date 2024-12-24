from typing import *
from collections import OrderedDict
from ...queryable import Queryable
from ...query import Query

def strjoin(separator: str):
    return lambda en: separator.join([str(s) for s in en])


class pairwise:
    def __init__(self):
        pass

    def _make(self, en):
        old = None
        firstTime = True
        for e in en:
            if not firstTime:
                yield (old, e)
            old = e
            if firstTime:
                firstTime = False

    def __call__(self, en):
        return Queryable(self._make(en))


class count_by:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, en):
        result = OrderedDict()
        for e in en:
            gr = self.selector(e)
            if gr not in result:
                result[gr] = 0
            result[gr] += 1
        return Query.dict(result)
