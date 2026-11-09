
from dotenv import load_dotenv
from google import genai
import os

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API KEY NOT FOUND!")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Say hello to my AI E-Commerce Intelligence project!"
        )

        print("GEMINI CONNECTION SUCCESSFUL!")
        print(response.text)

    except Exception as e:
        print("Connection error:", e)
