from google import genai
import os
import json
import re

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==============================================
# 1️⃣ QUESTION GENERATION
# ==============================================
def ask_gemini(prompt: str):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    questions = [
        q.strip("- ").strip()
        for q in text.split("\n")
        if q.strip()
    ]

    return questions


# ==============================================
# 2️⃣ STRICT SEMANTIC EVALUATION
# ==============================================
def evaluate_with_gemini(questions, answers, domain):

    prompt = f"""
You are a STRICT senior technical interviewer.

Domain: {domain}

Evaluate the candidate carefully.

For each answer:
- Check technical correctness
- Check depth
- Check structure
- Penalize vague or incorrect answers

Return STRICT JSON only in this format:

{{
  "total_score": int,
  "strengths": [],
  "weaknesses": [],
  "learning_plan": {{
      "performance_level": "",
      "focus_areas": [],
      "technical_gaps": [],
      "2_week_roadmap": [],
      "resources": [],
      "strategy": ""
  }}
}}

Questions:
{questions}

Answers:
{answers}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    import re
    raw = response.text.strip()
    cleaned = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(cleaned)
    except Exception as e:
        print("⚠ JSON Parsing Failed:", e)
        print("Gemini Raw Response:", raw)

        return {
            "total_score": 0,
            "strengths": [],
            "weaknesses": ["Evaluation failed"],
            "learning_plan": {}
        }
