from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test retrieving all activities"""
    # Arrange - no special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    email = "test_success@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in result["message"]

    # Verify participant was added
    response2 = client.get("/activities")
    assert email in response2.json()[activity]["participants"]


def test_signup_duplicate():
    """Test signing up for an activity when already registered"""
    # Arrange
    email = "test_duplicate@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_activity_not_found():
    """Test signing up for a non-existent activity"""
    # Arrange
    email = "test_notfound@mergington.edu"
    activity = "Nonexistent Activity"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_delete_success():
    """Test successful unregistration from an activity"""
    # Arrange
    email = "test_delete_success@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")  # Signup first

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert email in result["message"]

    # Verify participant was removed
    response2 = client.get("/activities")
    assert email not in response2.json()[activity]["participants"]


def test_delete_not_signed_up():
    """Test unregistering when not signed up"""
    # Arrange
    email = "test_delete_not_signed@mergington.edu"
    activity = "Programming Class"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]


def test_delete_activity_not_found():
    """Test unregistering from a non-existent activity"""
    # Arrange
    email = "test_delete_notfound@mergington.edu"
    activity = "Nonexistent Activity"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]