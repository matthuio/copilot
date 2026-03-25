import google.generativeai as genai
import os

# Replace with your API key
genai.configure(api_key='AIzaSyClL6GNrUMIdILzXbA0_Qs3MTEirU9fnW0')

try:
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content("Say hello in a short sentence")
    print(response.text)
except Exception as e:
    print("Error:", e)

input("Press Enter to exit...")
