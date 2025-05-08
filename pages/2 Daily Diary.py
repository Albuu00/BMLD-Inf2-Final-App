import pandas as pd
from datetime import datetime
# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======
import streamlit as st

# Datei-Pfad für die CSV-Datei
file_path = "data.csv"

# Überprüfen, ob die Datei existiert, und initialisieren
try:
    if pd.io.common.file_exists(file_path):
        diary_data = pd.read_csv(file_path, encoding="utf-8")  # CSV-Datei laden
    else:
        # Falls die Datei nicht existiert, initialisiere ein leeres DataFrame
        diary_data = pd.DataFrame(columns=["date", "time", "entry", "satisfaction"])
except Exception as e:
    st.error(f"Fehler beim Laden der Datei: {e}")

# Titel der App
st.title("My Daily Diary")

# Textfeld für den Nutzer
user_input = st.text_area("Schreibe hier deine Gedanken:", placeholder="Dein Text...")

# Auswahl für Zufriedenheit mit Smileys
satisfaction = st.radio(
    "Wie zufrieden bist du heute mit deinen erledigten To-Dos?",
    options=["😃 Sehr zufrieden", "🙂 Zufrieden", "😐 Neutral", "☹️ Unzufrieden", "😢 Sehr unzufrieden"]
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

        # Speichern in einer Textdatei (optional, falls benötigt)
        with open("daily_diary.txt", "a", encoding="utf-8") as file:
            file.write(f"{result['date']} {result['time']} - {result['entry']} ({result['satisfaction']})\n")

        # Speichern in die CSV-Datei
        new_row = pd.DataFrame([result])  # Neuen Eintrag als DataFrame erstellen
        diary_data = pd.concat([diary_data, new_row], ignore_index=True)  # Zeile hinzufügen
        diary_data.to_csv(file_path, index=False, encoding="utf-8")  # CSV-Datei speichern

        st.success("Dein Text wurde gespeichert!")
    else:
        st.error("Das Textfeld darf nicht leer sein.")

# Gespeicherte Einträge anzeigen
st.subheader("Deine bisherigen Einträge")
try:
    if not diary_data.empty:
        for index, row in diary_data.iterrows():
            st.markdown(f"**Datum:** {row['date']} **Zeit:** {row['time']}")
            st.markdown(f"> {row['entry']}")
            st.markdown("---")  # Trennlinie zwischen Einträgen
    else:
        st.info("Es gibt noch keine gespeicherten Einträge.")
except Exception as e:
    st.error(f"Fehler beim Anzeigen der Einträge: {e}")