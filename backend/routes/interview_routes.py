from flask import Blueprint, request, jsonify
import os

from utils.pdf_generator import generate_interview_report
from services.resume_service import extract_resume_text
from services.scoring_service import evaluate_answers
from services.recommendation_service import generate_learning_plan

interview_bp = Blueprint("interview_bp", __name__)


# ======================================================
# 1️⃣ RESUME UPLOAD API
# ======================================================
@interview_bp.route("/interview/upload-resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "Resume file missing"}), 400

    resume = request.files["resume"]

    if resume.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, resume.filename)
    resume.save(file_path)

    resume_text = extract_resume_text(file_path)

    return jsonify({
        "message": "Resume uploaded successfully",
        "resumeText": resume_text[:2000]
    }), 200


# ======================================================
# 2️⃣ INTERVIEW SUBMIT API (FIXED)
# ======================================================
@interview_bp.route("/interview/submit", methods=["POST"])
def submit_interview():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid payload"}), 400

        candidate = data.get("candidate", {})
        config = data.get("config", {})
        answers = data.get("answers", [])

        # =============================
        # VALIDATION
        # =============================
        if not candidate.get("name"):
            return jsonify({"error": "Candidate name missing"}), 400

        if not isinstance(answers, list) or len(answers) == 0:
            return jsonify({"error": "Answers invalid"}), 400


        # =============================
        # AI EVALUATION (FIXED)
        # =============================
        evaluation = evaluate_answers(answers)

        score = evaluation.get("overall_score", 0)
        strengths = evaluation.get("strengths", [])
        improvements = evaluation.get("improvements", [])
        weaknesses = evaluation.get("weaknesses", [])


        # =============================
        # LEARNING PLAN
        # =============================
        learning_plan = generate_learning_plan(
            domain=config.get("domain", "General"),
            score=score,
            weaknesses=weaknesses
        )


        # =============================
        # PDF REPORT
        # =============================
        report_path = generate_interview_report(
            candidate=candidate,
            evaluation={
                "score": score,
                "strengths": strengths,
                "improvements": improvements,
                "learning_plan": learning_plan
            }
        )


        # =============================
        # RESPONSE
        # =============================
        return jsonify({
            "candidate": candidate,
            "score": score,
            "strengths": strengths,
            "improvements": improvements,
            "learning_plan": learning_plan,
            "report": report_path
        }), 200


    except Exception as e:
        print("SUBMIT ERROR:", e)

        return jsonify({
            "error": "Interview submission failed",
            "details": str(e)
        }), 500
