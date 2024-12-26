from typing import *



from ._queryable_helpers import *
from ._push_queries import *
from . import agg
import itertools


T = TypeVar('T')
TOut = TypeVar('TOut')

class _NoDefault:
    pass

class Queryable(Generic[T]):
    def __init__(self, en: Iterable[T], length: Optional[int] = None):
        self.en = en
        self.length = length

    def __iter__(self):
        for e in self.en:
            yield e

    def _method_concatenator(self, aggregator: AbstractPushQueryElement):
        return aggregator(self.en)

    ## Core methods

    def select(self, selector: Callable[[T], TOut]) -> 'Queryable[TOut]':
        return Queryable(map(selector, self.en), self.length)

    def where(self, filterSelector: Callable[[T], bool]) -> 'Queryable[T]':
        return Queryable(filter(filterSelector, self.en))

    def distinct(self, selector: Optional[Callable[[T], TOut]] = None) -> 'Queryable[T]':
        return Queryable(distinct(self.en, selector))

    def select_many(self, selector: Callable[[T], Iterable[TOut]]) -> 'Queryable[TOut]':
        return Queryable(itertools.chain.from_iterable(map(selector, self.en)))

    def with_indices(self) -> 'Queryable[ItemWithIndex[T]]':
        return Queryable(with_indices(self.en), self.length)

    def group_by(self, selector: Callable[[T], TKey]) -> 'Queryable[Group[TKey,T]]':
        return Queryable(group_by(self.en, selector))


    def skip(self, count) -> 'Queryable[T]':
        return Queryable(itertools.islice(self.en, count, None))

    def take(self, count) -> 'Queryable[T]':
        return Queryable(itertools.islice(self.en, count))

    def skip_while(self, condition) -> 'Queryable[T]':
        return Queryable(skip_while(self.en, condition))

    def take_while(self, condition) -> 'Queryable[T]':
        return Queryable(take_while(self.en, condition))

    def append(self, *args: T) -> 'Queryable[T]':
        return Queryable(append(self.en, args))

    def prepend(self, *args: T) -> 'Queryable[T]':
        return Queryable(prepend(self.en, args))

    def intersect(self, en2: Iterable[T]) -> 'Queryable[T]':
        return Queryable(intersect(self.en, en2))

    def concat(self, en2: Iterable[T]) -> 'Queryable[T]':
        return Queryable(concat(self.en, en2))

    def order_by(self, selector: Callable[[T], Any]) -> 'Queryable[T]':
        return Queryable(Orderer(self.en, [(-1, selector)]), self.length)

    def order_by_descending(self, selector: Callable[[T], Any]) -> 'Queryable[T]':
        return Queryable(Orderer(self.en, [(1, selector)]), self.length)

    def then_by(self, selector: Callable[[T], Any]) -> 'Queryable[T]':
        if not isinstance(self.en, Orderer):
            raise ValueError('then_by can only be called directly after order_by or order_by_descending')
        return Queryable(Orderer(self.en, self.en._funcs + [(-1, selector)]), self.length)

    def then_by_descending(self, selector: Callable[[T], Any]) -> 'Queryable[T]':
        if not isinstance(self.en, Orderer):
            raise ValueError('then_by can only be called directly after order_by or order_by_descending')
        return Queryable(Orderer(self.en, self.en._funcs + [(1, selector)]), self.length)

    def foreach(self, action: Callable[[T], None]) -> None:
        foreach(self.en, action)

    def foreach_and_continue(self, action: Callable[[T], None]) -> 'Queryable[T]':
        return Queryable(foreach_and_continue(self.en, action), self.length)


    def fork(self, context: ForkContext, pipeline: Callable[[Any, Iterable[T]], Any]) -> 'Queryable[T]':
        return Queryable(fork(self.en, context, pipeline))

    def fire_and_forget(self, pipeline: Callable[[Iterable[T]], Any]) -> 'Queryable[T]':
        return Queryable(fork(self.en, ForkContext(None), lambda q, _: pipeline(q)))

    def parallel_select(self, selector, workers_count=None, buffer_size=1) -> 'Queryable[T]':
        return Queryable(parallel_select(self.en, selector, workers_count, buffer_size), self.length)

    def feed(self, *collectors: Callable):
        result = self
        for collector in collectors:
            result = collector(result)
        return result

    def aggregate(self, aggregator):
        return aggregate(self.en, aggregator)

    ## Aggregation methods



    def first(self) -> T:
        return self._method_concatenator(agg.First())

    def first_or_default(self, default=None) -> Optional[T]:
        return self._method_concatenator(agg.First().default_if_empty(default))

    def last(self) -> T:
        return self._method_concatenator(agg.Last())

    def last_or_default(self, default=None) -> Optional[T]:
        return self._method_concatenator(agg.Last().default_if_empty(default))

    def single(self) -> T:
        return self._method_concatenator(agg.Single())

    def single_or_default(self, default=None) -> Optional[T]:
        return self._method_concatenator(agg.Single().default_if_empty(default))

    def min(self, selector : Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> T:
        a = agg.Min(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def max(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> T:
        a = agg.Max(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def argmin(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> TOut:
        a = agg.ArgMin(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def argmax(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> TOut:
        a = agg.ArgMax(selector)
        if not isinstance(default, _NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def sum(self) -> T:
        return self._method_concatenator(agg.Sum())

    def mean(self) -> float:
        return self._method_concatenator(agg.Mean())

    def count(self) -> int:
        return self._method_concatenator(agg.Count())

    def any(self, selector: Optional[Callable] = None) -> bool:
        return self._method_concatenator(agg.Any(selector))

    def all(self, selector: Optional[Callable] = None) -> bool:
        return self._method_concatenator(agg.All(selector))

    def to_list(self) -> List[T]:
        return self._method_concatenator(agg.ToList())

    def to_dictionary(self,
                      key_selector: Optional[Callable[[T], TKey]] = None,
                      value_selector: Optional[Callable[[T], TValue]] = None) -> Dict[TKey, TValue]:
        return self._method_concatenator(agg.ToDictionary(key_selector, value_selector))

    def to_set(self) -> Set[T]:
        return self._method_concatenator(agg.ToSet())

    def to_tuple(self) -> Tuple[T,...]:
        return self._method_concatenator(agg.ToTuple())

    def aggregate_with(self, *args: PushQueryElement):
        if len(args)==1:
            return self._method_concatenator(args[0])
        else:
            return self._method_concatenator(SplitPipelines(*args))


    def to_text_file(self, filename: Union[str, Path], autoflush: bool = False, separator: str = '\n', **kwargs) -> None:
        return self._method_concatenator(agg.ToTextFile(filename, autoflush, separator, **kwargs))

    def to_zip_text_file(self, filename: Union[str, Path], separator: str = '\n', **kwargs) -> None:
        return self._method_concatenator(agg.ToZipTextFile(filename, separator, **kwargs))

    def to_pickle_file(self, filename) -> None:
        return self._method_concatenator(agg.ToPickleFile(filename))

    def to_zip_folder(self, filename: Union[str, Path], writer: Callable = pickle.dumps, replace=True,
                      compression=zipfile.ZIP_DEFLATED) -> None:
        return self._method_concatenator(agg.ToZipFolder(filename, writer, replace, compression))




