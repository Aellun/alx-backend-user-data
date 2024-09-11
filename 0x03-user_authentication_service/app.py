#!/usr/bin/env python3
"""Flask app with user registration
"""


from flask import Flask, jsonify, request, abort, redirect, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """return a json payload with message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    post: route to register user
    form data: 'email', 'password'
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # regsiter user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Handles user login and session creation."""
    # Get the email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    # Check if the login credentials are valid
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create a new session for the user
    session_id = AUTH.create_session(email)

    if not session_id:
        abort(401)

    # Create a response with the success message
    response = make_response(jsonify({"email": email, "message": "logged in"}))

    # Set the session ID in a cookie
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Handles the DELETE /sessions route
    to log out a user by destroying their session.

    Steps:
    1. Fetches the session ID from the cookie.
    2. Find the user corresponding to the session ID.
    3. If the user exists, destroy the session and redirect to '/'.
    4. If no user is found, return a 403 status code.
    """
    # fetchs session ID from the cookies
    session_id = request.cookies.get("session_id")

    # If no session_id in cookies,
    # abort with 403 Forbidden
    if not session_id:
        abort(403)

    # Find the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)

    # If no user is found,
    # abort with 403 Forbidden
    if not user:
        abort(403)

    # Destroy the session for the found user
    AUTH.destroy_session(user.id)

    # Redirect to the home page
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    Handles the GET /profile route
    to retrieve a user's profile information.

    Steps:
    1. Fetches the session ID from the cookie.
    2. Find the user corresponding to the session ID.
    3. If the user exists, respond with the user's
    email in a JSON payload.
    4. If no user is found, return a 403 status code.
    """
    # Get the session ID from the cookies
    session_id = request.cookies.get("session_id")

    # If session_id is None, abort with 403 Forbidden
    if not session_id:
        abort(403)

    # Get the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)

    # Abort with 403 Forbidden If no user is found,
    if not user:
        abort(403)

    # Return a JSON response with the user's email
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """POST /reset_password
    Form data:
        - email: The user's email.
    Response:
        - Return reset token if email is valid.
        - Return 403 status if email is not registered.
    """
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        # Generate user reset token
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # Throw 403 error if user does not exist,
        abort(403)

    # Return the email and reset token in JSON format
    return jsonify({
        "email": email,
        "reset_token": reset_token
    }), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Handle the password update request."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400, description="Missing required form fields")

    try:
        # Update the password with the Auth class
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # respond with a 403 status code if an exception is raised,
        return jsonify({"message": "Invalid reset token"}), 403

    # If successful, respond with a 200 status code
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
