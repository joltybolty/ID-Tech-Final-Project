import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
print("--- Say the word 'goodbye' in any sentence to end session ---")
client = OpenAI(
    api_key = "sk-proj-lEyW1PTgYBP9bQMeYikkT3BlbkFJQAXez34xx1DY4nYOep0P"
)
freq = 48000
duration = 10
end_session = False
while not end_session:
    print("Recording...")
    recording = sd.rec(int(duration * freq), samplerate = freq, channels = 2)
    sd.wait()

    write("recording0.wav", freq, recording)
    audio_file = open("recording0.wav", "rb")
    transcript = client.audio.translations.create(
        model = "whisper-1",
        file = audio_file
    )
    print("Recording finished.")
    system_data = [
        {
            "role": "system",
            "content": "You are an assistant who answers any prompts given to you to the best of your abilities"
        },
        {
            "role": "user",
            "content": transcript.text
        }
    ]
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = system_data
    )
    assistant_response = response.choices[0].message.content
    system_data.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )
    print(transcript.text)
    if not("goodbye" in transcript.text or "Goodbye" in transcript.text):
        print("Assistant: " + assistant_response)
    else:
        print(transcript.text)
        end_session = True