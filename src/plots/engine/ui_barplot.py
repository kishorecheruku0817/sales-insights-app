import streamlit as st
from .ui_common import ui_axes, ui_style_common, ui_kwargs_blocks
from .utils import estimator_fn, errorbar_value, noneify


def build_barplot_params(df):
    st.subheader("Barplot configuration")

    mode = st.radio("Mode", ["Basic", "Advanced"], horizontal=True)

    axes = ui_axes(df, y_numeric_only=True)
    if axes["x"] is None:
        st.warning("x is required.")
        return None

    # Defaults
    params = dict(
        x=axes["x"],
        y=axes["y"],
        hue=axes["hue"],
        rotation=axes["rotation"],
        order=None,
        hue_order=None,
        estimator=estimator_fn("mean"),
        errorbar=("ci", 95),
        n_boot=1000,
        seed=None,
        orient=None,
        width=0.8,
        dodge="auto",
        gap=0.0,
        fill=True,
        capsize=0.0,
        native_scale=False,
    )

    if mode == "Advanced":
        with st.expander("Advanced barplot params", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                est_name = st.selectbox(
                    "estimator",
                    ["mean", "sum", "median", "count", "min", "max"],
                    index=0,
                )
                params["estimator"] = estimator_fn(est_name)
            with c2:
                err_kind = st.selectbox(
                    "errorbar", ["None", "ci", "pi", "sd", "se"], index=1
                )
                err_level = st.slider(
                    "error level (ci/pi)",
                    50,
                    99,
                    95,
                    disabled=err_kind not in ("ci", "pi"),
                )
                params["errorbar"] = errorbar_value(err_kind, int(err_level))
            with c3:
                params["n_boot"] = int(
                    st.number_input(
                        "n_boot", min_value=0, max_value=100000, value=1000, step=100
                    )
                )

            c4, c5, c6 = st.columns(3)
            with c4:
                seed_txt = st.text_input("seed (blank=None)", "")
                params["seed"] = int(seed_txt) if seed_txt.strip() else None
            with c5:
                params["width"] = float(st.slider("width", 0.1, 2.0, 0.8, 0.05))
            with c6:
                dodge_sel = st.selectbox("dodge", ["auto", "True", "False"], index=0)
                params["dodge"] = (
                    "auto" if dodge_sel == "auto" else (dodge_sel == "True")
                )

            params["gap"] = float(st.slider("gap", 0.0, 1.0, 0.0, 0.05))
            params["fill"] = st.checkbox("fill", value=True)
            params["capsize"] = float(st.slider("capsize", 0.0, 1.0, 0.0, 0.05))

            style = ui_style_common("cat")
            params.update(style)

            blocks = ui_kwargs_blocks()
            params["err_kws"] = blocks["err_kws"]
            params["extra_kwargs"] = blocks["extra_kwargs"]

    else:
        # Basic still gets style (small)
        with st.expander("Style", expanded=False):
            params.update(ui_style_common("cat"))

    return params
