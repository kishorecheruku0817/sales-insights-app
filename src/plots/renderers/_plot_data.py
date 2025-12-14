import pandas as pd


def barplot_data(
    df: pd.DataFrame,
    x: str,
    y: str | None,
    hue: str | None,
    estimator_name: str = "mean",
):
    d = df.copy()
    print(x)
    print(y)
    print(hue)
    print(estimator_name)
    cols = [c for c in [x, y, hue] if c is not None]
    d = d.dropna(subset=[c for c in cols if c is not None])

    print(cols)
    print(d)
    if y is None:
        # Count mode
        if hue:
            out = d.groupby([x, hue]).size().reset_index(name="count")
        else:
            out = d.groupby([x]).size().reset_index(name="count")
        return out

    # Aggregation mode
    agg_map = {
        "mean": "mean",
        "sum": "sum",
        "median": "median",
        "len": "count",
        "min": "min",
        "max": "max",
    }
    agg = agg_map.get(str(estimator_name.__name__), "mean")

    if hue:
        out = (
            d.groupby([x, hue], dropna=True)[y].agg(agg).reset_index(name=f"{agg}_{y}")
        )
    else:
        out = d.groupby([x], dropna=True)[y].agg(agg).reset_index(name=f"{agg}_{y}")

    return out


def lineplot_data(
    df: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None,
    estimator_name: str = "mean",
):
    d = df.copy()
    cols = [x, y] + ([hue] if hue else [])
    d = d.dropna(subset=[c for c in cols if c is not None])
    out = df[cols].dropna()

    # Aggregation mode
    agg_map = {
        "mean": "mean",
        "sum": "sum",
        "median": "median",
        "len": "count",
        "min": "min",
        "max": "max",
    }
    print("-----")
    print(estimator_name.__name__)
    agg = agg_map.get(str(estimator_name.__name__), "mean")

    if hue:
        out = (
            d.groupby([x, hue], dropna=True)[y].agg(agg).reset_index(name=f"{agg}_{y}")
        )
    else:
        out = d.groupby([x], dropna=True)[y].agg(agg).reset_index(name=f"{agg}_{y}")

    return out


def boxplot_data(df: pd.DataFrame, x: str, y: str, hue: str | None):
    cols = [x, y] + ([hue] if hue else [])
    out = df[cols].dropna()
    return out
