import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    assert "<title>Mergington High School" in response.text

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball Team" in data
    assert "Soccer Club" in data

@pytest.mark.parametrize("activity,email", [
    ("Basketball Team", "newstudent@mergington.edu"),
    ("Soccer Club", "anotherstudent@mergington.edu")
])
def test_signup_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

@pytest.mark.parametrize("activity,email", [
    ("Basketball Team", "james@mergington.edu"),
    ("Soccer Club", "liam@mergington.edu")
])
def test_unregister_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Try unregistering again (should fail)
    response2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response2.status_code == 400
    assert "Participant not found" in response2.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
