"""Backend tests for activities endpoints."""

from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities_returns_all_activities():
    """Test retrieving all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert activities["Chess Club"]["max_participants"] == 12
    assert len(activities["Chess Club"]["participants"]) > 0


def test_signup_for_activity_adds_participant(save_activities):
    """Test signing up a student for an activity."""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity = app.activities[activity_name]
    initial_count = len(activity["participants"])
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activity["participants"]
    assert len(activity["participants"]) == initial_count + 1


def test_signup_for_nonexistent_activity_returns_404():
    """Test signing up for an activity that doesn't exist."""
    response = client.post(
        "/activities/NonexistentActivity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_returns_400(save_activities):
    """Test that signing up twice for the same activity fails."""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_participant_removes_email(save_activities):
    """Test removing a participant from an activity."""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity = app.activities[activity_name]
    
    assert email in activity["participants"]
    
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activity["participants"]


def test_unregister_nonexistent_participant_returns_400(save_activities):
    """Test removing a participant who is not signed up."""
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_from_nonexistent_activity_returns_404():
    """Test removing from an activity that doesn't exist."""
    response = client.delete(
        "/activities/NonexistentActivity/participants",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
