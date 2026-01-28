from flask import Flask, jsonify
from flask_cors import CORS

from routes.question_routes import question_bp
from routes.interview_routes import interview_bp
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(question_bp, url_prefix="/api")
app.register_blueprint(interview_bp, url_prefix="/api")
app.register_blueprint(analysis_bp, url_prefix="/api")

@app.route("/")
def home():
    return jsonify({
        "status": "Smart Interview Backend Running ✅"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)