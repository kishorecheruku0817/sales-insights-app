import streamlit as st
import pandas as pd

from src.plots.engine.ui_barplot import build_barplot_params
from src.plots.engine.ui_boxplot import build_boxplot_params
from src.plots.engine.ui_lineplot import build_lineplot_params

from src.plots.renderers.barplot import render_barplot
from src.plots.renderers.boxplot import render_boxplot
from src.plots.renderers.lineplot import render_lineplot


def render_insights(df: pd.DataFrame):
    st.title("📈 Insights (Multiple Plots)")

    st.subheader("👀 Data preview (first 10 rows)")
    st.dataframe(df.head(10))

    st.divider()

    plot_type = st.selectbox(
        "Choose plot", ["None", "barplot", "boxplot", "lineplot"], index=0
    )

    if plot_type == "barplot":
        params = build_barplot_params(df)
        if params:
            render_barplot(df, params)

    elif plot_type == "boxplot":
        params = build_boxplot_params(df)
        if params:
            render_boxplot(df, params)

    elif plot_type == "lineplot":
        params = build_lineplot_params(df)
        if params:
            render_lineplot(df, params)
