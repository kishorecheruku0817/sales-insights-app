# app.py
import numpy as np
import pandas as pd
import streamlit as st

from src.insights import render_insights


st.set_page_config(page_title="CSV Cleaner & Sales Insights", layout="wide")


# ---------------- Helpers ----------------
def read_csv(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()


def dataframe_preview(df, title="Preview (first 10 rows)"):
    st.subheader(title)
    st.dataframe(df.head(10))


# ---------------- Sidebar Navigation ----------------
with st.sidebar:
    st.title("📊 CSV Cleaner App")
    page = st.radio("Go to", ["Home", "Upload & Clean", "Insights"])


# ---------------- Home ----------------
if page == "Home":
    st.title("📊 CSV Cleaner & Sales Insights (v0.1)")
    st.write("Download a sample CSV, upload your file, clean it, and generate plots.")

    st.subheader("Download Sample CSV to test")
    col1, col2, col3 = st.columns([3, 3, 1])
    with col3:
        # Ensure this file exists in your repo at: data/sales_complex_dirty_v2.csv
        try:
            with open("data/sales_complex_dirty_v2.csv", "rb") as f:
                st.download_button(
                    label="📥 Download sample CSV",
                    data=f,
                    file_name="sales_complex_dirty_v2.csv",
                    mime="text/csv",
                )
        except FileNotFoundError:
            st.warning("Sample CSV not found at data/sales_complex_dirty_v2.csv")


# ---------------- Upload & Clean ----------------
elif page == "Upload & Clean":
    st.title("📤 Upload & Clean Your CSV")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is None:
        st.info("Please upload a CSV file to get started.")
    else:
        df = read_csv(uploaded_file)

        dataframe_preview(df, "👀 Preview (first 10 rows)")

        st.subheader("📏 Basic info")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
            st.write("**Dtypes:**")
            st.write(df.dtypes.to_frame("dtype"))
        with c2:
            st.write("**NaN counts per column:**")
            st.write(df.isna().sum().to_frame("NaN_count"))

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

        st.subheader("🧹 Cleaning options")
        drop_all_na_rows = st.checkbox(
            "Drop rows where all columns are NaN", value=True
        )
        drop_any_na_rows = st.checkbox("Drop rows with ANY NaN value", value=False)
        drop_duplicates = st.checkbox("Drop duplicate rows", value=True)

        fill_numeric_zero = st.checkbox(
            "Fill NaNs in numeric columns with 0", value=True, disabled=drop_any_na_rows
        )
        fill_cat_unknown = st.checkbox(
            "Fill NaNs in text columns with 'Unknown'",
            value=True,
            disabled=drop_any_na_rows,
        )

        if st.button("🚀 Clean my data"):
            df_cleaned = df.copy()
            rows_before = df_cleaned.shape[0]

            if drop_all_na_rows:
                df_cleaned = df_cleaned.dropna(how="all")

            if drop_any_na_rows:
                df_cleaned = df_cleaned.dropna(how="any")
            else:
                if fill_numeric_zero and numeric_cols:
                    df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(0)

                if fill_cat_unknown and cat_cols:
                    df_cleaned[cat_cols] = df_cleaned[cat_cols].fillna("Unknown")

            if drop_duplicates:
                df_cleaned = df_cleaned.drop_duplicates()

            rows_after = df_cleaned.shape[0]
            st.success(
                f"✅ Cleaning done! Rows before: {rows_before}, after: {rows_after} "
                f"(removed {rows_before - rows_after} rows)."
            )

            dataframe_preview(df_cleaned, "🔍 Cleaned preview (first 10 rows)")

            st.subheader("📊 NaN summary after cleaning")
            st.write(df_cleaned.isna().sum().to_frame("NaN_count"))

            csv_bytes = df_cleaned.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download cleaned CSV",
                csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv",
            )


# ---------------- Insights (delegated to insights.py) ----------------
elif page == "Insights":
    uploaded_file = st.file_uploader(
        "Upload CSV for insights",
        type=["csv"],
        key="insights_uploader",
    )

    if uploaded_file is None:
        st.info("Upload a CSV to generate plots. You can use the sample CSV from Home.")
    else:
        df = read_csv(uploaded_file)
        render_insights(df)
