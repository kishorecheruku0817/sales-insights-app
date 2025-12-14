import json
import numpy as np
import streamlit as st


def noneify(v):
    return None if v in (None, "None", "") else v


def parse_json_dict(text: str, label="JSON"):
    text = (text or "").strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
        if not isinstance(obj, dict):
            st.error(f'{label} must be a JSON object (dict). Example: {{"alpha": 0.6}}')
            return None
        return obj
    except Exception as e:
        st.error(f"Invalid {label}: {e}")
        return None


def estimator_fn(name: str):
    mapping = {
        "mean": np.mean,
        "sum": np.sum,
        "median": np.median,
        "count": len,
        "min": np.min,
        "max": np.max,
    }
    return mapping.get(name, np.mean)


def errorbar_value(kind: str, level: int):
    if kind == "None":
        return None
    if kind in ("sd", "se"):
        return kind
    return (kind, int(level))
