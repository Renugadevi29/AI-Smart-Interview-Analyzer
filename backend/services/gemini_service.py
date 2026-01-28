from google import genai
import os

# Initialize client with API key
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(prompt: str) -> list:
    """
    Generate interview questions dynamically using Gemini
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    # Gemini returns text → split into questions
    text = response.text.strip()

    questions = [
        q.strip("- ").strip()
        for q in text.split("\n")
        if q.strip()
    ]

    return questions