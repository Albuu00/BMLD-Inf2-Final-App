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
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        # Checkbox zum Abhaken
        if st.checkbox("", value=todo["completed"], key=f"todo_{i}"):
            toggle_task(i)
    with col2:
        # Aufgabe anzeigen (grau, wenn abgehakt)
        if todo["completed"]:
            st.markdown(f"<span style='color: gray; text-decoration: line-through;'>{todo['task']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(todo["task"])