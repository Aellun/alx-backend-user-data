import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with the wrong password."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """attempt to Log in with the correct credentials
    and return the session_id."""
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    response_data = response.json()
    assert "session_id" in response_data
    assert response_data["email"] == email
    assert response_data["message"] == "logged in"
    return response_data["session_id"]


def profile_unlogged() -> None:
    """Attempt to access the profile without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access the profile with a valid session ID."""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] is not None


def log_out(session_id: str) -> None:
    """Log out the user by destroying the session."""
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 302  # Expecting a redirect to the home page


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == email
    assert "reset_token" in response_data
    return response_data["reset_token"]


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Update the password using the reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password", data={
            "email": email, "reset_token": reset_token,
            "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
