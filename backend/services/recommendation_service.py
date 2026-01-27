from services.gemini_service import ask_gemini

def generate_personalized_learning_plan(domain, score, weaknesses, experience, resume_summary=None):

    prompt = f"""
You are an AI interview coach.

Candidate Details:
- Domain: {domain}
- Overall Score: {score}
- Experience Level: {experience}
- Weak Areas: {", ".join(weaknesses)}

{f"Resume Summary: {resume_summary}" if resume_summary else ""}

Generate a personalized learning plan including:
1. Key improvement areas
2. Topics to learn
3. Daily / weekly practice roadmap
4. Recommended resources
5. Final motivation note

Keep it concise and actionable.
"""

    return ask_gemini(prompt)
