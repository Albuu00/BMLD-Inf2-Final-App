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
if st.session_state.todos:
    df = pd.DataFrame(st.session_state.todos)
    df["date"] = pd.to_datetime(df.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
else:
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

# ✅ Erfüllte To-Dos anzeigen
st.subheader("✅ Erfüllte To-Dos")
if not erfüllte.empty:
    for period, tasks in erfüllte.iterrows():
        st.markdown(f"**Zeitraum:** {period.strftime('%d.%m.%Y') if period != 'Gesamt' else 'Gesamt'}")
        for task, count in tasks.items():
            st.markdown(f"- {task}: {count}x")
else:
    st.info("Es gibt keine erfüllten To-Dos.")

# ❌ Nicht erfüllte To-Dos anzeigen
st.subheader("❌ Nicht erfüllte To-Dos")
if not nicht_erfüllte.empty:
    for period, tasks in nicht_erfüllte.iterrows():
        st.markdown(f"**Zeitraum:** {period.strftime('%d.%m.%Y') if period != 'Gesamt' else 'Gesamt'}")
        for task, count in tasks.items():
            st.markdown(f"- {task}: {count}x")
else:
    st.info("Es gibt keine nicht erfüllten To-Dos.")

# 💾 Button zum Speichern der Daten
if st.button("Daten speichern"):
    try:
        dm = DataManager()

        # Erfüllte speichern
        if not erfüllte.empty:
            for period, tasks in erfüllte.iterrows():
                for task, count in tasks.items():
                    record = {"task": task, "count": count, "period": str(period), "status": "erfüllt"}
                    dm.append_record(session_state_key="daten", record_dict=record)

        # Nicht erfüllte speichern
        if not nicht_erfüllte.empty:
            for period, tasks in nicht_erfüllte.iterrows():
                for task, count in tasks.items():
                    record = {"task": task, "count": count, "period": str(period), "status": "nicht erfüllt"}
                    dm.append_record(session_state_key="daten", record_dict=record)

        st.success("To-Dos wurden erfolgreich gespeichert!")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Daten: {e}")


# Navigation zwischen den Seiten
st.markdown("---")  # Trennlinie für bessere Übersicht
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Zurück zum Daily Diary"):
        st.switch_page("pages/2 Daily Diary.py")

with col3:
    if st.button("Weiter zur Erfolgsübersicht"):
        st.switch_page("pages/4 Erfolgsübersicht.py")