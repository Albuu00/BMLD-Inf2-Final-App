from datetime import datetime
# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Beispiel-Daten (du kannst diese durch deine echten Daten ersetzen)
if "todos_data" not in st.session_state:
    st.session_state.todos_data = pd.DataFrame({
        "task": ["2 Liter Wasser trinken", "Spazieren", "Einkaufen", "Lesen"],
        "completed": [True, False, True, False],
        "timestamp": [
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=7),
            datetime.now() - timedelta(days=30),
        ]
    })

# Titel der Seite
st.title("To-Do Statistiken")

# Auswahl der Dauer
duration = st.selectbox(
    "Zeitraum auswählen:",
    options=["1 Tag", "1 Woche", "1 Monat"]
)

# Filtere die Daten basierend auf der Auswahl
if duration == "1 Tag":
    start_date = datetime.now() - timedelta(days=1)
elif duration == "1 Woche":
    start_date = datetime.now() - timedelta(weeks=1)
elif duration == "1 Monat":
    start_date = datetime.now() - timedelta(days=30)

filtered_data = st.session_state.todos_data[
    st.session_state.todos_data["timestamp"] >= start_date
]

# Erledigte und nicht erledigte To-Dos filtern
completed_todos = filtered_data[filtered_data["completed"]]
not_completed_todos = filtered_data[~filtered_data["completed"]]

# Funktion zum Erstellen eines Liniendiagramms
def plot_line_chart(data, title):
    if data.empty:
        st.write(f"Keine Daten für {title.lower()}.")
        return
    counts = data.groupby(data["timestamp"].dt.date).size()
    fig, ax = plt.subplots()
    counts.plot(kind="line", ax=ax, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Datum")
    ax.set_ylabel("Anzahl der To-Dos")
    st.pyplot(fig)

# Grafiken anzeigen
st.subheader("Erledigte To-Dos")
plot_line_chart(completed_todos, "Erledigte To-Dos")

st.subheader("Nicht erledigte To-Dos")
plot_line_chart(not_completed_todos, "Nicht erledigte To-Dos")

