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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
