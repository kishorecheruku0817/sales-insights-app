import numpy as np
import streamlit as st
from .utils import noneify


def build_scatterplot_params(df):
    cols = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.subheader("Scatter plot configuration")

    c1, c2, c3 = st.columns([3, 3, 2])
    with c1:
        x = st.selectbox("x (numeric)", numeric_cols)
    with c2:
        y = st.selectbox("y (numeric)", numeric_cols)
    with c3:
        hue = st.selectbox("hue (optional)", ["None"] + cols)

    c4, c5, c6 = st.columns(3)
    with c4:
        size = st.selectbox("size (optional)", ["None"] + numeric_cols)
    with c5:
        style = st.selectbox("style (optional)", ["None"] + cols)
    with c6:
        alpha = st.slider("alpha", 0.1, 1.0, 0.8, 0.05)

    st.markdown("### Regression (optional)")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        add_reg = st.checkbox("Add regression line", value=False)
    with r2:
        reg_ci = st.selectbox("CI", ["None", "95", "68"], index=0, disabled=not add_reg)
    with r3:
        reg_order = st.selectbox(
            "Polynomial order", [1, 2, 3], index=0, disabled=not add_reg
        )
    with r4:
        reg_scatter = st.checkbox(
            "Show points in regplot", value=False, disabled=not add_reg
        )

    st.markdown("### Style")
    s1, s2, s3 = st.columns(3)
    with s1:
        palette = st.selectbox(
            "palette",
            [
                "None",
                "deep",
                "muted",
                "bright",
                "pastel",
                "dark",
                "colorblind",
                "Set2",
                "Set3",
                "tab10",
            ],
            index=0,
        )
    with s2:
        color = st.text_input("color (optional)", "")
    with s3:
        legend_sel = st.selectbox("legend", ["auto", "True", "False"], index=0)

    legend = "auto" if legend_sel == "auto" else (legend_sel == "True")

    return {
        # scatter
        "x": x,
        "y": y,
        "hue": noneify(hue),
        "size": noneify(size),
        "style": noneify(style),
        "alpha": float(alpha),
        "palette": noneify(palette),
        "color": noneify(color),
        "legend": legend,
        # regression options (stored for renderer)
        "add_reg": bool(add_reg),
        "reg_ci": None if reg_ci == "None" else int(reg_ci),
        "reg_order": int(reg_order),
        "reg_scatter": bool(reg_scatter),
    }
