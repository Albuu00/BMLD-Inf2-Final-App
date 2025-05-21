import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Beispiel-Daten (ersetze dies durch deine echten To-Do-Daten)
#data = [
    #{"task": "2 Liter Wasser trinken", "completed": True, "date": "2025-05-01"},
    #{"task": "2 Liter Wasser trinken", "completed": False, "date": "2025-05-02"},
    #{"task": "Spazieren", "completed": True, "date": "2025-05-03"},
    #{"task": "Spazieren", "completed": True, "date": "2025-05-04"},
    #{"task": "10 Minuten Dehnen", "completed": False, "date": "2025-05-05"},
    #{"task": "10 Minuten Dehnen", "completed": True, "date": "2025-05-06"},
    #{"task": "Mindestens eine Frucht gegessen", "completed": True, "date": "2025-05-07"},
    #{"task": "Mindestens eine Frucht gegessen", "completed": False, "date": "2025-05-08"},
#]

#df = pd.DataFrame(data)

# Sicherstellen, dass st.session_state.todos initialisiert ist
if "todos" not in st.session_state or not st.session_state.todos:
    st.error("Keine To-Do-Daten verfügbar. Bitte füge zuerst To-Dos hinzu.")
    st.stop()

# Daten aus st.session_state.todos laden
df = pd.DataFrame(st.session_state.todos)

# Überprüfen, ob die notwendigen Spalten vorhanden sind
required_columns = {"task", "completed", "timestamp"}
if not required_columns.issubset(df.columns):
    st.error(f"Die To-Do-Daten müssen die folgenden Spalten enthalten: {', '.join(required_columns)}")
    st.stop()

# Datum aus dem Zeitstempel extrahieren
df["date"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.date
df = df.dropna(subset=["date"])  # Ungültige Datumswerte entfernen

# Zeitraum-Auswahl
duration = st.selectbox("Zeitraum auswählen:", ["pro Woche", "pro Monat"])

# Zeitraum berechnen
if duration == "pro Monat":
    df["period"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.start_time  # Monat als Startdatum
else:
    df["period"] = pd.to_datetime(df["date"]).dt.to_period("W").dt.start_time  # Woche als Startdatum

# Gruppieren und zählen: Erfüllte und nicht erfüllte To-Dos
completed = df[df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)
not_completed = df[~df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Diagramm erstellen
st.subheader("To-Do Übersicht")
fig, ax = plt.subplots(figsize=(12, 6))

# Erfüllte To-Dos plotten
for task in completed.columns:
    ax.plot(completed.index, completed[task], label=f"{task} (erfüllt)", marker="o")

# Nicht erfüllte To-Dos plotten
for task in not_completed.columns:
    ax.plot(not_completed.index, not_completed[task], label=f"{task} (nicht erfüllt)", linestyle="--", marker="x")

# Diagramm formatieren
ax.set_title("To-Do Übersicht pro Zeitraum")
ax.set_xlabel("Zeitraum")
ax.set_ylabel("Anzahl")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ganze Zahlen auf der Y-Achse
ax.set_xticks(completed.index)
ax.set_xticklabels(completed.index.strftime("%d.%m.%y"), rotation=45)  # X-Achse formatieren
ax.legend()  # Legende hinzufügen
st.pyplot(fig)