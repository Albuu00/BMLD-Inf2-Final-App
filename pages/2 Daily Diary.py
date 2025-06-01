import pandas as pd
from datetime import datetime
import streamlit as st
from utils.login_manager import LoginManager
from utils.data_manager import DataManager

# ====== Start Login Block ======
LoginManager().go_to_login('Start.py')

# Initialisiere "dailydiary" in st.session_state, falls es nicht existiert
if "dailydiary" not in st.session_state:
    st.session_state.dailydiary = pd.DataFrame(columns=["date", "time", "entry", "satisfaction"])

# Titel der Seite
st.title("My Daily Diary")

# Textfeld für den Nutzer
user_input = st.text_area("Schreibe hier deine Gedanken:", placeholder="Dein Text...")

# Auswahl für Zufriedenheit mit Smileys
satisfaction = st.radio(
    "Wie zufrieden bist du heute mit deinen erledigten To-Dos?",
    options=[" Sehr zufrieden", " Zufrieden", " Neutral", " Unzufrieden", " Sehr unzufrieden"]
)

# Button zum Speichern
if st.button("Speichern"):
    if user_input.strip():  # Überprüfen, ob das Eingabefeld nicht leer ist
        # Daten vorbereiten
        result = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "entry": user_input.strip(),
            "satisfaction": satisfaction  # Zufriedenheit hinzufügen
        }

        # Eintrag speichern
        DataManager().append_record(session_state_key="dailydiary", record_dict=result)
        st.success("Dein Text wurde gespeichert!")
    else:
        st.error("Das Textfeld darf nicht leer sein.")


# Button zum Löschen der Aufgabe
st.subheader("Deine bisherigen Einträge")
try:
    if not st.session_state.dailydiary.empty:
        for index, row in st.session_state.dailydiary.iterrows():
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"**Datum:** {row['date']} **Zeit:** {row['time']}")
                st.markdown(f"> {row['entry']}")
                st.markdown(f"**Zufriedenheit:** {row['satisfaction']}")
            with col2:
                if st.button("🗑️", key=f"delete_{index}"):
                    st.session_state.dailydiary = st.session_state.dailydiary.drop(index).reset_index(drop=True)
                    DataManager().save_data(session_state_key="dailydiary")
                    st.rerun()
            st.markdown("---")
    else:
        st.info("Es gibt noch keine gespeicherten Einträge.")
except Exception as e:
    st.error(f"Fehler beim Anzeigen der Einträge: {e}")


# Navigation zwischen den Seiten
st.markdown("---")  # Trennlinie für bessere Übersicht
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Zurück zu den ToDos"):
        st.switch_page("pages/1 ToDos.py")

with col3:
    if st.button("Weiter zu den Daten"):
        st.switch_page("pages/3 Daten.py")