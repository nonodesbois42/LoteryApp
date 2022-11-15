import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
import utils
import random
import time
import streamlit as st
import utils
import pandas as pd

st.set_page_config(page_title="Visualisation Bénévoles Lutinerie", layout="wide")
utils.center_text(f"<h2>Visualisation Bénévoles Lutinerie</h2>")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # GET DATA
    XLSX_PATH = "sheet.xlsx"
    utils.get_xlsx(XLSX_PATH)
    data = utils.get_and_filter_df(XLSX_PATH)

    # LAYOUT
    slider = st.slider(
        "Minimum number of hours", min_value=0, max_value=int(data.total.max())
    )

    data_with_min = data[data["total"] > slider]
    with st.container():
        left_column, right_column = st.columns((1, 2))
        with left_column:
            st.dataframe(data, use_container_width=True)
        with right_column:
            st.plotly_chart(utils.create_bar_fig(data_with_min))

    st.write("---")

    with st.container():
        utils.center_text(f"<h2>Create a weighted random draw</h2>")
        _, _, centered, _, _ = st.columns(5)
        with centered:
            state = st.button("Click to random draw !")

        if state:
            col1, col2, col3 = st.columns([0.5, 1, 0.5])
            with st.empty():
                for i in range(50):
                    name_choosen = random.choices(
                        data_with_min.index, weights=data_with_min["total"]
                    )
                    utils.center_text(
                        f"<h1>And the winner is ... {name_choosen[0]} !</h1><br><h3>({int(data_with_min.at[name_choosen[0],'total'])} hours)</h3>"
                    )
                    time.sleep(0.1)
            st.balloons()

