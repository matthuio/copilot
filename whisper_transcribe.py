import whisper
from send_request import send_request

def transcribe():
    model = whisper.load_model("base")  # you can change this later
    result = model.transcribe("voice.wav")

    print(result["text"])

    with open("transcription.txt","w", encoding="utf-8") as f:
        f.write(result["text"])

    send_request()