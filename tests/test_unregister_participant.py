from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_the_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity = app.activities[activity_name]
    original_participants = list(activity["participants"])

    try:
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in activity["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activity["participants"] = original_participants
