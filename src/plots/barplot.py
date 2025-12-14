# import json
# import numpy as np
# import pandas as pd
# import streamlit as st
# import seaborn as sns
# import matplotlib.pyplot as plt


# def noneify(v):
#     return None if v in (None, "None", "") else v


# def parse_json_dict(text, label="JSON"):
#     text = (text or "").strip()
#     if not text:
#         return None
#     try:
#         obj = json.loads(text)
#         if not isinstance(obj, dict):
#             st.error(f'{label} must be a JSON object (dict). Example: {{"alpha": 0.6}}')
#             return None
#         return obj
#     except Exception as e:
#         st.error(f"Invalid {label}: {e}")
#         return None


# def estimator_fn(name: str):
#     mapping = {
#         "mean": np.mean,
#         "sum": np.sum,
#         "median": np.median,
#         "count": len,
#         "min": np.min,
#         "max": np.max,
#     }
#     return mapping.get(name, np.mean)


# def errorbar_value(kind: str, level: int):
#     if kind == "None":
#         return None
#     if kind in ("sd", "se"):
#         return kind
#     return (kind, int(level))  # ('ci', 95) or ('pi', 95)


# def draw_barplot(df: pd.DataFrame, columns: list[str]):

#     # ---- Column lists (restrict y to numeric) ----
#     numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
#     x_cols = columns  # allow any column for x (categorical is common)
#     y_cols = numeric_cols  # restrict y to numeric only

#     st.subheader("Barplot")

#     # ---- Basic vs Advanced toggle ----
#     mode = st.radio("Mode", ["Basic", "Advanced"], horizontal=True)

#     # ---- Basic controls (always shown) ----
#     c1, c2, c3, c4 = st.columns([3, 3, 2, 2])
#     with c1:
#         x = st.selectbox("x (required)", x_cols, index=0)
#     with c2:
#         y = st.selectbox("y (numeric)", ["None"] + y_cols, index=0)
#     with c3:
#         hue = st.selectbox("hue", ["None"] + columns, index=0)
#     with c4:
#         rotation = st.selectbox("x tick rotation", list(range(0, 181, 5)), index=0)

#     x_col = noneify(x)
#     y_col = noneify(y)
#     hue_col = noneify(hue)

#     if x_col is None:
#         st.warning("x is required.")
#         return

#     # ---- Defaults for params ----
#     order = None
#     hue_order = None
#     orient = None
#     est_name = "mean"
#     err_kind = "ci"
#     err_level = 95
#     n_boot = 1000
#     seed = None
#     units = None
#     weights = None
#     color = None
#     palette = None
#     saturation = 0.75
#     fill = True
#     width = 0.8
#     dodge = "auto"
#     gap = 0.0
#     log_scale = None
#     native_scale = False
#     legend = "auto"
#     capsize = 0.0
#     err_kws = None
#     extra_kwargs = {}

#     # ---- Advanced panel ----
#     if mode == "Advanced":
#         with st.expander("Advanced parameters", expanded=True):
#             g1, g2, g3 = st.columns(3)

#             with g1:
#                 order_mode = st.selectbox(
#                     "order", ["None", "Auto (unique x)", "Manual select"], index=0
#                 )
#                 if order_mode == "Auto (unique x)":
#                     order = list(df[x_col].dropna().unique())
#                 elif order_mode == "Manual select":
#                     x_vals = [str(v) for v in df[x_col].dropna().unique()]
#                     order = st.multiselect("Pick order values", x_vals)

#             with g2:
#                 hue_order_mode = st.selectbox(
#                     "hue_order", ["None", "Auto (unique hue)", "Manual select"], index=0
#                 )
#                 if hue_col is not None and hue_order_mode == "Auto (unique hue)":
#                     hue_order = list(df[hue_col].dropna().unique())
#                 elif hue_col is not None and hue_order_mode == "Manual select":
#                     hue_vals = [str(v) for v in df[hue_col].dropna().unique()]
#                     hue_order = st.multiselect("Pick hue_order values", hue_vals)

#             with g3:
#                 orient = st.selectbox("orient", ["None", "x", "y", "h", "v"], index=0)
#                 orient = None if orient == "None" else orient

#             g4, g5, g6 = st.columns(3)
#             with g4:
#                 est_name = st.selectbox(
#                     "estimator",
#                     ["mean", "sum", "median", "count", "min", "max"],
#                     index=0,
#                 )
#             with g5:
#                 err_kind = st.selectbox(
#                     "errorbar", ["None", "ci", "pi", "sd", "se"], index=1
#                 )
#                 err_level = st.slider(
#                     "error level (ci/pi)",
#                     50,
#                     99,
#                     95,
#                     disabled=err_kind not in ("ci", "pi"),
#                 )
#             with g6:
#                 n_boot = st.number_input(
#                     "n_boot", min_value=0, max_value=100000, value=1000, step=100
#                 )

#             g7, g8, g9 = st.columns(3)
#             with g7:
#                 seed_text = st.text_input("seed (blank=None)", "")
#                 seed = int(seed_text) if seed_text.strip() else None
#             with g8:
#                 units = st.selectbox("units", ["None"] + columns, index=0)
#                 units = noneify(units)
#             with g9:
#                 weights = st.selectbox("weights", ["None"] + columns, index=0)
#                 weights = noneify(weights)

#             g10, g11, g12 = st.columns(3)
#             with g10:
#                 palette = st.selectbox(
#                     "palette",
#                     [
#                         "None",
#                         "deep",
#                         "muted",
#                         "bright",
#                         "pastel",
#                         "dark",
#                         "colorblind",
#                         "Set2",
#                         "Set3",
#                         "tab10",
#                     ],
#                     index=0,
#                 )
#                 palette = noneify(palette)
#                 color_text = st.text_input("color (optional)", "")
#                 color = noneify(color_text)
#             with g11:
#                 saturation = st.slider("saturation", 0.0, 1.0, 0.75, 0.05)
#                 fill = st.checkbox("fill", value=True)
#             with g12:
#                 width = st.slider("width", 0.1, 2.0, 0.8, 0.05)
#                 dodge_sel = st.selectbox("dodge", ["auto", "True", "False"], index=0)
#                 dodge = "auto" if dodge_sel == "auto" else (dodge_sel == "True")

#             g13, g14, g15 = st.columns(3)
#             with g13:
#                 gap = st.slider("gap", 0.0, 1.0, 0.0, 0.05)
#             with g14:
#                 log_scale = st.selectbox(
#                     "log_scale", ["None", "x", "y", "both"], index=0
#                 )
#                 log_scale = None if log_scale == "None" else log_scale
#                 native_scale = st.checkbox("native_scale", value=False)
#             with g15:
#                 legend_sel = st.selectbox("legend", ["auto", "True", "False"], index=0)
#                 legend = "auto" if legend_sel == "auto" else (legend_sel == "True")
#                 capsize = st.slider("capsize", 0.0, 1.0, 0.0, 0.05)

#             err_kws_text = st.text_area(
#                 "err_kws (JSON dict)",
#                 value="",
#                 placeholder='{"alpha": 0.6, "linewidth": 1}',
#             )
#             err_kws = parse_json_dict(err_kws_text, "err_kws")

#             kwargs_text = st.text_area(
#                 "kwargs (JSON dict)",
#                 value="",
#                 placeholder='{"edgecolor": "black", "linewidth": 1}',
#             )
#             extra_kwargs = parse_json_dict(kwargs_text, "kwargs") or {}

#     # ---- Build seaborn params ----
#     params = dict(
#         data=df,
#         x=x_col,
#         y=y_col,
#         hue=hue_col,
#         order=order,
#         hue_order=hue_order,
#         estimator=estimator_fn(est_name),
#         errorbar=errorbar_value(err_kind, int(err_level)),
#         n_boot=int(n_boot),
#         seed=seed,
#         units=units,
#         weights=weights,
#         orient=orient,
#         color=color,
#         palette=palette,
#         saturation=float(saturation),
#         fill=bool(fill),
#         width=float(width),
#         dodge=dodge,
#         gap=float(gap),
#         log_scale=log_scale,
#         native_scale=bool(native_scale),
#         legend=legend,
#         capsize=float(capsize),
#         err_kws=err_kws,
#     )
#     params.update(extra_kwargs)

#     # ---- Code snippet generator ----
#     with st.expander("Generate code snippet"):

#         def _repr(v):
#             if callable(v):
#                 # show the selected estimator name rather than a function repr
#                 return est_name
#             return repr(v)

#         # Build a readable call (avoid dumping full df)
#         pretty_lines = [
#             "sns.barplot(",
#             "    data=df,",
#             f"    x={_repr(x_col)},",
#             f"    y={_repr(y_col)},",
#             f"    hue={_repr(hue_col)},",
#         ]

#         # Include advanced params only when not default-ish or in Advanced mode
#         if mode == "Advanced":
#             for k in [
#                 "order",
#                 "hue_order",
#                 "orient",
#                 "palette",
#                 "color",
#                 "saturation",
#                 "fill",
#                 "width",
#                 "dodge",
#                 "gap",
#                 "log_scale",
#                 "native_scale",
#                 "legend",
#                 "capsize",
#                 "n_boot",
#                 "seed",
#                 "units",
#                 "weights",
#                 "err_kws",
#             ]:
#                 if k in params and params[k] is not None and params[k] != "auto":
#                     pretty_lines.append(f"    {k}={_repr(params[k])},")
#             pretty_lines.append(f"    estimator={est_name},")
#             pretty_lines.append(f"    errorbar={_repr(params['errorbar'])},")
#         pretty_lines.append(")")

#         st.code("\n".join(pretty_lines), language="python")

#     # ---- Plot ----
#     fig, ax = plt.subplots(figsize=(9, 5))
#     params["ax"] = ax
#     sns.barplot(**params)
#     ax.tick_params(axis="x", rotation=rotation)
#     st.pyplot(fig)
