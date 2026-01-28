from flask import Blueprint, request, jsonify
import os
from utils.pdf_generator import generate_interview_report
from services.resume_service import extract_resume_text
from services.scoring_service import evaluate_answers
from services.recommendation_service import generate_learning_plan  

interview_bp = Blueprint("interview_bp", __name__)

# ===============================
# 1️⃣ RESUME UPLOAD API
# ===============================
@interview_bp.route("/interview/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "Resume file missing"}), 400

    resume = request.files["resume"]

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, resume.filename)
    resume.save(file_path)

    text = extract_resume_text(file_path)

    return jsonify({
        "message": "Resume uploaded successfully",
        "resumeText": text[:2000]
    })


# ===============================
# 2️⃣ INTERVIEW SUBMISSION API
# ===============================
@interview_bp.route("/interview/submit", methods=["POST"])
def submit_interview():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    candidate = data.get("candidate", {})
    config = data.get("config", {})
    answers = data.get("answers", [])

    if not answers:
        return jsonify({"error": "Answers missing"}), 400

    # Evaluate answers
    evaluation = evaluate_answers(answers)

    # Generate personalized learning plan
    learning_plan = generate_learning_plan(
        domain=config.get("domain"),
        score=evaluation["score"],
        weaknesses=evaluation["improvements"]
    )

    report_path = generate_interview_report(
        candidate,
        {
            "score": evaluation["score"],
            "strengths": evaluation["strengths"],
            "improvements": evaluation["improvements"],
            "learning_plan": learning_plan
        }
    )

    return jsonify({
        "candidate": candidate,
        "score": evaluation["score"],
        "strengths": evaluation["strengths"],
        "improvements": evaluation["improvements"],
        "learning_plan": learning_plan,
        "report": report_path
    })