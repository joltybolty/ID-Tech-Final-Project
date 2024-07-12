import pyaudio
from openai import OpenAI
import wave
from pynput import keyboard
import sounddevice as sd
from scipy.io.wavfile import write

client = OpenAI(
    api_key = "sk-proj-lEyW1PTgYBP9bQMeYikkT3BlbkFJQAXez34xx1DY4nYOep0P"
)

class recorder:
    recording = False
    def __init__(self, wavfile, chunksize, dataformat, channels, rate):
        self.filename = wavfile
        self.chunksize = chunksize
        self.dataformat = dataformat
        self.channels = channels
        self.rate = rate
        self.pa = pyaudio.PyAudio()

    def start(self):
        if not self.recording:
            self.wf = wave.open(self.filename, "wb")
            self.wf.setnchannels(self.channels)
            self.wf.setsampwidth(self.pa.get_sample_size(self.dataformat))
            self.wf.setframerate(self.rate)

            def callback(in_data, frame_count, time_info, status):
                self.wf.writeframes(in_data)
                return(in_data, pyaudio.paContinue)

            self.stream = self.pa.open(format = self.dataformat, channels = self.channels, rate = self.rate, input = True, stream_callback = callback)
            self.stream.start_stream()
            self.recording = True
            print("Recording...")

    def stop(self):
        if self.recording:
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.recording = False
            print("Recording finished.")

r = recorder("mic.wav", 8192, pyaudio.paInt16, 2, 44100)