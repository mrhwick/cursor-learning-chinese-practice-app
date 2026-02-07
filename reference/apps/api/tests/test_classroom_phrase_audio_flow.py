from fastapi.testclient import TestClient


def test_teacher_student_phrase_audio_and_feedback_flow(client: TestClient) -> None:
    # Teacher signup + create classroom
    res = client.post(
        "/api/auth/signup",
        json={"email": "teacher@example.com", "password": "password123", "role": "teacher"},
    )
    assert res.status_code == 200

    res = client.post("/api/classrooms", json={"name": "Chinese 101"})
    assert res.status_code == 200
    classroom = res.json()
    classroom_id = classroom["id"]
    invite_code = classroom["invite_code"]

    # Teacher creates phrase
    res = client.post(
        f"/api/classrooms/{classroom_id}/phrases",
        json={"chinese": "你好", "pinyin": "nǐ hǎo", "english": "Hello", "notes": None},
    )
    assert res.status_code == 200
    phrase = res.json()
    phrase_id = phrase["id"]

    # Upload invalid model audio
    res = client.post(
        f"/api/phrases/{phrase_id}/model-audio",
        files={"file": ("not-audio.txt", b"hello", "text/plain")},
    )
    assert res.status_code == 400

    # Upload valid model audio
    res = client.post(
        f"/api/phrases/{phrase_id}/model-audio",
        files={"file": ("model.wav", b"RIFF....WAVE", "audio/wav")},
    )
    assert res.status_code == 200

    # Logout teacher
    res = client.post("/api/auth/logout")
    assert res.status_code == 200

    # Student signup + join classroom
    res = client.post(
        "/api/auth/signup",
        json={"email": "student@example.com", "password": "password123", "role": "student"},
    )
    assert res.status_code == 200

    res = client.post("/api/classrooms/join", json={"invite_code": invite_code})
    assert res.status_code == 200
    assert res.json()["classroom_id"] == classroom_id

    # Student can list phrases
    res = client.get(f"/api/classrooms/{classroom_id}/phrases")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Student can fetch model audio
    res = client.get(f"/api/phrases/{phrase_id}/model-audio")
    assert res.status_code == 200

    # Student uploads submission (invalid content type)
    res = client.post(
        f"/api/phrases/{phrase_id}/submissions",
        files={"file": ("nope.txt", b"nope", "text/plain")},
    )
    assert res.status_code == 400

    # Student uploads submission (valid audio)
    res = client.post(
        f"/api/phrases/{phrase_id}/submissions",
        files={"file": ("attempt.webm", b"WEBM....", "audio/webm")},
    )
    assert res.status_code == 200
    submission_id = res.json()["id"]

    # Leave feedback
    res = client.post(
        f"/api/submissions/{submission_id}/feedback",
        json={"comment": "Good job", "score_tones": 4, "score_clarity": 5},
    )
    assert res.status_code == 200
    feedback_id = res.json()["id"]

    # List feedback
    res = client.get(f"/api/submissions/{submission_id}/feedback")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Student can delete own feedback
    res = client.delete(f"/api/feedback/{feedback_id}")
    assert res.status_code == 200

