from flask import Blueprint, request, jsonify
from services.gemini_service import evaluate_with_gemini
from services.recommendation_service import generate_learning_plan
from utils.pdf_generator import generate_interview_report
import subprocess
import os

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

        # -----------------------------
        # Return Final Response
        # -----------------------------
        return jsonify({
            "candidate": candidate,
            "domain": config.get("domain"),
            "difficulty": config.get("difficulty"),
            "score": evaluation.get("total_score", 0),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
            "learning_plan": learning_plan,
            "report": report_filename  # 🔥 IMPORTANT for download + email
        }), 200

    except Exception as e:
        print("❌ Interview Submission Error:", e)
        return jsonify({"error": "Interview evaluation failed"}), 500


# ======================================================
# 2️⃣ SEND REPORT TO MAIL (Trigger UiPath Robot)
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
        # Validate report file exists
        # -----------------------------
        report_path = os.path.join("reports", report)

        if not os.path.exists(report_path):
            return jsonify({"error": "Report file not found"}), 404

        # -----------------------------
        # UiPath Robot Executable Path
        # -----------------------------
        uirobot_path = r"C:\Users\ELCOT\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"

        # -----------------------------
        # UiPath Workflow File Path
        # 🔁 Change this to your actual xaml path
        # -----------------------------
        workflow_path = r"D:\UiPathProjects\SendInterviewReport.xaml"

        # -----------------------------
        # Trigger UiPath Process
        # -----------------------------
        subprocess.Popen([
            uirobot_path,
            "-file",
            workflow_path,
            "-input",
            f'{{"email":"{email}","report":"{report}"}}'
        ])

        return jsonify({
            "message": "UiPath automation triggered successfully"
        }), 200

    except Exception as e:
        print("❌ Send Report Error:", e)
        return jsonify({"error": "Failed to trigger automation"}), 500