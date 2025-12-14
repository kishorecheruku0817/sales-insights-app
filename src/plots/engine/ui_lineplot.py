import streamlit as st
from .ui_common import ui_axes, ui_style_common
from .utils import estimator_fn, noneify


def build_lineplot_params(df):
    st.subheader("Lineplot configuration")

    mode = st.radio("Mode", ["Basic", "Advanced"], horizontal=True)
    axes = ui_axes(df, y_numeric_only=True)
    if axes["x"] is None or axes["y"] is None:
        st.warning("Lineplot needs both x and y.")
        return None

    params = dict(
        x=axes["x"],
        y=axes["y"],
        hue=axes["hue"],
        rotation=axes["rotation"],
        marker=noneify(
            st.selectbox("marker", ["None", "o", ".", "s", "D", "^", "v", "x"], index=0)
        ),
        linewidth=float(st.slider("linewidth", 0.5, 6.0, 2.0, 0.5)),
        estimator=estimator_fn("mean"),
    )

    with st.expander("Style", expanded=(mode == "Advanced")):
        params.update(ui_style_common("line"))
        est_name = st.selectbox(
            "estimator",
            ["mean", "sum", "median", "count", "min", "max"],
            index=0,
        )
        params["estimator"] = estimator_fn(est_name)

    return params
