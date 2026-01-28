from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from textwrap import wrap

def generate_interview_report(candidate, evaluation):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Interview_Report_{candidate['name']}_{timestamp}.pdf"
    path = os.path.join("reports", filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Smart Interview Report")
    y -= 40

    # Candidate Info
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Name: {candidate['name']}")
    y -= 20
    c.drawString(50, y, f"Email: {candidate['email']}")
    y -= 30

    # Score
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Score: {evaluation['score']}")
    y -= 30

    # Strengths
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Strengths:")
    y -= 20

    c.setFont("Helvetica", 11)
    for s in evaluation["strengths"]:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

        c.drawString(70, y, f"- {s}")
        y -= 15

    y -= 20

    # Improvements
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Areas for Improvement:")
    y -= 20

    c.setFont("Helvetica", 11)
    for i in evaluation["improvements"]:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

        c.drawString(70, y, f"- {i}")
        y -= 15

    y -= 20

    # Learning Plan
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Personalized Learning Plan:")
    y -= 20

    c.setFont("Helvetica", 10)
    for line in evaluation["learning_plan"]:
        wrapped_lines = wrap(line, 90)

        for wline in wrapped_lines:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)

            c.drawString(60, y, wline)
            y -= 14

        y -= 6

    # ✅ SAVE PDF (ONLY ONCE – OUTSIDE LOOPS)
    c.save()
    return path