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

    # Spalte "date" prüfen und Datumsformat sicherstellen
    if "date" not in df.columns:
        df["date"] = datetime.now().strftime("%Y-%m-%d")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        st.warning("Keine gültigen Datumseinträge vorhanden. Es können keine To-Dos angezeigt werden.")
        st.stop()
else:
    df = pd.DataFrame(columns=["task", "completed", "date"])

# Zeitraum-Auswahl
zeitraum = st.selectbox("Zeitraum auswählen:", ["Gesamt", "Woche", "Monat"])

# Zeitraum-Spalte berechnen
if zeitraum == "Woche":
    df["period"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)  # Startdatum der Woche
elif zeitraum == "Monat":
    df["period"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)  # Startdatum des Monats
else:
    df["period"] = "Gesamt"

# Gruppieren nach Erfüllungsstatus
erfüllte = df[df["completed"] == True].groupby(["period", "task"]).size().unstack(fill_value=0)
nicht_erfüllte = df[df["completed"] == False].groupby(["period", "task"]).size().unstack(fill_value=0)

# ✅ Erfüllte To-Dos anzeigen
st.subheader("✅ Erfüllte To-Dos")
if not erfüllte.empty:
    for period, tasks in erfüllte.iterrows():
        zeitraum_label = period.strftime('%d.%m.%Y') if period != "Gesamt" else "Gesamt"
        st.markdown(f"**Zeitraum:** {zeitraum_label}")
        for task, count in tasks.items():
            st.markdown(f"- {task}: {count}x")
else:
    st.info("Es gibt keine erfüllten To-Dos.")

# ❌ Nicht erfüllte To-Dos anzeigen
st.subheader("❌ Nicht erfüllte To-Dos")
if not nicht_erfüllte.empty:
    for period, tasks in nicht_erfüllte.iterrows():
        zeitraum_label = period.strftime('%d.%m.%Y') if period != "Gesamt" else "Gesamt"
        st.markdown(f"**Zeitraum:** {zeitraum_label}")
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
        st.switch_page("pages/4 Grafik.py")