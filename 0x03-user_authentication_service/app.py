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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
