import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    models = genai.list_models()
    for model in models:
        print(model.name)
except Exception as e:
    print("Error listing models:", e)
import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    models = genai.list_models()
    for model in models:
        print(model.name)
except Exception as e:
    print("Error listing models:", e)
