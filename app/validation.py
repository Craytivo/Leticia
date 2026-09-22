import re

ALLOWED_TOPICS = {
    "Marriage & Legal Rights",
    "Finances & Property",
    "Spousal Rights & Responsibilities",
    "Separation",
    "Children & Family",
    "Other",
}

ALLOWED_SITUATIONS = {
    "Currently married",
    "Considering separation",
    "Separated",
    "Divorced",
    "Other",
}

ALLOWED_RESPONSE_PREFERENCES = {"contact", "anonymous"}

EMAIL_RE = re.compile(r"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")


def validate_question(payload):
    errors = {}

    if not isinstance(payload, dict):
        return {}, {"form": "Invalid submission."}

    topic = payload.get("topic", "")
    situation = payload.get("situation", "")
    question = payload.get("question", "")
    preference = payload.get("response_preference", "")
    privacy = payload.get("privacy")
    name = payload.get("name", "")
    email = payload.get("email", "")

    if not isinstance(topic, str) or topic.strip() not in ALLOWED_TOPICS:
        errors["topic"] = "Please select a valid topic."

    if situation and (not isinstance(situation, str) or situation.strip() not in ALLOWED_SITUATIONS):
        errors["situation"] = "Please select a valid situation."

    if not isinstance(question, str):
        errors["question"] = "Please enter your question."
    else:
        question = question.strip()
        if len(question) < 10:
            errors["question"] = "Please enter at least 10 characters."
        elif len(question) > 3000:
            errors["question"] = "Your question must be 3000 characters or fewer."

    if preference not in ALLOWED_RESPONSE_PREFERENCES:
        errors["response_preference"] = "Please select a response preference."

    if privacy is not True:
        errors["privacy"] = "Please confirm the privacy acknowledgement."

    if preference == "contact":
        if not isinstance(name, str) or not name.strip():
            errors["name"] = "Please enter your first name."
        elif len(name.strip()) > 80:
            errors["name"] = "Your first name must be 80 characters or fewer."

        if not isinstance(email, str) or not email.strip():
            errors["email"] = "Please enter your email address."
        elif len(email.strip()) > 254 or not EMAIL_RE.match(email.strip()):
            errors["email"] = "Please enter a valid email address."

    normalized = {
        "topic": topic.strip() if isinstance(topic, str) else "",
        "situation": situation.strip() if isinstance(situation, str) else "",
        "question": question if isinstance(question, str) else "",
        "response_preference": preference,
        "response_requested": preference == "contact",
        "name": name.strip() if preference == "contact" and isinstance(name, str) else None,
        "email": email.strip().lower() if preference == "contact" and isinstance(email, str) else None,
    }

    return normalized, errors
