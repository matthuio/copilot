import soundcard as sc
import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100

# List all physical microphones
mics = sc.all_microphones(include_loopback=False)
if not mics:
    print("No microphones found!")
    input("Press Enter to exit")
    exit()

# Pick the first microphone
mic = mics[0]
print(f"Testing recording from: {mic.name}")

try:
    with mic.recorder(samplerate=sample_rate) as recorder:
        print("Recording 5 seconds...")
        audio = recorder.record(numframes=sample_rate * 5)
except Exception as e:
    print("Error during recording:", e)
    input("Press Enter to exit")
    exit()

# Normalize and save
audio = audio.flatten()
audio = audio - np.mean(audio)
max_val = np.max(np.abs(audio))
if max_val > 0:
    audio = audio / max_val
audio_int16 = np.int16(audio * 32767)

write("test.wav", sample_rate, audio_int16)
print("Saved test.wav successfully!")
input("Press Enter to exit...")
