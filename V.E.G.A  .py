import time
import deepspeech as ds
import numpy as np
import pyaudio

class VEGA:
    def __init__(self, model_path, scorer_path):
        self.name = "VEGA"
        self.power = 100
        self.temperature = 30
        self.is_active = False
        self.model = ds.Model(model_path)
        self.model.enableExternalScorer(scorer_path)
        self.stream = None

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
        else:
            print("I'm sorry, I didn't understand that command.")

    def listen_for_command(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 5

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* Listening...")

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* Processing...")

        audio = np.frombuffer(b''.join(frames), dtype=np.int16)
        text = self.model.stt(audio)
        print("You said:", text)
        self.process_command(text)

        stream.stop_stream()
        stream.close()
        p.terminate()

def main():
    model_path = "C:\Users\purus\Downloads\deepspeech-0.9.3-models.pbmm"
    scorer_path = "C:\Users\purus\Downloads\deepspeech-0.9.3-models.scorer"
    vega = VEGA(model_path, scorer_path)
    vega.boot_up()
    while vega.is_active:
        vega.listen_for_command()

if __name__ == "__main__":
    main()
