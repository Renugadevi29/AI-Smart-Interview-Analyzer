from flask import Blueprint, request, jsonify
import os
import uuid
from services.resume_service import extract_text_from_pdf

resume_bp = Blueprint("resume_bp", __name__)

UPLOAD_FOLDER = "uploads"

# Temporary in-memory storage
RESUME_STORAGE = {}

@resume_bp.route("/resume/upload", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        if not file.filename.endswith(".pdf"):
            return jsonify({"error": "Only PDF allowed"}), 400

        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)

        # Extract text
        resume_text = extract_text_from_pdf(file_path)

        # Store temporarily
        RESUME_STORAGE[unique_id] = resume_text

        return jsonify({
            "resume_id": unique_id
        }), 200

    except Exception as e:
        print("❌ Resume Upload Error:", e)
        return jsonify({"error": "Resume upload failed"}), 500