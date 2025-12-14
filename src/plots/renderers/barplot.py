import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._utils import filter_params
from ._show_code import generate_code
from ._plot_data import barplot_data
from ._pivot import pivot_long_to_wide


_ALLOWED_BARPLOT = {
    "x",
    "y",
    "hue",
    "order",
    "hue_order",
    "estimator",
    "errorbar",
    "n_boot",
    "seed",
    "units",
    "weights",
    "orient",
    "color",
    "palette",
    "saturation",
    "fill",
    "width",
    "dodge",
    "gap",
    "log_scale",
    "native_scale",
    "legend",
    "capsize",
    "err_kws",
}


def render_barplot(df, params):
    fig, ax = plt.subplots(figsize=(9, 5))

    rotation = params.get("rotation", 0)
    extra = params.get("extra_kwargs", {}) or {}

    safe = filter_params(params, _ALLOWED_BARPLOT)
    safe_extra = extra if isinstance(extra, dict) else {}

    sns.barplot(data=df, ax=ax, **safe, **safe_extra)
    ax.tick_params(axis="x", rotation=rotation)
    st.pyplot(fig)

    # 🔍 Show code
    with st.expander("🧾 Show code"):
        code = generate_code("sns.barplot", safe)
        st.code(code, language="python")

    with st.expander("⬇️ Download plot data (CSV)"):
        # estimator name: store it in params from UI as "estimator_name"
        est_name = params.get("estimator", "mean")
        plot_df = barplot_data(
            df, safe["x"], safe.get("y"), safe.get("hue"), estimator_name=est_name
        )

        # Identify the value column (count OR agg_y)
        value_cols = [
            c
            for c in plot_df.columns
            if c not in [safe["x"], safe.get("hue")] and c is not None
        ]
        value_col = value_cols[0] if value_cols else None

        format_choice = st.selectbox(
            "CSV format",
            ["Long (recommended)", "Wide (pivot)"],
            index=0,
            key="barplot_csv_format",
        )

        aggfunc = st.selectbox(
            "Pivot aggregation (if duplicates)",
            ["first", "mean", "sum", "median", "min", "max"],
            index=0,
            key="barplot_pivot_agg",
            disabled=not (
                format_choice.startswith("Wide") and safe.get("hue") and value_col
            ),
        )

        export_df = plot_df
        if format_choice.startswith("Wide") and safe.get("hue") and value_col:
            export_df = pivot_long_to_wide(
                plot_df,
                index_col=safe["x"],
                columns_col=safe["hue"],
                value_col=value_col,
                aggfunc=aggfunc,
            )
        csv_bytes = export_df.to_csv(index=False).encode("utf-8")
        st.dataframe(export_df.head(20))
        st.download_button(
            "📥 Download plot data CSV",
            data=csv_bytes,
            file_name="barplot_data.csv",
            mime="text/csv",
        )
