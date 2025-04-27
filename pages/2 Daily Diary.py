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
if st.button("Speichern"):
    with open("daily_diary.txt", "a", encoding="utf-8") as file:
        file.write(user_input + "\n")
    st.success("Dein Text wurde gespeichert!")

    # Speichern des neuen Eintrags
    DataManager().append_record(session_state_key='data_df', record_dict=result)  

# Gespeicherte Einträge anzeigen
st.subheader("Deine bisherigen Einträge")
try:
    # CSV-Datei laden
    file_path = "data.csv"
    if pd.io.common.file_exists(file_path):
        diary_data = pd.read_csv(file_path)
        for index, row in diary_data.iterrows():
            st.markdown(f"**Datum:** {row['date']} **Zeit:** {row['time']}")
            st.markdown(f"> {row['entry']}")
            st.markdown("---")  # Trennlinie zwischen Einträgen
    else:
        st.info("Es gibt noch keine gespeicherten Einträge.")
except Exception as e:
    st.error(f"Fehler beim Laden der Einträge: {e}")