from flask import Blueprint, jsonify, render_template, request

from .services.questions import save_question
from .validation import validate_question

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return render_template("index.html")


@main.get("/health")
def health():
    return {"status": "ok"}


@main.post("/api/questions")
def submit_question():
    if not request.is_json:
        return jsonify(ok=False, errors={"form": "Please submit the form normally."}), 400

    payload = request.get_json(silent=True)
    normalized, errors = validate_question(payload)

    if errors:
        return jsonify(ok=False, errors=errors), 400

    if payload.get("website"):
        return jsonify(ok=True, question_id="LET-SPAM"), 201

    saved = save_question(normalized)
    return jsonify(ok=True, question_id=saved["id"]), 201


@main.get("/thank-you")
def thank_you():
    return render_template("thank-you.html")
