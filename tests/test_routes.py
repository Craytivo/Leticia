from app import create_app


def test_home_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Leticia Ngwenya" in response.data
    assert b"Know your rights" in response.data


def test_health_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_question_submission_validation():
    app = create_app()
    client = app.test_client()
    response = client.post("/api/questions", json={
        "topic": "",
        "question": "too short",
        "response_preference": "contact",
        "privacy": False,
    })
    assert response.status_code == 400
    assert response.json["ok"] is False
    assert "topic" in response.json["errors"]
    assert "name" in response.json["errors"]
    assert "email" in response.json["errors"]
    assert "privacy" in response.json["errors"]


def test_question_submission_anonymous(tmp_path, monkeypatch):
    from app.services import questions

    monkeypatch.setattr(questions, "DATA_DIR", tmp_path)
    monkeypatch.setattr(questions, "DATA_FILE", tmp_path / "questions.json")

    app = create_app()
    client = app.test_client()
    response = client.post("/api/questions", json={
        "topic": "Marriage & Legal Rights",
        "situation": "Currently married",
        "question": "What legal rights should I understand within my marriage?",
        "response_preference": "anonymous",
        "privacy": True,
    })

    assert response.status_code == 201
    assert response.json["ok"] is True
    assert response.json["question_id"] == "LET-0001"

    saved = (tmp_path / "questions.json").read_text(encoding="utf-8")
    assert "LET-0001" in saved
    assert "What legal rights" in saved


def test_thank_you_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/thank-you?id=LET-0001&response=anonymous")
    assert response.status_code == 200
    assert b"Question received." in response.data
