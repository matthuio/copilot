import keyboard
import time
import winsound
import threading
import pyaudio
import numpy as np
from scipy.io.wavfile import write
from whisper_transcribe import transcribe

# Settings
sample_rate = 44100
chunk_size = 1024
recording = []
is_recording = False

p = pyaudio.PyAudio()
stream = None

def record_audio():
    global recording, is_recording, stream
    try:
        while is_recording:
            data = stream.read(chunk_size, exception_on_overflow=False)
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            recording.append(audio_chunk)
    except Exception as e:
        print("Recording thread error:", e)

def hotkeyPress(event):
    global is_recording, recording, stream
    if not is_recording:
        try:
            winsound.Beep(389, 30)
            print("Recording started...")
            recording = []
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=sample_rate,
                            input=True,
                            frames_per_buffer=chunk_size)
            is_recording = True
            threading.Thread(target=record_audio, daemon=True).start()
        except Exception as e:
            print("Error starting recording:", e)

def hotkeyRelease(event):
    global is_recording, recording, stream
    if is_recording:
        try:
            winsound.Beep(500, 40)
            print("Recording stopped")
            is_recording = False
            time.sleep(0.1)  # give thread a moment to finish

            if stream:
                stream.stop_stream()
                stream.close()
                stream = None

            if recording:
                audio = np.concatenate(recording)
                audio = audio - np.mean(audio)
                max_val = np.max(np.abs(audio))
                if max_val > 0:
                    audio = audio / max_val
                audio_int16 = np.int16(audio * 32767)
                write("voice.wav", sample_rate, audio_int16)
                print("Saved voice.wav,Transcribing")
                transcribe()
            else:
                print("No audio recorded.")
        except Exception as e:
            print("Error stopping recording:", e)

# Setup hotkeys
try:
    keyboard.on_press_key("v", hotkeyPress)
    keyboard.on_release_key("v", hotkeyRelease)
except Exception as e:
    print("Error registering hotkeys:", e)
    input("Press Enter to exit")
    exit()

# Keep script alive
try:
    print("Press 'v' to start/stop recording. Press Ctrl+C to quit.")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nExiting program.")
except Exception as e:
    print("Unexpected error:", e)
input("Press Enter to close...")
