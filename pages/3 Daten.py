# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======
import streamlit as st

# Überprüfen, ob die To-Do-Liste existiert
if "todos" not in st.session_state:
    st.session_state.todos = []

st.title("Übersicht der To-Dos")

# Erfüllte und nicht erfüllte To-Dos filtern
erfüllte_todos = [todo["task"] for todo in st.session_state.todos if todo["completed"]]
nicht_erfüllte_todos = [todo["task"] for todo in st.session_state.todos if not todo["completed"]]

# Erfüllte To-Dos anzeigen
st.subheader("✅ Erfüllte To-Dos")
if erfüllte_todos:
    for todo in erfüllte_todos:
        st.markdown(f"- {todo}")
else:
    st.info("Es gibt keine erfüllten To-Dos.")

# Nicht erfüllte To-Dos anzeigen
st.subheader("❌ Nicht erfüllte To-Dos")
if nicht_erfüllte_todos:
    for todo in nicht_erfüllte_todos:
        st.markdown(f"- {todo}")
else:
    st.info("Alle To-Dos wurden erfüllt!")