import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._utils import filter_params
from ._show_code import generate_code
from ._plot_data import histogram_data


_ALLOWED_HIST = {
    "x",
    "hue",
    "bins",
    "stat",
    "kde",
    "element",
    "multiple",
    "color",
    "palette",
    "legend",
}


def render_histogram(df, params):
    fig, ax = plt.subplots(figsize=(9, 5))

    safe = filter_params(params, _ALLOWED_HIST)

    sns.histplot(data=df, ax=ax, **safe)
    st.pyplot(fig)

    # ---- Show code ----
    with st.expander("🧾 Show code"):
        code = generate_code(
            plot_func="sns.histplot",
            params=safe,
            data_var="df",
        )
        st.code(code, language="python")

    # ---- Download plot data ----
    with st.expander("⬇️ Download plot data (CSV)"):
        plot_df = histogram_data(
            df=df,
            x=safe["x"],
            hue=safe.get("hue"),
        )

        st.dataframe(plot_df.head(20))

        st.download_button(
            "📥 Download histogram data CSV",
            data=plot_df.to_csv(index=False).encode("utf-8"),
            file_name="histogram_data.csv",
            mime="text/csv",
        )
