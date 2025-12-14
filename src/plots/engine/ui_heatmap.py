import streamlit as st
import numpy as np


def build_heatmap_params(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.subheader("Correlation Heatmap")

    c1, c2, c3 = st.columns(3)
    with c1:
        cols = st.multiselect(
            "Numeric columns",
            numeric_cols,
            default=numeric_cols[:6],
        )
    with c2:
        method = st.selectbox(
            "Correlation method",
            ["pearson", "spearman", "kendall"],
            index=0,
        )
    with c3:
        annot = st.checkbox("Show values", value=True)

    c4, c5, c6 = st.columns(3)
    with c4:
        cmap = st.selectbox(
            "Color map",
            ["coolwarm", "viridis", "magma", "plasma", "RdBu", "YlGnBu"],
            index=0,
        )
    with c5:
        center = st.checkbox("Center at 0", value=True)
    with c6:
        linewidths = st.slider("Grid width", 0.0, 2.0, 0.5, 0.1)

    return {
        "columns": cols,
        "method": method,
        "annot": annot,
        "cmap": cmap,
        "center": 0 if center else None,
        "linewidths": linewidths,
    }
