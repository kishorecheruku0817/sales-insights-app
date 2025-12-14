def generate_code(plot_func: str, params: dict, data_var: str = "df") -> str:
    """
    plot_func: 'sns.barplot', 'sns.lineplot', etc.
    params: filtered params actually passed to seaborn
    """

    def _repr(v):
        if callable(v):
            return v.__name__
        return repr(v)

    lines = [f"{plot_func}("]
    lines.append(f"    data={data_var},")

    for k, v in params.items():
        lines.append(f"    {k}={_repr(v)},")

    lines.append(")")
    return "\n".join(lines)
