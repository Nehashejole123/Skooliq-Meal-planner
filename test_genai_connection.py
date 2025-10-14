import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # loads .env file

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No GEMINI_API_KEY found in .env file")
else:
    try:
        client = genai.Client(api_key=api_key)
        models = list(client.models.list())
        print("✅ Connection successful! Available models:")
        for m in models:
            print("-", m.name)
    except Exception as e:
        print("❌ Error:", e)
