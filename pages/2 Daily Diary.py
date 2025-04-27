import pandas as pd
from datetime import datetime
# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======
import streamlit as st

# Titel der App
st.title("My Daily Diary")
import requests

# Textfeld für den Nutzer
user_input = st.text_area("Schreibe hier deine Gedanken:", placeholder="Dein Text...")

# Button zum Speichern
#if st.button("Speichern"):
    #with open("daily_diary.txt", "a", encoding="utf-8") as file:
        #file.write(user_input + "\n")
    #st.success("Dein Text wurde gespeichert!")

# Button zum Speichern
if st.button("Speichern"):
    if user_input.strip():  # Überprüfen, ob das Eingabefeld nicht leer ist
        # Daten vorbereiten
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "entry": user_input.strip()
        }

        # Daten in eine CSV-Datei speichern
        file_path = "daily_diary.csv"
        try:
            # Überprüfen, ob die Datei existiert
            if not pd.io.common.file_exists(file_path):
                # Neue Datei erstellen und Daten speichern
                df = pd.DataFrame([entry])
                df.to_csv(file_path, index=False)
            else:
                # Daten an bestehende Datei anhängen
                df = pd.read_csv(file_path)
                df = df.append(entry, ignore_index=True)
                df.to_csv(file_path, index=False)

            st.success("Dein Eintrag wurde gespeichert!")
        except Exception as e:
            st.error(f"Fehler beim Speichern: {e}")
    else:
        st.error("Das Textfeld darf nicht leer sein.")