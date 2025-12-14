import pandas as pd


def pivot_long_to_wide(
    df_long: pd.DataFrame,
    *,
    index_col: str,
    columns_col: str,
    value_col: str,
    aggfunc: str = "first",
) -> pd.DataFrame:
    """
    Convert long -> wide:
    index_col becomes rows, columns_col becomes columns, value_col becomes cell values.
    aggfunc handles duplicates (mean/sum/median/first/max/min).
    """
    wide = df_long.pivot_table(
        index=index_col,
        columns=columns_col,
        values=value_col,
        aggfunc=aggfunc,
    )
    return wide.reset_index()
