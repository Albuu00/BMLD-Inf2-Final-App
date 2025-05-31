import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Sicherstellen, dass die Daten in st.session_state vorhanden sind
if "todos" not in st.session_state or not st.session_state["todos"]:
    st.info("Keine To-Do-Daten verfügbar. Bitte fügen Sie To-Dos auf der Startseite hinzu.")
    st.stop()

# Daten aus st.session_state laden
data = st.session_state["todos"]
df = pd.DataFrame(data)

# Überprüfen, ob die notwendigen Spalten vorhanden sind
required_columns = {"task", "completed", "date"}
if not required_columns.issubset(df.columns):
    st.error(f"Die To-Do-Daten müssen die folgenden Spalten enthalten: {', '.join(required_columns)}")
    st.stop()

# Spalte "date" in datetime umwandeln
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])  # Ungültige Datumswerte entfernen

# Zeitraum-Auswahl
duration = st.selectbox("Zeitraum auswählen:", ["pro Woche", "pro Monat"])

# Zeitraum berechnen
if duration == "pro Monat":
    df["period"] = df["date"].dt.to_period("M").dt.start_time  # Monat als Startdatum

else:
    df["period"] = df["date"].dt.to_period("W").dt.start_time  # Woche als Startdatum


# Gruppieren und zählen: Erfüllte und nicht erfüllte To-Dos
completed = df[df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)
not_completed = df[~df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Sicherstellen, dass die Werte ganze Zahlen sind
completed = completed.astype(int)
not_completed = not_completed.astype(int)

# Summieren der To-Dos über den Zeitraum
completed_sum = completed.groupby(level=0).sum()  # Summiere alle erfüllten To-Dos pro Zeitraum
not_completed_sum = not_completed.groupby(level=0).sum()  # Summiere alle nicht erfüllten To-Dos pro Zeitraum

# Diagramm erstellen
st.subheader("Erfolgsübersicht")
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

# Y-Achse auf ganze Zahlen beschränken
ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ganze Zahlen auf der Y-Achse

# Sicherstellen, dass die Y-Achse keine Dezimalzahlen anzeigt
ax.set_ylim(bottom=0)  # Setzt den unteren Grenzwert der Y-Achse auf 0
ax.yaxis.get_major_locator().set_params(integer=True)  # Erzwingt ganze Zahlen auf der Y-Achse

# X-Achse formatieren
ax.set_xticks(completed.index.union(not_completed.index))  # Alle Zeiträume anzeigen
ax.set_xticklabels(completed.index.union(not_completed.index).strftime("%d.%m.%y"), rotation=45)

# Legende hinzufügen
ax.legend()  
st.pyplot(fig)

# Navigation zwischen den Seiten
st.markdown("---")  # Trennlinie für bessere Übersicht
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Zurück zu den Daten)"):
        st.switch_page("pages/3 Daten.py")

with col3:
    if st.button("Zurück zur Startseite"):
        st.switch_page("Start.py")