import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Sicherstellen, dass die Daten in st.session_state vorhanden sind
if "todos" not in st.session_state or not st.session_state["todos"]:
    st.info("Keine To-Do-Daten verfügbar. Bitte fügen Sie To-Dos auf der Startseite hinzu.")
    st.stop()

# Daten aus der Datei `to_do.csv` laden und mit den aktuellen To-Dos kombinieren
file_path = "to_do.csv"
if "todos" in st.session_state:
    current_todos = pd.DataFrame(st.session_state["todos"])
else:
    current_todos = pd.DataFrame(columns=["task", "completed", "date"])

# Prüfen, ob die Datei existiert
try:
    if pd.io.common.file_exists(file_path):
        saved_todos = pd.read_csv(file_path)
    else:
        saved_todos = pd.DataFrame(columns=["task", "completed", "date"])
except Exception as e:
    st.error(f"Fehler beim Laden der Datei: {e}")
    saved_todos = pd.DataFrame(columns=["task", "completed", "date"])

# Kombinieren der aktuellen und gespeicherten To-Dos
combined_todos = pd.concat([saved_todos, current_todos], ignore_index=True)

# Duplikate entfernen (basierend auf `task` und `date`)
combined_todos = combined_todos.drop_duplicates(subset=["task", "date"], keep="last")

# Sicherstellen, dass die Datei aktualisiert wird
combined_todos.to_csv(file_path, index=False)

# Daten in ein DataFrame laden
df = combined_todos

# Überprüfen, ob die notwendigen Spalten vorhanden sind
required_columns = {"task", "completed", "date"}
if not required_columns.issubset(df.columns):
    st.error(f"Die To-Do-Daten müssen die folgenden Spalten enthalten: {', '.join(required_columns)}")
    st.stop()

# Spalte "date" in datetime umwandeln
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])  # Ungültige Datumswerte entfernen

# Sicherstellen, dass die Spalte 'completed' boolesche Werte enthält
if df["completed"].dtype != bool:
    df["completed"] = df["completed"].astype(bool)

# Zeitraum-Auswahl
duration = st.selectbox("Zeitraum auswählen:", ["pro Woche", "pro Monat"])

# Zeitraum berechnen
if duration == "pro Monat":
    df["period"] = df["date"].dt.to_period("M").dt.start_time  # Monat als Startdatum
else:
    df["period"] = df["date"].dt.to_period("W").dt.start_time  # Woche als Startdatum


# Gruppieren und zählen: Erfüllte To-Dos
completed = df[df["completed"]].groupby(["period", "task"]).size().unstack(fill_value=0)

# Sicherstellen, dass die Werte ganze Zahlen sind
completed = completed.astype(int)

# Summieren der To-Dos über den Zeitraum
completed_sum = completed.groupby(level=0).sum()  # Summiere alle erfüllten To-Dos pro Zeitraum

# Diagramm für erfüllte To-Dos als Säulendiagramm erstellen
st.subheader("✅ Erfüllte To-Dos")
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Breite der Säulen und Abstand
bar_width = 0.3  # Breite der Säulen
spacing = 0.4  # Abstand zwischen den Säulen
x_positions = range(len(completed.index))  # Positionen der Zeiträume auf der X-Achse

# Jede Aufgabe einzeln plotten
colors = plt.cm.tab10.colors  # Farbpalette
tasks = completed.columns  # Liste der Aufgaben
for i, task in enumerate(tasks):
    ax1.bar(
        [x + i * (bar_width + spacing) for x in x_positions],  # Verschiebe jede Säule um die Breite + Abstand
        completed[task],  # Anzahl der erledigten To-Dos für die Aufgabe
        width=bar_width,
        label=task,
        color=colors[i % len(colors)]  # Zyklische Farbzuweisung
    )

# Diagramm formatieren
ax1.set_title("Erfüllte To-Dos pro Zeitraum")
ax1.set_xlabel("Zeitraum")
ax1.set_ylabel("Anzahl")
ax1.set_xticks([x + (len(tasks) * (bar_width + spacing) - spacing) / 2 for x in x_positions])  # Zentriere die Labels
ax1.set_xticklabels(completed.index.strftime("%d.%m.%y"), rotation=45)  # Zeiträume als Labels
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ganze Zahlen auf der Y-Achse
ax1.legend(title="Aufgaben")  # Legende mit Titel
st.pyplot(fig1)


# Navigation zwischen den Seiten
st.markdown("---")  # Trennlinie für bessere Übersicht
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Zurück zu den Daten"):
        st.switch_page("pages/3 Daten.py")

with col3:
    if st.button("Zurück zur Startseite"):
        st.switch_page("Start.py")