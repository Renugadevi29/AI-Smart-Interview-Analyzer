from flask import Blueprint, request, jsonify
from services.gemini_service import evaluate_with_gemini
from services.recommendation_service import generate_learning_plan
from services.hybrid_service import hybrid_score
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

        # ======================================================
        # ✅ SAFE GEMINI EVALUATION
        # ======================================================
        try:
            evaluation = evaluate_with_gemini(
                questions=questions,
                answers=answers,
                domain=config.get("domain")
            )
        except Exception as e:
            print("⚠️ Gemini Evaluation Error:", str(e))
            evaluation = {
                "total_score": 50,
                "strengths": [],
                "improvements": [],
                "weaknesses": []
            }

        print("✅ Gemini evaluation completed")
        print("Questions:", questions)
        print("Answers:", answers)

        # ======================================================
        # 🆕 HYBRID MODEL (FULLY INDEPENDENT)
        # ======================================================
        hybrid_results = []

        for q, ans in zip(questions, answers):
            try:
                # 👇 No Gemini dependency anymore
                score = hybrid_score(ans, q)
                hybrid_results.append(score)

            except Exception as e:
                print("⚠️ Hybrid Error:", str(e))
                hybrid_results.append(0)

        # Average Hybrid Score
        avg_hybrid_score = 0
        if len(hybrid_results) > 0:
            avg_hybrid_score = sum(hybrid_results) / len(hybrid_results)

        print("Gemini Score:", evaluation.get("total_score"))
        print("Hybrid Score:", avg_hybrid_score)

        # -----------------------------
        # Generate Learning Plan
        # -----------------------------
        try:
            learning_plan = generate_learning_plan(
                domain=config.get("domain"),
                score=evaluation.get("total_score", 0),
                weaknesses=evaluation.get("weaknesses", [])
            )
        except Exception as e:
            print("⚠️ Learning Plan Error:", str(e))
            learning_plan = {
                "performance_level": "Unavailable",
                "focus_areas": [],
                "technical_gaps": [],
                "two_week_roadmap": [],
                "recommended_resources": [],
                "improvement_strategy": "Could not generate due to API load"
            }

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
            "hybrid_score": avg_hybrid_score,
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
            "learning_plan": learning_plan,
            "report": report_filename
        }), 200

    except Exception as e:
        print("❌ Interview Submission Error:", str(e))
        return jsonify({"error": "Interview evaluation failed"}), 500


# ======================================================
# 2️⃣ SEND REPORT TO MAIL (UNCHANGED)
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

        report_path = os.path.abspath(os.path.join("reports", report))

        if not os.path.exists(report_path):
            return jsonify({"error": f"Report not found: {report_path}"}), 404

        uirobot_path = r"C:\Users\ELCOT\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"

        if not os.path.exists(uirobot_path):
            return jsonify({"error": "UiRobot.exe not found"}), 404

        input_data = {
            "in_email": email,
            "in_report": report_path
        }

        print("Email:", email)
        print("Report Path:", report_path)

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