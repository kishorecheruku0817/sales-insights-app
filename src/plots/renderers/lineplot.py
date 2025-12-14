import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._utils import filter_params
from ._show_code import generate_code
from ._plot_data import lineplot_data


_ALLOWED_LINEPLOT = {
    "x",
    "y",
    "hue",
    "palette",
    "color",
    "marker",
    "linewidth",
    "legend",
    "log_scale",
    "units",
    "estimator",
    "errorbar",
    "n_boot",
    "seed",
}


def render_lineplot(df, params):
    fig, ax = plt.subplots(figsize=(9, 5))

    rotation = params.get("rotation", 0)

    # ✅ Only keep seaborn-supported params
    safe = filter_params(params, _ALLOWED_LINEPLOT)

    # ---- Plot ----
    sns.lineplot(data=df, ax=ax, **safe)
    ax.tick_params(axis="x", rotation=rotation)
    st.pyplot(fig)

    # ---- Show code (exactly what ran) ----
    with st.expander("🧾 Show code"):
        code = generate_code(
            plot_func="sns.lineplot",
            params=safe,
            data_var="df",
        )
        st.code(code, language="python")

    with st.expander("⬇️ Download plot data (CSV)"):
        # estimator name: store it in params from UI as "estimator_name"
        est_name = params.get("estimator", "mean")
        plot_df = lineplot_data(
            df, safe["x"], safe.get("y"), safe.get("hue"), estimator_name=est_name
        )

        print(plot_df)
        csv_bytes = plot_df.to_csv(index=False).encode("utf-8")
        st.dataframe(plot_df.head(20))
        st.download_button(
            "📥 Download plot data CSV",
            data=csv_bytes,
            file_name="lineplot_data.csv",
            mime="text/csv",
        )
