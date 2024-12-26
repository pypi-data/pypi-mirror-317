from typing import *
from .._misc import *
import itertools

def grid_iter(keys,lists):
    for config in itertools.product(*lists):
        yield Obj(**{key: value for key, value in zip(keys, config)})


def grid_dict(dict):
    keys = list(dict)
    lists = [dict[key] for key in keys]
    length = 1
    for l in lists:
        length *= len(l)
    return grid_iter(keys, lists), length



def grid_args(args):
    length = 1
    for l in args:
        length*=len(l)
    return itertools.product(*args),length



def triangle_iter(items,with_diagonal):
    for index1,item1 in enumerate(items):
        begin = index1
        if not with_diagonal:
            begin+=1
        for index2 in range(begin,len(items)):
            item2=items[index2]
            yield (item1,item2)

T = TypeVar('T')

from itertools import combinations

def powerset_iter(iterable):
    xs = list(iterable)
    for i in range(len(xs)+1):
        for p in combinations(xs,i):
            yield p















