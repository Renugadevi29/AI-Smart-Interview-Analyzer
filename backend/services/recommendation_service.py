from services.gemini_service import ask_gemini
import json

def generate_learning_plan(domain, score, weaknesses):

    prompt = f"""
You are a strict AI interview evaluator.

Candidate Performance:
Domain: {domain}
Score: {score}/100
Weak Areas: {", ".join(weaknesses)}

Generate a HIGHLY personalized structured learning plan.

Return JSON in this format:

{{
  "performance_level": "",
  "focus_areas": [],
  "technical_gaps": [],
  "two_week_roadmap": [],
  "recommended_resources": [],
  "improvement_strategy": ""
}}

Rules:
- Must explain why marks were lost.
- Must be domain specific.
- Minimum 300 words total.
- Do not give generic advice.
"""

    response = ask_gemini(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "performance_level": "Needs Improvement",
            "focus_areas": weaknesses,
            "technical_gaps": weaknesses,
            "two_week_roadmap": ["Revise fundamentals daily"],
            "recommended_resources": ["Official documentation"],
            "improvement_strategy": "Focus on conceptual clarity."
        }
