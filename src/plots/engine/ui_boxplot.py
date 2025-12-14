import streamlit as st
from .ui_common import ui_axes, ui_style_common
from .utils import noneify


def build_boxplot_params(df):
    st.subheader("Boxplot configuration")

    mode = st.radio("Mode", ["Basic", "Advanced"], horizontal=True)
    axes = ui_axes(df, y_numeric_only=True)
    if axes["x"] is None or axes["y"] is None:
        st.warning("Boxplot needs both x (category) and y (numeric).")
        return None

    params = dict(
        x=axes["x"],
        y=axes["y"],
        hue=axes["hue"],
        rotation=axes["rotation"],
        dodge=True,
        width=0.8,
        gap=0.0,
        showfliers=True,
    )

    with st.expander("Style", expanded=(mode == "Advanced")):
        params.update(ui_style_common("cat"))

        if mode == "Advanced":
            c1, c2, c3 = st.columns(3)
            with c1:
                params["showfliers"] = st.checkbox("showfliers", value=True)
            with c2:
                params["width"] = float(st.slider("width", 0.1, 2.0, 0.8, 0.05))
            with c3:
                dodge_sel = st.selectbox("dodge", ["True", "False"], index=0)
                params["dodge"] = dodge_sel == "True"

    return params
