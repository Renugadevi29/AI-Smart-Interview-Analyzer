import os
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()

# Get key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

# Init client
client = genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> list:
    """
    Generate interview questions using Gemini
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini")

        text = response.text.strip()

        questions = [
            q.strip("-• ").strip()
            for q in text.split("\n")
            if q.strip()
        ]

        return questions

    except Exception as e:
        print("🔥 Gemini API Error:", e)
        raise e
