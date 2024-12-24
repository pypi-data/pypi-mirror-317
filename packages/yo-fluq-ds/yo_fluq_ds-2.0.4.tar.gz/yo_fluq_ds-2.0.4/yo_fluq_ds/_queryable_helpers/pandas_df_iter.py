from .._misc import Obj

# region yo_fluq_ds
import pandas as pd


def pandas_df_iter(dataframe, as_obj: bool):
    for row in dataframe.iterrows():
        if as_obj:
            yield Obj(**row[1].to_dict())
        else:
            yield row[1].to_dict()

# endregion yo_fluq_ds