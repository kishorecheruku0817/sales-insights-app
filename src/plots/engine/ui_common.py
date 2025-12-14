import numpy as np
import pandas as pd
import streamlit as st
from .utils import noneify, parse_json_dict


def get_columns(df: pd.DataFrame):
    cols = df.columns.tolist()
    num = df.select_dtypes(include=[np.number]).columns.tolist()
    cat = [c for c in cols if c not in num]
    return cols, num, cat


def ui_axes(df, *, y_numeric_only=True):
    cols, num_cols, _ = get_columns(df)

    c1, c2, c3, c4 = st.columns([3, 3, 2, 2])
    with c1:
        x = st.selectbox("x", cols)
    with c2:
        y_choices = num_cols if y_numeric_only else cols
        y = st.selectbox("y", ["None"] + y_choices)
    with c3:
        hue = st.selectbox("hue", ["None"] + cols)
    with c4:
        rotation = st.selectbox("x tick rotation", list(range(0, 181, 5)), index=0)

    return {
        "x": noneify(x),
        "y": noneify(y),
        "hue": noneify(hue),
        "rotation": int(rotation),
    }


def ui_style_common(plot_kind: str):
    """
    plot_kind: "cat" for bar/box/violin, "line" for line/scatter
    Returns only params that that kind supports.
    """
    st.markdown("### Style")
    c1, c2, c3 = st.columns(3)

    with c1:
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
        color = st.text_input("color (optional)", "")

    with c2:
        legend = st.selectbox("legend", ["auto", "True", "False"], index=0)
        # log_scale = st.selectbox("log_scale", ["None", "x", "y", "both"], index=0)

    with c3:
        # saturation is ONLY for categorical (bar/box/violin etc)
        saturation = None
        if plot_kind == "cat":
            saturation = st.slider("saturation", 0.0, 1.0, 0.75, 0.05)

    out = {
        "palette": noneify(palette),
        "color": noneify(color),
        "legend": "auto" if legend == "auto" else (legend == "True"),
        # "log_scale": None if log_scale == "None" else log_scale,
    }
    if plot_kind == "cat":
        out["saturation"] = float(saturation)

    return out


def ui_kwargs_blocks():
    err_kws_text = st.text_area(
        "err_kws (JSON dict)", value="", placeholder='{"alpha": 0.6, "linewidth": 1}'
    )
    kwargs_text = st.text_area(
        "kwargs (JSON dict)",
        value="",
        placeholder='{"edgecolor": "black", "linewidth": 1}',
    )
    return {
        "err_kws": parse_json_dict(err_kws_text, "err_kws"),
        "extra_kwargs": parse_json_dict(kwargs_text, "kwargs") or {},
    }
