from datetime import datetime
# ====== Start Login Block ======
from utils.login_manager import LoginManager
from utils.data_manager import DataManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import requests

# OpenWeatherMap API-Schlüssel und Basis-URL
API_KEY = "b08ff895beacec99a194e0aa80c2aac4"  # Ersetze dies durch deinen OpenWeatherMap-API-Schlüssel
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# Funktion, um Wetterdaten abzurufen
def get_weather(city="Zurich"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(BASE_URL, params=params)
    st.write(f"HTTP-Statuscode: {response.status_code}")  # Debugging: Zeigt den HTTP-Statuscode an
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        st.error("Ungültiger API-Schlüssel. Bitte überprüfe deinen API-Schlüssel.")
    else:
        st.error(f"Fehler beim Abrufen der Wetterdaten: {response.status_code}")
    return None

# Funktion, um eine Wetteraussage zu generieren
def generate_weather_message(weather_data):
    if not weather_data:
        return "Wetterdaten konnten nicht abgerufen werden."
    
    weather = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]

    if "sonnig" in weather or "klar" in weather:
        return f"Heute ist es schön sonnig draußen mit {temp}°C. Ein perfekter Tag, um draußen etwas zu unternehmen!"
    elif "regen" in weather or "nass" in weather:
        return f"Heute regnet es stark mit {temp}°C. Eine super Gelegenheit, um es sich zu Hause gemütlich zu machen!"
    elif "bewölkt" in weather:
        return f"Heute ist es bewölkt mit {temp}°C. Vielleicht ein guter Tag für einen Spaziergang!"
    else:
        return f"Das Wetter heute: {weather} mit {temp}°C. Mach das Beste daraus!"

# Wetterdaten abrufen
weather_data = get_weather()

# Aktuelles Datum, Wochentag und Uhrzeit
current_time = datetime.now().strftime("%A, %d. %B %Y, %H:%M:%S")

# Titel der Seite mit Datum und Zeit
st.title(f"To-Do Liste  |  {current_time}")

# Wetterbericht anzeigen
st.subheader("Wetterbericht")
weather_message = generate_weather_message(weather_data)
st.write(weather_message)

# Initiale To-Do-Liste
if "todos" not in st.session_state:
    st.session_state.todos = [
        {"task": "2 Liter Wasser trinken", "completed": False},
        {"task": "Spazieren", "completed": False},
        {"task": "10 Minuten Dehnen", "completed": False},
        {"task": "Mindestens eine Frucht gegessen", "completed": False},
        {"task": "Mindestens ein Gemüse gegessen", "completed": False},
        {"task": "7 bis 8 Stunden geschlafen", "completed": False},
        {"task": "Etwas aufräumen oder putzen", "completed": False},
        {"task": "Mindestens eine Stunde Handypause", "completed": False}
    ]

# Funktion zum Abhaken von Aufgaben
def toggle_task(index):
    st.session_state.todos[index]["completed"] = not st.session_state.todos[index]["completed"]


# Eingabefeld und Button zum Hinzufügen neuer To-Dos
st.subheader("Neues To-Do hinzufügen")
new_todo = st.text_input("Gib ein neues To-Do ein:")
if st.button("Hinzufügen"):
    if new_todo.strip():  # Überprüfen, ob das Eingabefeld nicht leer ist
        st.session_state.todos.append({"task": new_todo.strip(), "completed": False})
        st.success(f"'{new_todo}' wurde zur To-Do-Liste hinzugefügt!")
    else:
        st.error("Das To-Do-Feld darf nicht leer sein.")

# To-Do-Liste anzeigen
for i, todo in enumerate(st.session_state.todos):
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col1:
        # Checkbox zum Abhaken
        #checked = st.checkbox("", value=todo["completed"], key=f"todo_{i}")
        #if checked != todo["completed"]:
            #toggle_task(i)
        # Checkbox oder grüner Haken anzeigen
        if todo["completed"]:
            # Grüner Haken anzeigen, wenn die Aufgabe erledigt ist
            st.markdown(
                f"<span style='color: green; font-size: 20px;'>✔</span>",
                unsafe_allow_html=True,
            )
        else:
            # Checkbox anzeigen, wenn die Aufgabe nicht erledigt ist
            if st.checkbox("", value=todo["completed"], key=f"todo_{i}"):
                # Status der Aufgabe direkt aktualisieren
                st.session_state.todos[i]["completed"] = True
    with col2:
        # Aufgabe anzeigen (grau, wenn abgehakt)
        if todo["completed"]:
            st.markdown(f"<span style='color: gray; text-decoration: line-through;'>{todo['task']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(todo["task"])
    with col3:
        # Button zum Löschen der Aufgabe
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()
            