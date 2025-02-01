import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Food and Diet Recommendation System!")

st.sidebar.success("Select a recommendation app.")

st.markdown(
    """
    A FOOD and diet recommendation web application using content-based approach with Scikit-Learn, FastAPI and Streamlit.
   
    """
)
