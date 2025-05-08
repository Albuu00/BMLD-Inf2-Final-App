import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Beispiel-Daten (ersetze dies durch deine echten To-Do-Daten)
data = [
    {"task": "2 Liter Wasser trinken", "completed": True, "date": "2025-05-01"},
    {"task": "2 Liter Wasser trinken", "completed": False, "date": "2025-05-02"},
    {"task": "Spazieren", "completed": True, "date": "2025-05-03"},
    {"task": "Spazieren", "completed": True, "date": "2025-05-04"},
    {"task": "10 Minuten Dehnen", "completed": False, "date": "2025-05-05"},
    {"task": "10 Minuten Dehnen", "completed": True, "date": "2025-05-06"},
    {"task": "Mindestens eine Frucht gegessen", "completed": True, "date": "2025-05-07"},
    {"task": "Mindestens eine Frucht gegessen", "completed": False, "date": "2025-05-08"},
]

# Daten in ein DataFrame laden
df = pd.DataFrame(data)

# Datum in datetime umwandeln und Woche extrahieren
df["date"] = pd.to_datetime(df["date"])
df["week"] = df["date"].dt.strftime("%Y-%U")  # Jahr-Woche Format

# Streamlit-Filter für die Dauer
duration = st.selectbox("Zeitraum auswählen:", ["pro Woche", "pro Monat"])

if duration == "pro Monat":
    df["period"] = df["date"].dt.to_period("M").dt.start_time  # Monat als Startdatum
else:
    df["period"] = df["date"].dt.to_period("W").dt.start_time  # Woche als Startdatum

# Gruppieren und zählen: Erfüllte To-Dos
completed = df[df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Gruppieren und zählen: Nicht erfüllte To-Dos
not_completed = df[~df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Diagramm für erfüllte To-Dos
st.subheader("Erfüllte To-Dos")
fig, ax = plt.subplots(figsize=(10, 6))
for task in completed.columns:
    ax.plot(completed.index, completed[task], label=task, marker="o")
ax.set_title("Erfüllte To-Dos pro Zeitraum")
ax.set_xlabel("Zeitraum")
ax.set_ylabel("Anzahl erfüllt")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ganze Zahlen auf der Y-Achse
ax.set_xticks(completed.index)
ax.set_xticklabels(completed.index.strftime("%d.%m.%y"), rotation=45)  # X-Achse formatieren
ax.legend()
st.pyplot(fig)

# Diagramm für nicht erfüllte To-Dos
st.subheader("Nicht erfüllte To-Dos")
fig, ax = plt.subplots(figsize=(10, 6))
for task in not_completed.columns:
    ax.plot(not_completed.index, not_completed[task], label=task, marker="o")
ax.set_title("Nicht erfüllte To-Dos pro Zeitraum")
ax.set_xlabel("Zeitraum")
ax.set_ylabel("Anzahl nicht erfüllt")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ganze Zahlen auf der Y-Achse
ax.set_xticks(not_completed.index)
ax.set_xticklabels(not_completed.index.strftime("%d.%m.%y"), rotation=45)  # X-Achse formatieren
ax.legend()
st.pyplot(fig)