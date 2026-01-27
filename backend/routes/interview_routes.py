from flask import Blueprint, request, jsonify
from services.scoring_service import evaluate_answers
from services.recommendation_service import generate_personalized_learning_plan
import os
from flask import Blueprint, request, jsonify
from services.resume_service import extract_resume_text
from services.gemini_service import ask_gemini


interview_bp = Blueprint("interview_bp", __name__)


@interview_bp.route("/submit", methods=["POST"])
def submit_interview():
    data = request.json

    answers = data.get("answers", [])
    domain = data.get("domain")

    evaluation = evaluate_answers(answers)
    learning_path = generate_personalized_learning_plan(
    domain=domain,
    score=evaluation["score"],
    weaknesses=evaluation["improvements"],
    experience=data.get("experience", "Fresher")
)


    return jsonify({
        "evaluation": evaluation,
        "learningPath": learning_path
    })

@interview_bp.route("/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    resume = request.files["resume"]

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, resume.filename)
    resume.save(file_path)

    resume_text = extract_resume_text(file_path)

    return jsonify({
        "message": "Resume uploaded successfully",
        "resumeText": resume_text[:2000]  # limit text for safety
    })
