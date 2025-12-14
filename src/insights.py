import streamlit as st
import pandas as pd

from src.plots.engine.ui_barplot import build_barplot_params
from src.plots.engine.ui_boxplot import build_boxplot_params
from src.plots.engine.ui_lineplot import build_lineplot_params

from src.plots.renderers.barplot import render_barplot
from src.plots.renderers.boxplot import render_boxplot
from src.plots.renderers.lineplot import render_lineplot
from src.plots.engine.ui_histogram import build_histogram_params
from src.plots.renderers.histogram import render_histogram
from src.plots.engine.ui_scatterplot import build_scatterplot_params
from src.plots.renderers.scatterplot import render_scatterplot
from src.plots.engine.ui_heatmap import build_heatmap_params
from src.plots.renderers.heatmap import render_heatmap


def render_insights(df: pd.DataFrame):
    st.title("📈 Insights (Multiple Plots)")

    st.subheader("👀 Data preview (first 10 rows)")
    st.dataframe(df.head(10))

    st.divider()

    plot_type = st.selectbox(
        "Choose plot",
        [
            "None",
            "barplot",
            "boxplot",
            "lineplot",
            "histogram",
            "scatterplot",
            "heatmap",
        ],
        index=0,
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
    elif plot_type == "histogram":
        params = build_histogram_params(df)
        if params:
            render_histogram(df, params)
    elif plot_type == "scatterplot":
        params = build_scatterplot_params(df)
        if params:
            render_scatterplot(df, params)
    elif plot_type == "heatmap":
        params = build_heatmap_params(df)
        if params:
            render_heatmap(df, params)
