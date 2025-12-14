import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from ._utils import filter_params
from ._show_code import generate_code
from ._plot_data import scatterplot_data


_ALLOWED_SCATTER = {
    "x",
    "y",
    "hue",
    "size",
    "style",
    "alpha",
    "palette",
    "color",
    "legend",
}


def render_scatterplot(df, params):
    fig, ax = plt.subplots(figsize=(9, 5))

    # regression config is renderer-only (not passed to sns.scatterplot)
    add_reg = params.get("add_reg", False)
    reg_ci = params.get("reg_ci", None)
    reg_order = params.get("reg_order", 1)
    reg_scatter = params.get("reg_scatter", False)

    safe = filter_params(params, _ALLOWED_SCATTER)

    # ---- Scatter plot ----
    sns.scatterplot(data=df, ax=ax, **safe)

    # ---- Regression line ----
    # regplot doesn't support hue directly; we do one regression per hue group if hue exists
    if add_reg:
        x = safe["x"]
        y = safe["y"]
        hue = safe.get("hue")

        if hue:
            for val, g in df[[x, y, hue]].dropna().groupby(hue):
                sns.regplot(
                    data=g,
                    x=x,
                    y=y,
                    scatter=reg_scatter,
                    ci=reg_ci,
                    order=reg_order,
                    ax=ax,
                    label=f"{val} trend",
                )
        else:
            sns.regplot(
                data=df,
                x=x,
                y=y,
                scatter=reg_scatter,
                ci=reg_ci,
                order=reg_order,
                ax=ax,
            )

    st.pyplot(fig)

    # ---- Show code ----
    with st.expander("🧾 Show code"):
        code_scatter = generate_code("sns.scatterplot", safe, data_var="df")
        st.code(code_scatter, language="python")

        if add_reg:
            st.markdown(
                "**Regression note:** `regplot` doesn’t support `hue`, so we draw one regression per hue group."
            )
            # show a readable regplot snippet
            reg_snip = f"""# Regression line(s)
# If hue is selected, loop each hue group and call regplot
sns.regplot(data=df, x={safe['x']!r}, y={safe['y']!r}, ci={reg_ci}, order={reg_order})
"""
            st.code(reg_snip, language="python")

    # ---- Download plot data ----
    with st.expander("⬇️ Download plot data (CSV)"):
        plot_df = scatterplot_data(
            df=df,
            x=safe["x"],
            y=safe["y"],
            hue=safe.get("hue"),
            size=safe.get("size"),
            style=safe.get("style"),
        )
        st.dataframe(plot_df.head(20))
        st.download_button(
            "📥 Download scatter plot data CSV",
            data=plot_df.to_csv(index=False).encode("utf-8"),
            file_name="scatterplot_data.csv",
            mime="text/csv",
        )
