import numpy as np
import pandas as pd
import streamlit as st

def clean_dataframe(
    df: pd.DataFrame,
    drop_all_na_rows: bool = False,
    drop_any_na_rows: bool = True,
    fill_numeric_zero: bool = True,
    fill_cat_unknown: bool = True,
    drop_all_duplicates: bool = True,
  ):
    """
    Apply cleaning rules to the input DataFrame and return a cleaned copy.
    """
    df_cleaned = df.copy()
    rows_before = df_cleaned.shape[0]

    # detect numeric / categorical
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df_cleaned.select_dtypes(exclude=[np.number]).columns.tolist()

    if drop_all_na_rows:
        df_cleaned = df_cleaned.dropna(how="all")

    if drop_any_na_rows:
        df_cleaned = df_cleaned.dropna(how="any")
    else:
        if fill_numeric_zero and numeric_cols:
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(0)
        if fill_cat_unknown and cat_cols:
            df_cleaned[cat_cols] = df_cleaned[cat_cols].fillna("Unknown")

    if drop_all_duplicates:
        df_cleaned = df_cleaned.drop_duplicates()

    rows_after = df_cleaned.shape[0]
    return df_cleaned, rows_before, rows_after
