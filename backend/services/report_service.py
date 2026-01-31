from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(candidate, evaluation, learning_plan):
    os.makedirs("reports", exist_ok=True)

    filename = f"Interview_Report_{candidate['name']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = os.path.join("reports", filename)

    c = canvas.Canvas(path, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Smart Interview Report")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Name: {candidate['name']}")
    y -= 20
    c.drawString(50, y, f"Email: {candidate['email']}")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Score: {evaluation['score']}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Strengths:")
    y -= 20
    for s in evaluation["strengths"]:
        c.drawString(70, y, f"- {s}")
        y -= 15

    y -= 10
    c.drawString(50, y, "Improvements:")
    y -= 20
    for i in evaluation["improvements"]:
        c.drawString(70, y, f"- {i}")
        y -= 15

    y -= 20
    c.drawString(50, y, "Learning Plan:")
    y -= 20
    c.setFont("Helvetica", 10)
    for line in learning_plan.split("\n"):
        c.drawString(60, y, line)
        y -= 14

    c.save()
    return path
