import streamlit as st
import random
import time
import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# Data utilities
@st.cache
def get_xlsx(path):
    # get xlsx
    SPREADSHEET_KEY_ID = "1eAUqZjClxjZh5xiEPFugICr-8ZiD7X5-Nu7iugGwsy4"
    url = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key={}".format(
        SPREADSHEET_KEY_ID
    )
    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)


@st.cache
def get_and_filter_df(path):
    data = pd.read_excel(path)
    # Rename usefull column for convenience purposes
    data.rename({"Bénévoles": "name", "Total": "total"}, axis=1, inplace=True)
    # Drop every row that doesn't have a date on Atelier column
    data = data[data["Atelier"].notna()]
    # Keep only necessary columns
    data = data[["name", "total"]]
    # Drop others unnecessary rows
    data.dropna(inplace=True)
    data.set_index("name", inplace=True)
    data.sort_values(by="total", ascending=False, inplace=True)
    return data

# Layout utilities
def center_text(text: str):
    return st.markdown(f"<center>{text}</center>", unsafe_allow_html=True)

# Plotly figure
def create_bar_fig(df):
    fig = px.bar(df, color_discrete_sequence=["rgb(204,102,119)"])
    fig.update_layout(
        xaxis_title="Name",
        yaxis_title="Amount of hours",
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig