from ._misc import *
from ._push_queries import *
from .agg import *
from . import agg

class _NoDefault:
    pass


class PushQuery(PushQueryElement):
    def __init__(self):
        self.head = None  # type: Optional[PushQueryElement]
        self.tail = None  # type: Optional[PushQueryElement]


    def _method_concatenator(self, pqe: AbstractPushQueryElement):
        if self.head is None:
            self.head = pqe
            self.tail = pqe
        else:
            self.tail.subscribe(pqe, None)
            self.tail = pqe
        return self

    def instance(self):
        if self.head is None:
            raise ValueError('PQEBuilder was not completed, HEAD is not set!')
        return self.head.instance()

    def select(self, selector: Callable) -> 'PushQuery':
        return self._method_concatenator(SelectPQE(selector))

    def where(self, filter: Callable) ->'PushQuery':
        return self._method_concatenator(WherePQE(filter))

    def select_many(self, selector: Callable) -> 'PushQuery':
        return self._method_concatenator(SelectManyPQE(selector))

    def split_pipelines(self, **kwargs:PushQueryElement):
        pqe = SplitPipelines(**kwargs)
        return self._method_concatenator(pqe)

    def split_by_group(self, group_selector, with_total = None):
        return self._method_concatenator(SplitByGroup(group_selector, with_total))

    def split_dictionary(self):
        return self._method_concatenator(SplitByDictionary())





    def first(self) -> 'PushQuery':
        return self._method_concatenator(agg.First())

    def first_or_default(self, default=None) -> 'PushQuery':
        return self._method_concatenator(agg.First().default_if_empty(default))

    def last(self) -> 'PushQuery':
        return self._method_concatenator(agg.Last())

    def last_or_default(self, default=None) -> 'PushQuery':
        return self._method_concatenator(agg.Last().default_if_empty(default))

    def single(self) -> 'PushQuery':
        return self._method_concatenator(agg.Single())

    def single_or_default(self, default=None) -> 'PushQuery':
        return self._method_concatenator(agg.Single().default_if_empty(default))

    def min(self, selector : Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> 'PushQuery':
        a = agg.Min(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def max(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> 'PushQuery':
        a = agg.Max(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def argmin(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> 'PushQuery':
        a = agg.ArgMin(selector)
        if not isinstance(default,_NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def argmax(self, selector: Callable[[T], TOut] = lambda z: z, default = _NoDefault()) -> 'PushQuery':
        a = agg.ArgMax(selector)
        if not isinstance(default, _NoDefault):
            a = a.default_if_empty(default)
        return self._method_concatenator(a)

    def sum(self) -> 'PushQuery':
        return self._method_concatenator(agg.Sum())

    def mean(self) -> 'PushQuery':
        return self._method_concatenator(agg.Mean())

    def count(self) -> 'PushQuery':
        return self._method_concatenator(agg.Count())

    def any(self, selector: Optional[Callable] = None) -> 'PushQuery':
        return self._method_concatenator(Any(selector))

    def all(self, selector: Optional[Callable] = None) -> 'PushQuery':
        return self._method_concatenator(agg.All(selector))

    def to_list(self) -> 'PushQuery':
        return self._method_concatenator(agg.ToList())

    def to_dictionary(self,
                      key_selector: Optional[Callable[[T], TKey]] = None,
                      value_selector: Optional[Callable[[T], TValue]] = None) -> 'PushQuery':
        return self._method_concatenator(agg.ToDictionary(key_selector, value_selector))

    def to_set(self) -> 'PushQuery':
        return self._method_concatenator(agg.ToSet())

    def to_tuple(self) -> 'PushQuery':
        return self._method_concatenator(agg.ToTuple())

    def aggregate_with(self, *args: PushQueryElement):
        if len(args)==1:
            return self._method_concatenator(args[0])
        else:
            return self._method_concatenator(SplitPipelines(*args))

    # region extended

    def to_dataframe(self, **kwargs) -> 'PushQuery':
        return self._method_concatenator(agg.ToDataframe(**kwargs))

    def to_ndarray(self) -> 'PushQuery':
        return self._method_concatenator(agg.ToNDArray())

    def to_series(self, value_selector: Optional[Callable] = None, key_selector: Optional[Callable] = None, **kwargs) -> 'PushQuery':
        return self._method_concatenator(agg.ToSeries(value_selector, key_selector, **kwargs))

    def to_text_file(self, filename: Union[str, Path], autoflush: bool = False, separator: str = '\n', **kwargs) -> 'PushQuery':
        return self._method_concatenator(agg.ToTextFile(filename, autoflush, separator, **kwargs))

    def to_zip_text_file(self, filename: Union[str, Path], separator: str = '\n', **kwargs) -> 'PushQuery':
        return self._method_concatenator(agg.ToZipTextFile(filename, separator, **kwargs))

    def to_pickle_file(self, filename) -> 'PushQuery':
        return self._method_concatenator(agg.ToPickleFile(filename))

    def to_zip_folder(self, filename: Union[str, Path], writer: Callable = pickle.dumps, replace=True,
                      compression=zipfile.ZIP_DEFLATED) -> 'PushQuery':
        return self._method_concatenator(agg.ToZipFolder(filename, writer, replace, compression))

    # endregion extended

