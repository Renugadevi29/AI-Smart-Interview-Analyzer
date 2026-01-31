from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from routes.question_routes import question_bp
from routes.interview_routes import interview_bp
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app)

# -----------------------------
# BASE DIRECTORY CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# -----------------------------
# BLUEPRINTS
# -----------------------------
app.register_blueprint(question_bp, url_prefix="/api")
app.register_blueprint(interview_bp, url_prefix="/api")
app.register_blueprint(analysis_bp, url_prefix="/api")

# -----------------------------
# HOME CHECK
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "Smart Interview Backend Running ✅"
    })

# -----------------------------
# PDF DOWNLOAD ROUTE ✅
# -----------------------------
@app.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)