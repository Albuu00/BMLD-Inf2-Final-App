import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import streamlit as st

# Datei-Pfad für die To-Do-Daten
file_path = "data.csv"

# Überprüfen, ob die Datei existiert und die richtigen Spalten enthält
if not os.path.exists(file_path):
    # Erstelle eine leere Datei mit den richtigen Spalten
    columns = ["task", "completed", "timestamp"]  # "timestamp" hinzugefügt
    df = pd.DataFrame(columns=columns)
    df.to_csv(file_path, index=False)

# Initialisierung des Data Managers (hier mit Verbindung zu SwitchDrive)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="HealthySync") 

# Laden der Daten
try:
    # Lade die Daten aus der Datei in st.session_state
    if "todos" not in st.session_state:
        st.session_state.todos = pd.read_csv(file_path).to_dict(orient="records")
except ValueError as e:
    st.error(f"Fehler beim Laden der Daten: {e}")
    # Erstelle eine leere Datei, falls sie fehlt oder fehlerhaft ist
    columns = ["task", "completed", "timestamp"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(file_path, index=False)
    st.warning("Eine neue Datei wurde erstellt, da die alte Datei fehlerhaft war.")

# Funktion zum Speichern der Daten
def save_todos():
    df = pd.DataFrame(st.session_state.todos)
    df.to_csv(file_path, index=False)

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

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
        save_todos()  # Speichere die Daten vor dem Wechsel der Seite
        st.switch_page("pages/1 ToDos.py")
with col2:
    if st.button("Daily Diary"):
        save_todos()  # Speichere die Daten vor dem Wechsel der Seite
        st.switch_page("pages/2 Daily Diary.py")
with col3:
    if st.button("Daten"):
        save_todos()  # Speichere die Daten vor dem Wechsel der Seite
        st.switch_page("pages/3 Daten.py")
with col4:
    if st.button("Grafik"):
        save_todos()  # Speichere die Daten vor dem Wechsel der Seite
        st.switch_page("pages/4 Grafik.py")