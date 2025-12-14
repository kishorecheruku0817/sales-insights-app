import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._utils import filter_params
from ._show_code import generate_code
from ._plot_data import boxplot_data
from ._pivot import pivot_long_to_wide


_ALLOWED_BOXPLOT = {
    "x",
    "y",
    "hue",
    "order",
    "hue_order",
    "orient",
    "color",
    "palette",
    "saturation",
    "fill",
    "width",
    "dodge",
    "gap",
    "whis",
    "linewidth",
    "fliersize",
    "showfliers",
    "log_scale",
    "native_scale",
    "legend",
}


def render_boxplot(df, params):
    fig, ax = plt.subplots(figsize=(9, 5))

    rotation = params.get("rotation", 0)
    extra = params.get("extra_kwargs", {}) or {}

    safe = filter_params(params, _ALLOWED_BOXPLOT)
    safe_extra = extra if isinstance(extra, dict) else {}

    sns.boxplot(data=df, ax=ax, **safe, **safe_extra)
    ax.tick_params(axis="x", rotation=rotation)
    st.pyplot(fig)

    # 🔍 Show code
    with st.expander("🧾 Show code"):
        code = generate_code("sns.boxplot", safe)
        st.code(code, language="python")

    with st.expander("⬇️ Download plot data (CSV)"):
        plot_df = boxplot_data(
            df=df,
            x=safe["x"],
            y=safe["y"],
            hue=safe.get("hue"),
        )

        st.dataframe(plot_df.head(20))

        st.download_button(
            "📥 Download plot data CSV",
            data=plot_df.to_csv(index=False).encode("utf-8"),
            file_name="boxplot_data.csv",
            mime="text/csv",
        )
