from fastapi.testclient import TestClient


def test_me_requires_login(client: TestClient) -> None:
    res = client.get("/api/me")
    assert res.status_code == 401


def test_signup_login_logout_cycle(client: TestClient) -> None:
    res = client.post(
        "/api/auth/signup",
        json={"email": "teacher@example.com", "password": "password123", "role": "teacher"},
    )
    assert res.status_code == 200
    assert res.json()["role"] == "teacher"

    res = client.get("/api/me")
    assert res.status_code == 200
    assert res.json()["email"] == "teacher@example.com"

    res = client.post("/api/auth/logout")
    assert res.status_code == 200

    res = client.get("/api/me")
    assert res.status_code == 401


def test_student_cannot_create_classroom(client: TestClient) -> None:
    res = client.post(
        "/api/auth/signup",
        json={"email": "student@example.com", "password": "password123", "role": "student"},
    )
    assert res.status_code == 200

    res = client.post("/api/classrooms", json={"name": "Chinese 101"})
    assert res.status_code == 403

