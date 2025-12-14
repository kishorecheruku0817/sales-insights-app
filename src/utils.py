import streamlit as st

def render_footer():
  st.markdown(
      """
      <hr>
      <div style="text-align:center; font-size: 0.9rem; color: #777;">
          Built with <b>Passion</b> using Python & Streamlit · <b>By Kishore</b>
      </div>
      """,
      unsafe_allow_html=True,
  )

def side_bar():
  with st.sidebar:
    st.title("📊 CSV Cleaner App")
    page = st.radio(
        "Go to",
        ["Home", "Upload & Clean", "Insights"]  # note spacing
    )
  return page