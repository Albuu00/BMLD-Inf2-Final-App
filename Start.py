import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialisierung des Data Managers (hier mit Verbindung zu SwitchDrive)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_DB") 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# Laden der Daten
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )

import streamlit as st

# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

st.title("HealthySync")

# Streamlit über den Text unten direkt in die App - cool!
"""
Diese App wurde von folgenden Personen entwickelt:
- Albulena Ibishi (ibishalb@students.zhaw.ch)
- Simona Flachsmann (flachsim@students.zhaw.ch)
- Aylin Ago (agoayl01@students.zhaw.ch)

Diese App ist ein Todo Reminder.
""" 
if st.button("Todos"):
    st.switch_page("pages/1 ToDos.py")
if st.button("Daily Diary"):
    st.switch_page("pages/2 Daily Diary.py")
if st.button("Daten"):
    st.switch_page("pages/3 Daten.py")
if st.button("Grafik"):
    st.switch_page("pages/4 Grafik.py")