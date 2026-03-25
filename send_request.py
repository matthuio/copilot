import google.generativeai as genai
import os

# Replace with your API key
genai.configure(api_key='AIzaSyCF2wfo-EXl8znuPw9Oq-ACCvmy8emWQno')
try:
    # models=genai.list_models()
    # for x in models:
    #     print(x)
    with open("transcription.txt","r", encoding="utf-8") as f:
        text=f.read()
        print(text)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(text)
    print(response.text)
    f.close()
except Exception as e:
    print("Error:", e)

input("Press Enter to exit...")
