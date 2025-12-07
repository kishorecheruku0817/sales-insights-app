import io
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="CSV Cleaner & Sales Insights",
    layout="wide",
)

with st.sidebar:
    st.title("📊 CSV Cleaner App")
    page = st.radio(
        "Go to",
        ["Home", "Upload & Clean", "Insights (coming soon)"]  # note spacing
    )

if page == "Home":
    st.title("📊 CSV Cleaner & Sales Insights (v0.1)")
    st.write(
        "Upload your CSV, clean missing values, and download a cleaned file. "
        "Later we'll add detailed sales analysis and Seaborn visualizations."
    )

    st.markdown("""
    ### What this app does
    - ✅ Upload any CSV
    - ✅ Clean missing values (NaNs)
    - ✅ Download a cleaned version
    - 📈 Soon: visual insights using Seaborn
    """)

    st.subheader("Download Sample CSV to test")

    col1, col2, col3 = st.columns([3, 3, 1])
    with col3:
        with open("data/sales_complex_dirty.csv", "rb") as f:
            st.download_button(
                label="📥 Download sample CSV",
                data=f,
                file_name="sales_complex_dirty.csv",
                mime="text/csv",
            )

elif page == "Upload & Clean":
    st.title("📤 Upload & Clean Your CSV")
    st.write("Upload your CSV, choose cleaning options, and download a cleaned file.")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

        st.subheader("👀 Preview of your data! you can see only 5 rows")
        st.dataframe(df.head())

        st.subheader("📏 Basic info")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
            st.write("**Dtypes:**")
            st.write(df.dtypes.to_frame("dtype"))

        with col2:
            st.write("**NaN counts per column:**")
            st.write(df.isna().sum().to_frame("NaN_count"))

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

        st.subheader("🧹 Cleaning options")

        st.markdown("**Global options**")
        drop_all_na_rows = st.checkbox("Drop rows where all columns are NaN", value=True)
        drop_any_na_rows = st.checkbox("Drop rows with ANY NaN value", value=False)
        drop_duplicates = st.checkbox("Drop duplicate rows", value=True)

        st.markdown("**Numeric columns (int/float)**")
        fill_numeric_zero = st.checkbox(
            "Fill NaNs in numeric columns with 0", value=True, disabled=drop_any_na_rows
        )

        st.markdown("**Text / categorical columns**")
        fill_cat_unknown = st.checkbox(
            "Fill NaNs in text columns with 'Unknown'", value=True, disabled=drop_any_na_rows
        )

        if st.button("🚀 Clean my data"):
            df_cleaned = df.copy()
            rows_before = df_cleaned.shape[0]

            # 1) Drop all-NaN rows
            if drop_all_na_rows:
                df_cleaned = df_cleaned.dropna(how="all")

            # 2) Either drop any-NaN rows OR fill NaNs
            if drop_any_na_rows:
                df_cleaned = df_cleaned.dropna(how="any")
            else:
                if fill_numeric_zero and numeric_cols:
                    df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(0)
                if fill_cat_unknown and cat_cols:
                    df_cleaned[cat_cols] = df_cleaned[cat_cols].fillna("Unknown")

            # 3) Drop duplicates
            if drop_duplicates:
                df_cleaned = df_cleaned.drop_duplicates()

            rows_after = df_cleaned.shape[0]

            st.success(
                f"✅ Cleaning done! Rows before: {rows_before}, after: {rows_after} "
                f"(removed {rows_before - rows_after} rows)."
            )

            st.subheader("🔍 Preview of cleaned data")
            st.dataframe(df_cleaned.head())

            st.subheader("📊 NaN summary after cleaning")
            st.write(df_cleaned.isna().sum().to_frame("NaN_count"))

            csv_buffer = io.StringIO()
            df_cleaned.to_csv(csv_buffer, index=False)
            cleaned_csv_bytes = csv_buffer.getvalue().encode("utf-8")

            st.download_button(
                "📥 Download cleaned CSV",
                cleaned_csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv",
            )

            st.info(
                "Next steps: we'll add a 'Generate Insights' section here "
                "with Seaborn charts and business metrics."
            )
    else:
        st.info("Please upload a CSV file to get started.")

elif page == "Insights (coming soon)":
    st.title("📈 Insights Dashboard")
    st.info("We’ll build the Seaborn-based insights dashboard here next.")
