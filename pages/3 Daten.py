# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Übersicht der To-Dos")

# To-Do-Daten in ein DataFrame umwandeln
if "todos" in st.session_state and st.session_state.todos:
    df = pd.DataFrame(st.session_state.todos)
    # Überprüfen, ob die Spalte "date" existiert
    if "date" not in df.columns:
        df["date"] = datetime.now().strftime("%Y-%m-%d")  # Füge das aktuelle Datum hinzu
    else:
        df["date"] = pd.to_datetime(df["date"])  # Stelle sicher, dass "date" ein Datumsformat hat
else:
    # Initialisiere ein leeres DataFrame mit den erwarteten Spalten
    df = pd.DataFrame(columns=["task", "completed", "date"])

# Zeitraum auswählen
zeitraum = st.selectbox("Zeitraum auswählen:", ["Gesamt", "Woche", "Monat"])

# Daten filtern nach Zeitraum
if zeitraum == "Woche":
    df["period"] = df["date"].dt.to_period("W").dt.start_time
elif zeitraum == "Monat":
    df["period"] = df["date"].dt.to_period("M").dt.start_time
else:
    df["period"] = "Gesamt"

# Gruppieren und zählen
erfüllte = df[df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)
nicht_erfüllte = df[~df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Erfüllte To-Dos anzeigen
st.subheader("✅ Erfüllte To-Dos")
if not erfüllte.empty:
    for period, tasks in erfüllte.iterrows():
        st.markdown(f"**Zeitraum:** {period.strftime('%d.%m.%Y') if period != 'Gesamt' else 'Gesamt'}")
        for task, count in tasks.items():
            st.markdown(f"- {task}: {count}x")
else:
    st.info("Es gibt keine erfüllten To-Dos.")

# Nicht erfüllte To-Dos anzeigen
st.subheader("❌ Nicht erfüllte To-Dos")
if not nicht_erfüllte.empty:
    for period, tasks in nicht_erfüllte.iterrows():
        st.markdown(f"**Zeitraum:** {period.strftime('%d.%m.%Y') if period != 'Gesamt' else 'Gesamt'}")
        for task, count in tasks.items():
            st.markdown(f"- {task}: {count}x")
else:
    st.info("Es gibt keine nicht erfüllten To-Dos.")

# Button zum Speichern der Daten
if st.button("Daten speichern"):
    try:
        # Speichere die Daten in SwitchDrive
        data_manager = DataManager(fs_protocol='webdav', fs_root_folder="HealthySync")
        data_manager.save_app_data(
            session_state_key="todos",
            file_name="todos.csv"
        )
        st.success("Daten wurden erfolgreich in SwitchDrive gespeichert!")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Daten: {e}")

# Bisherige Daten anzeigen
st.subheader("📋 Bisherige To-Dos")
if not df.empty:
    st.dataframe(df)  # Zeigt die Daten in einer interaktiven Tabelle an
else:
    st.info("Es gibt keine gespeicherten To-Dos.")