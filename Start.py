import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import streamlit as st


# # Überprüfen, ob die Datei existiert und die richtigen Spalten enthält
# file_path = "data.csv"
# if not os.path.exists(file_path):
#     # Erstelle eine leere Datei mit den richtigen Spalten
#     columns = ["task", "completed"]  # Falls du "current_time" verwenden möchtest, ersetze "timestamp" durch "current_time"
#     df = pd.DataFrame(columns=columns)
#     df.to_csv(file_path, index=False)

# Initialisierung des Data Managers (hier mit Verbindung zu SwitchDrive)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="HealthySync") 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page
#  Laden der Daten
#try:
# data_manager.load_user_data(
#     session_state_key='data_df', 
#     file_name='data.csv', 
#     initial_value=pd.DataFrame(),  # Passe hier "timestamp" an, falls du "current_time" verwendest
# )

data_manager.load_user_data(
    session_state_key="todos",
    file_name="to_do.csv",
    initial_value=pd.DataFrame()
)
# except ValueError as e:
#     st.error(f"Fehler beim Laden der Daten: {e}")
#     # Erstelle eine leere Datei, falls sie fehlt oder fehlerhaft ist
#     columns = ["task", "completed"]  # Passe hier "timestamp" an, falls du "current_time" verwendest
#     df = pd.DataFrame(columns=columns)
#     df.to_csv("data.csv", index=False)
#     st.warning("Eine neue Datei wurde erstellt, da die alte Datei fehlerhaft war.")



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