import streamlit as st
import numpy as np
from .utils import noneify


def build_histogram_params(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    all_cols = df.columns.tolist()

    st.subheader("Histogram configuration")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        x = st.selectbox("Numeric column", numeric_cols)
    with c2:
        hue = st.selectbox("Hue (optional)", ["None"] + all_cols)
    with c3:
        bins = st.slider("Bins", min_value=5, max_value=100, value=30, step=5)
    with c4:
        stat = st.selectbox(
            "Statistic", ["count", "frequency", "probability", "density"]
        )

    c5, c6, c7 = st.columns(3)
    with c5:
        kde = st.checkbox("Show KDE", value=False)
    with c6:
        element = st.selectbox("Element", ["bars", "step", "poly"])
    with c7:
        multiple = st.selectbox("Multiple", ["layer", "stack", "dodge", "fill"])

    return {
        "x": x,
        "hue": noneify(hue),
        "bins": bins,
        "stat": stat,
        "kde": kde,
        "element": element,
        "multiple": multiple,
    }
