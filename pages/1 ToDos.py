from datetime import datetime
# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st

# Initiale To-Do-Liste
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"task": "2 Liter Wasser trinken", "completed": False},
        {"task": "Spazieren", "completed": False},
        {"task": "10 Minuten Dehnen", "completed": False},
        {"task": "Mindestens eine Frucht gegessen", "completed": False},
        {"task": "Mindestens ein Gemüse gegessen", "completed": False},
        {"task": "7 bis 8 Stunden geschlafen", "completed": False},
        {"task": "Etwas aufräumen oder putzen", "completed": False},
        {"task": "Mindestens eine Stunde Handypause", "completed": False}
    ]

# Aktuelles Datum, Wochentag und Uhrzeit
current_time = datetime.now().strftime("%A, %d. %B %Y, %H:%M:%S")

# Titel der Seite mit Datum und Zeit
st.title(f"To-Do Liste  |  {current_time}")

# Funktion zum Abhaken von Aufgaben
def toggle_task(index):
    st.session_state.todos[index]["completed"] = not st.session_state.todos[index]["completed"]

# To-Do-Liste anzeigen
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        # Checkbox zum Abhaken
        if st.checkbox("", value=todo["completed"], key=f"todo_{i}"):
            toggle_task(i)
    with col2:
        # Aufgabe anzeigen (grau, wenn abgehakt)
        if todo["completed"]:
            st.markdown(f"<span style='color: gray; text-decoration: line-through;'>{todo['task']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(todo["task"])