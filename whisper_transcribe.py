import whisper

model = whisper.load_model("base")  # you can change this later
result = model.transcribe("voice.wav")

print(result["text"])

with open("transcription.txt","w", encoding="utf-8") as f:
    f.write(result["text"])