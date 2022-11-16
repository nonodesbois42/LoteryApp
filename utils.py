import streamlit as st

# Layout utilities
def center_text(text: str):
    return st.markdown(f"<center>{text}</center>", unsafe_allow_html=True)
