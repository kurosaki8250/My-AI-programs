import time
import speech_recognition as sr
import pyttsx3
import requests

class VEGA:
    def __init__(self):
        self.name = "VEGA"
        self.power = 100
        self.temperature = 30
        self.is_active = False

    def boot_up(self):
        print("Initializing VEGA...")
        time.sleep(1)
        print("System online. Welcome, Slayer.")
        self.is_active = True

    def shutdown(self):
        print("Shutting down VEGA...")
        time.sleep(1)
        print("System offline.")
        self.is_active = False

    def monitor_temperature(self):
        print(f"Temperature: {self.temperature} degrees Celsius.")

    def monitor_power(self):
        print(f"Power level: {self.power}%.")

    def process_command(self, command):
        if any(word in command for word in ["shutdown", "turn off", "power down"]):
            self.shutdown()
        elif any(word in command for word in ["temperature", "temp"]):
            self.monitor_temperature()
        elif "power" in command:
            self.monitor_power()
        elif "internet" in command:
            self.access_internet()
        else:
            print("I'm sorry, I didn't understand that command.")

    def access_internet(self):
        try:
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                print("Internet access successful.")
                # Process the response data here if needed
            else:
                print(f"Failed to access internet. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Failed to access internet: {e}")

    def chat(self):
        while self.is_active:
            r = sr.Recognizer()
            engine = pyttsx3.init()

            with sr.Microphone() as source:
                print("You: ")
                audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print("You said:", text)
                if any(greeting in text for greeting in ["hello", "hi", "hey"]):
                    engine.say("Hello there! How can I assist you today?")
                    engine.runAndWait()
                else:
                    self.process_command(text)
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def main():
    vega = VEGA()
    vega.boot_up()
    vega.chat()

if __name__ == "__main__":
    main()
