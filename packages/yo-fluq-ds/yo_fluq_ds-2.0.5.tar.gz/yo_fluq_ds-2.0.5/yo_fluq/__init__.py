from ._misc import *
from .queryable import Queryable
from .push_query import AbstractPushQueryElement, PushQuery
from .query import Query
from . import fluq, agg



# region extended


import pandas as pd
from typing import *

T = TypeVar('T')
TOut = TypeVar('TOut')

def _feed(object: T, *methods):
    result = object
    for method in methods:
        result = method(result)
    return result




pd.Series.feed = _feed
pd.DataFrame.feed = _feed
pd.core.groupby.DataFrameGroupBy.feed = _feed
pd.core.groupby.SeriesGroupBy.feed = _feed

# endregion extended