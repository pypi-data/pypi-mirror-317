from typing import *
from ._misc import *
from ._queryable_helpers import *
from .queryable import Queryable
from .push_query import PushQuery

# region extended
import pandas as pd
import numpy as np
# endregion extended



class FileQuery:
    def text(self, path: Union[str,Path], **file_kwargs) -> Queryable[str]:
        return Queryable(text_file(path, **file_kwargs))

    def zipped_text(self, path: Union[str,Path], encoding: str ='utf-8') -> Queryable[str]:
        return Queryable(zip_text_file(path, encoding))

    def zipped_folder(self, path: Union[str,Path], parser: Callable = pickle.loads, with_length:bool = True):
        length = None
        if with_length:
            with zipfile.ZipFile(path, 'r') as zfile:
                length = len(zfile.namelist())
        return Queryable(zip_folder(path,parser), length)


    def pickle(self,
               path: Union[str,Path],
               file_obj_factory:Optional[Callable] = lambda fname: open(fname,'rb')
               ) -> Queryable[Any]:
        return Queryable(pickle_file(path, file_obj_factory))


class CombinatoricsQuery:
    def grid(self, **kwargs)->Queryable[Obj]:
        return Queryable(*grid_dict(kwargs))

    def grid_dict(self, dict) -> Queryable[Obj]:
        return Queryable(*grid_dict(dict))

    def cartesian(self,*args)->Queryable[Tuple]:
        return Queryable(*grid_args(args))

    def triangle(self, items: T, with_diagonal=True) -> Queryable[Tuple[T, T]]:
        return Queryable(triangle_iter(items, with_diagonal), (len(items) * (len(items) - 1)) // 2)

    def powerset(self, iterable: Iterable[T]) -> Queryable[Tuple[T,...]]:
        return Queryable(powerset_iter(iterable))

class QueryClass:
    def en(self, en: Iterable[T]) -> Queryable[T]:
        length = None
        if hasattr(en, '__len__'):
            length = len(en)
        return Queryable(en,length)

    def args(self, *args: T)  -> Queryable[T]:
        return Queryable(args,len(args))


    def dict(self, dictionary: Dict[TKey, TValue])  -> Queryable[KeyValuePair[TKey, TValue]]:
        return Queryable(dictionary.items(),len(dictionary)).select(lambda z: KeyValuePair(z[0],z[1]))

    def push(self) -> PushQuery:
        return PushQuery()

    def loop(self, begin: T, delta: T, end: Optional[T] = None, endtype=LoopEndType.NotEqual) -> Queryable[T]:
        lp = loop_maker(begin,delta,end,endtype)
        return Queryable(lp.make())

    file = FileQuery()

    combinatorics = CombinatoricsQuery()

    def folder(self, location: Union[Path, str], pattern: str = '*') -> Queryable[Path]:
        return Queryable(folder(location, pattern))


    # region extended
    def df(self, dataframe: pd.DataFrame, as_obj: bool = True) -> Queryable[Obj]:
        return Queryable(pandas_df_iter(dataframe, as_obj), dataframe.shape[0])

    def series(self, series: pd.Series) -> Queryable[KeyValuePair]:
        return Queryable(
            map(lambda z: KeyValuePair(z[0], z[1]), zip(series.index, series)),
            series.shape[0]
        )

    # endregion extended

Query = QueryClass()