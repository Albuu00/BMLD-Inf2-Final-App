import pandas as pd
import os
import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialisierung des Data Managers (hier mit Verbindung zu SwitchDrive)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="HealthySync") 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page
#  Laden der Daten
data_manager.load_user_data(
    session_state_key="todos",
    file_name="to_do.csv",
    initial_value=pd.DataFrame()
)

data_manager.load_user_data(
    session_state_key="dailydiary",
    file_name="daily_diary.csv",
    initial_value=pd.DataFrame()
)

data_manager.load_user_data(
    session_state_key="daten",
    file_name="daten.csv",
    initial_value=pd.DataFrame()
)

# Titel der Anwendung
st.markdown("<h1 style='color:turquoise;'>HealthySync</h1>", unsafe_allow_html=True)
st.markdown("""HealthySync ist ein Todo Reminder, der dir hilft, deine täglichen Aufgaben zu organisieren und zu verfolgen.""")

# Autoren und Beschreibung
st.markdown("""
### Autoren:
- **Albulena Ibishi** (ibishalb@students.zhaw.ch)
- **Simona Flachsmann** (flachsim@students.zhaw.ch)
- **Aylin Ago** (agoayl01@students.zhaw.ch)

""")

# Buttons nebeneinander anzeigen
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Todos"):
        st.switch_page("pages/1 ToDos.py")
with col2:
    if st.button("Daily Diary"):
        st.switch_page("pages/2 Daily Diary.py")
with col3:
    if st.button("Daten"):
        st.switch_page("pages/3 Daten.py")
with col4:
    if st.button("Erfolgsübersicht"):
        st.switch_page("pages/4 Grafik.py")