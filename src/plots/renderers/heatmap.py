import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._show_code import generate_code


def render_heatmap(df, params):
    cols = params["columns"]
    method = params["method"]

    if len(cols) < 2:
        st.warning("Select at least two numeric columns.")
        return

    corr_df = df[cols].corr(method=method)

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        corr_df,
        annot=params["annot"],
        cmap=params["cmap"],
        center=params["center"],
        linewidths=params["linewidths"],
        ax=ax,
    )

    st.pyplot(fig)

    # ---- Show code ----
    with st.expander("🧾 Show code"):
        code = f"""
corr = df[{cols!r}].corr(method={method!r})

sns.heatmap(
    corr,
    annot={params['annot']},
    cmap={params['cmap']!r},
    center={params['center']},
    linewidths={params['linewidths']},
)
""".strip()
        st.code(code, language="python")

    # ---- Download correlation matrix ----
    with st.expander("⬇️ Download correlation matrix (CSV)"):
        st.dataframe(corr_df)
        st.download_button(
            "📥 Download correlation CSV",
            data=corr_df.to_csv().encode("utf-8"),
            file_name="correlation_matrix.csv",
            mime="text/csv",
        )
