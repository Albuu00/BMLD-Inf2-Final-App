# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======
import streamlit as st

# Titel der App
st.title("My Daily Diary")

# Textfeld für den Nutzer
user_input = st.text_area("Schreibe hier deine Gedanken:", placeholder="Dein Text...")

# Button zum Speichern
if st.button("Speichern"):
    with open("daily_diary.txt", "a", encoding="utf-8") as file:
        file.write(user_input + "\n")
    st.success("Dein Text wurde gespeichert!")