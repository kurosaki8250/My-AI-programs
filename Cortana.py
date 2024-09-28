import torch
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit as kit
import pyjokes
import pytz
from transformers import pipeline

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on the time of day
def wish_me():
    hour = int(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Cortana. How can I assist you today?")

# Function to take microphone input from the user and return it as text
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
    except Exception as e:
        print("Say that again please...")
        return None

    return command

# Initialize Whisper model for speech recognition
model_id = "openai/whisper-large-v2"
whisper_model = pipeline('automatic-speech-recognition', model=model_id)

# Function to handle various user commands
def run_assistant():
    wish_me()
    while True:
        command = take_command()
        if command is None:
            continue

        command = command.lower()

        if 'wikipedia' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in command:
            webbrowser.open("youtube.com")

        elif 'open google' in command:
            webbrowser.open("google.com")

        elif 'play music' in command:
            music_dir = 'path_to_music_directory'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in command:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open code' in command:
            code_path = "path_to_vscode"
            os.startfile(code_path)

        elif 'play' in command:
            song = command.replace('play', '')
            speak('playing ' + song)
            kit.playonyt(song)

        elif 'tell me a joke' in command:
            speak(pyjokes.get_joke())

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break

# Start the assistant
if __name__ == "__main__":
    run_assistant()

