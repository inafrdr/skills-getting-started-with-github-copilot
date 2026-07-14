import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def save_activities():
    """Fixture to save and restore activities state for each test."""
    original_state = {}
    for activity_name, activity_data in app.activities.items():
        original_state[activity_name] = {
            "participants": list(activity_data["participants"])
        }
    
    yield
    
    for activity_name, activity_data in original_state.items():
        app.activities[activity_name]["participants"] = activity_data["participants"]
