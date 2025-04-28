import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialisierung des Data Managers (hier mit Verbindung zu SwitchDrive)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="HealthySync") 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# Erstelle eine leere Datei mit den richtigen Spalten
columns = ["task", "completed", "timestamp"]
df = pd.DataFrame(columns=columns)
df.to_csv("data.csv", index=False)
import streamlit as st

# Laden der Daten
data_manager.load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )
except ValueError as e:
    st.error(f"Fehler beim Laden der Daten: {e}")
    # Erstelle eine leere Datei, falls sie fehlt
    df = pd.DataFrame(columns=["task", "completed", "timestamp"])
    df.to_csv("data.csv", index=False)
# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

st.markdown("<h1 style='color:turquoise;'>HealthySync</h1>", unsafe_allow_html=True)

# Streamlit über den Text unten direkt in die App - cool!
"""
Autoren:
- Albulena Ibishi (ibishalb@students.zhaw.ch)
- Simona Flachsmann (flachsim@students.zhaw.ch)
- Aylin Ago (agoayl01@students.zhaw.ch)

Diese App ist ein Todo Reminder.
""" 
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
    if st.button("Grafik"):
        st.switch_page("pages/4 Grafik.py")