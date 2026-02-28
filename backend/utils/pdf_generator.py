from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from textwrap import wrap


def generate_interview_report(candidate, domain, difficulty, score,
                              strengths, improvements, learning_plan):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_name = candidate["name"].replace(" ", "_")

    filename = f"Interview_Report_{safe_name}_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50

    # -------------------------------
    # Title
    # -------------------------------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Smart Interview Report")
    y -= 40

    # -------------------------------
    # Candidate Info
    # -------------------------------
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Name: {candidate['name']}")
    y -= 20
    c.drawString(50, y, f"Email: {candidate['email']}")
    y -= 20
    c.drawString(50, y, f"Domain: {domain}")
    y -= 20
    c.drawString(50, y, f"Difficulty: {difficulty}")
    y -= 30

    # -------------------------------
    # Score
    # -------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Final Score: {score}/100")
    y -= 30

    # -------------------------------
    # Strengths
    # -------------------------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Strengths:")
    y -= 20

    c.setFont("Helvetica", 11)
    for s in strengths:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

        wrapped = wrap(s, 85)
        for line in wrapped:
            c.drawString(70, y, f"- {line}")
            y -= 15

        y -= 5

    y -= 10

    # -------------------------------
    # Improvements
    # -------------------------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Areas for Improvement:")
    y -= 20

    c.setFont("Helvetica", 11)
    for i in improvements:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

        wrapped = wrap(i, 85)
        for line in wrapped:
            c.drawString(70, y, f"- {line}")
            y -= 15

        y -= 5

    y -= 10

    # -------------------------------
    # Learning Plan
    # -------------------------------
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Personalized Learning Plan:")
    y -= 20

    c.setFont("Helvetica", 11)

    if isinstance(learning_plan, dict):

        sections = [
            ("Performance Level", learning_plan.get("performance_level")),
            ("Focus Areas", learning_plan.get("focus_areas")),
            ("Technical Gaps", learning_plan.get("technical_gaps")),
            ("2 Week Roadmap", learning_plan.get("two_week_roadmap")),
            ("Recommended Resources", learning_plan.get("recommended_resources")),
            ("Strategy", learning_plan.get("improvement_strategy")),
        ]

        for title, content in sections:

            if y < 60:
                c.showPage()
                y = height - 50

            c.setFont("Helvetica-Bold", 12)
            c.drawString(60, y, title + ":")
            y -= 18

            c.setFont("Helvetica", 11)

            if isinstance(content, list):
                for item in content:
                    wrapped = wrap(str(item), 85)
                    for line in wrapped:
                        c.drawString(80, y, f"- {line}")
                        y -= 14
                    y -= 4
            else:
                wrapped = wrap(str(content), 85)
                for line in wrapped:
                    c.drawString(80, y, line)
                    y -= 14

            y -= 10

    # -------------------------------
    # Save PDF
    # -------------------------------
    c.save()

    # 🔥 IMPORTANT: return only filename
    return filename