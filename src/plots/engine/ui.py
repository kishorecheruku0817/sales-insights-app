# import streamlit as st
# import numpy as np
# import pandas as pd
# from .config import PlotConfig
# from .utils import noneify, estimator_fn


# def render_plot_ui(df, plot_type: str) -> PlotConfig:
#     columns = df.columns.tolist()
#     numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

#     st.subheader(f"{plot_type.title()} configuration")

#     x = st.selectbox("X axis", columns)
#     y = st.selectbox("Y axis", ["None"] + numeric_cols)
#     hue = st.selectbox("Hue", ["None"] + columns)

#     rotation = st.selectbox("X label rotation", range(0, 181, 5))

#     estimator_name = st.selectbox("Estimator", ["mean", "sum", "median", "count"])

#     return PlotConfig(
#         plot_type=plot_type,
#         x=x,
#         y=noneify(y),
#         hue=noneify(hue),
#         estimator=estimator_fn(estimator_name),
#         rotation=rotation,
#     )
