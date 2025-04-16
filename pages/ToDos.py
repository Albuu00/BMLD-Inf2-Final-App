import streamlit as st

# Initiale To-Do-Liste
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"task": "2 Liter Wasser trinken", "completed": False},
        {"task": "Spazieren", "completed": False},
    ]

st.title("To-Do Liste")

# Funktion zum Abhaken von Aufgaben
def toggle_task(index):
    st.session_state.todos[index]["completed"] = not st.session_state.todos[index]["completed"]

# To-Do-Liste anzeigen
selected_tasks = st.multiselect(
    "Wähle die Aufgaben aus, die du abhaken möchtest:",
    options=[todo["task"] for todo in st.session_state.todos],
    default=[todo["task"] for todo in st.session_state.todos if todo["completed"]],
)

# Aktualisiere den Status der Aufgaben basierend auf der Auswahl
for i, todo in enumerate(st.session_state.todos):
    if todo["task"] in selected_tasks:
        todo["completed"] = True
    else:
        todo["completed"] = False

# Aufgaben anzeigen
for todo in st.session_state.todos:
    if todo["completed"]:
        st.markdown(
            f"<span style='color: gray; text-decoration: line-through;'>{todo['task']}</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(todo["task"])