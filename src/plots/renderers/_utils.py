def filter_params(params: dict, allowed: set[str]) -> dict:
    """
    Keep only keys supported by a given seaborn plot.
    (Also drops None values so seaborn/matplotlib don't get weird params.)
    """
    return {k: v for k, v in params.items() if k in allowed and v is not None}
