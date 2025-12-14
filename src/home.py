import streamlit as st

def home():
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