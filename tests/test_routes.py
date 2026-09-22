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
