from transformers import AutoTokenizer, AutoModelForCausalLM
import pyttsx3
import requests
from bs4 import BeautifulSoup
import os
import platform
import subprocess
import datetime
import torchaudio
import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2Processor

# Specify the model name
model_name = "cognitivecomputations/dolphin-2.9-llama3-8b"

# Download the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("./dolphin_llama3_8b")
tokenizer.save_pretrained("./dolphin_llama3_8b")

print("Model and tokenizer downloaded and saved locally.")

# Initialize Whisper model for speech-to-text
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForSequenceClassification.from_pretrained("facebook/wav2vec2-large-960h")

# Function to generate text using the model
def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(inputs['input_ids'], max_length=150, num_return_sequences=1)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to fetch weather information without an API
def fetch_weather(city):
    url = f'https://wttr.in/{city}?format=%C+%t'
    response = requests.get(url)
    weather_info = response.text.strip()
    return weather_info

# Function to browse the web
def browse_web(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('div', class_='BNeawe').text
    return result

# Function to get local device information
def get_device_info():
    battery = torch.device("cpu")
    memory_info = torch.virtual_memory()
    memory_percent = memory_info.percent
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_info = (f"Battery level: {battery_percent}%, "
                   f"Memory usage: {memory_percent}%, "
                   f"Current time: {time_now}")
    return device_info

# Function to open applications (Windows example)
def open_application(app_name):
    if platform.system() == "Windows":
        try:
            subprocess.Popen(app_name)
            return f"Opened {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    else:
        return "Application opening is not supported on this OS"

# Function to record audio and save to a file
def record_audio(filename, duration=5):
    # Initialize audio recording
    sample_rate = 44100
    channels = 1
    format = "wav"

    # Start recording
    print("Recording...")
    with torch.no_grad():
        # Use torchaudio's SoXEffectsChain for recording
        effects = torchaudio.sox_effects.SoxEffectsChain()
        effects.set_input_file(filename, sample_rate=sample_rate, channels=channels, format=format)
        effects.append_effect_to_chain("silence", [1, "0.1", "0.1%"], True)
        effects.append_effect_to_chain("trim", ["0.0", str(duration)])
        effects.append_effect_to_chain("norm", [])
        effects.append_effect_to_chain("rate", [str(sample_rate)])
        effects.append_effect_to_chain("channels", [str(channels)])
        effects.append_effect_to_chain("rate", [str(sample_rate)])
        effects.append_effect_to_chain("gain", ["-h"])
        effects.append_effect_to_chain("channels", [str(channels)])
        effects.append_effect_to_chain("channels", [str(channels)])
        effects.append_effect_to_chain("channels", [str(channels)])

        # Apply effects and save to file
        effects.apply_effect_file(filename)

    print(f"Audio recording saved as {filename}")

# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    # Load audio file and transcribe
    audio_input, _ = torchaudio.load(filename)
    inputs = processor(audio_input, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)

    return transcription[0]

# Main function to run the AI assistant
def main():
    while True:
        print("Speak now...")
        audio_filename = "input.wav"
        record_audio(audio_filename)
        user_input = transcribe_audio(audio_filename)
        
        print(f"You: {user_input}")

        if user_input.lower() == 'exit':
            break
        
        if "weather" in user_input.lower():
            city = user_input.split()[-1]  # Assuming the city is the last word
            response = fetch_weather(city)
        elif "browse" in user_input.lower():
            query = ' '.join(user_input.split()[1:])  # Assuming the query follows the keyword 'browse'
            response = browse_web(query)
        elif "device info" in user_input.lower():
            response = get_device_info()
        elif "open" in user_input.lower():
            app_name = ' '.join(user_input.split()[1:])  # Assuming the app name follows the keyword 'open'
            response = open_application(app_name)
        else:
            response = generate_text(user_input)
        
        print(f"Obsidian: {response}")
        text_to_speech(response)

if __name__ == "__main__":
    main()
