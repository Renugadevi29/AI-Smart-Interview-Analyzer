from flask import Blueprint, request, jsonify
from services.gemini_service import evaluate_with_gemini
from services.recommendation_service import generate_learning_plan
from utils.pdf_generator import generate_interview_report
import subprocess
import os
import json

interview_bp = Blueprint("interview_bp", __name__)


# ======================================================
# 1️⃣ SUBMIT INTERVIEW
# ======================================================
@interview_bp.route("/interview/submit", methods=["POST"])
def submit_interview():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        candidate = data.get("candidate")
        config = data.get("config")
        answers = data.get("answers")
        questions = data.get("questions")

        # -----------------------------
        # Validation
        # -----------------------------
        if not candidate:
            return jsonify({"error": "Candidate info missing"}), 400

        if not config:
            return jsonify({"error": "Config missing"}), 400

        if not answers or not questions:
            return jsonify({"error": "Answers or questions missing"}), 400

        # -----------------------------
        # Gemini Evaluation
        # -----------------------------
        evaluation = evaluate_with_gemini(
            questions=questions,
            answers=answers,
            domain=config.get("domain")
        )

        # -----------------------------
        # Generate Learning Plan
        # -----------------------------
        learning_plan = generate_learning_plan(
            domain=config.get("domain"),
            score=evaluation.get("total_score", 0),
            weaknesses=evaluation.get("weaknesses", [])
        )

        # -----------------------------
        # Generate PDF Report
        # -----------------------------
        report_filename = generate_interview_report(
            candidate=candidate,
            domain=config.get("domain"),
            difficulty=config.get("difficulty"),
            score=evaluation.get("total_score", 0),
            strengths=evaluation.get("strengths", []),
            improvements=evaluation.get("improvements", []),
            learning_plan=learning_plan
        )

        return jsonify({
            "candidate": candidate,
            "domain": config.get("domain"),
            "difficulty": config.get("difficulty"),
            "score": evaluation.get("total_score", 0),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
            "learning_plan": learning_plan,
            "report": report_filename
        }), 200

    except Exception as e:
        print("❌ Interview Submission Error:", str(e))
        return jsonify({"error": "Interview evaluation failed"}), 500


# ======================================================
# 2️⃣ SEND REPORT TO MAIL (Trigger UiPath)
# ======================================================
@interview_bp.route("/send-report", methods=["POST"])
def send_report():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        email = data.get("email")
        report = data.get("report")

        if not email:
            return jsonify({"error": "Email missing"}), 400

        if not report:
            return jsonify({"error": "Report filename missing"}), 400

        # -----------------------------
        # Build absolute PDF path
        # -----------------------------
        report_path = os.path.abspath(os.path.join("reports", report))

        if not os.path.exists(report_path):
            return jsonify({"error": f"Report not found: {report_path}"}), 404

        # -----------------------------
        # UiRobot Path
        # -----------------------------
        uirobot_path = r"C:\Users\ELCOT\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"

        if not os.path.exists(uirobot_path):
            return jsonify({"error": "UiRobot.exe not found"}), 404

        # -----------------------------
        # Prepare UiPath arguments
        # MUST match UiPath arguments
        # -----------------------------
        input_data = {
            "in_email": email,
            "in_report": report_path
        }

        # -----------------------------
        # Trigger UiPath Automation
        # -----------------------------
        print("Email:",email)
        print("Report Path:",report_path)
        subprocess.Popen([
            uirobot_path,
            "execute",
            "--process-name",
            "UiPath",
            "--input",
            json.dumps(input_data)
        ])

        return jsonify({
            "message": "UiPath automation triggered successfully"
        }), 200

    except Exception as e:
        print("❌ Send Report Error:", str(e))
        return jsonify({"error": "Failed to trigger automation"}), 500