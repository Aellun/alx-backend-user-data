#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Return a JSON payload with message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users:route to register a user.

    Form data: 'email', 'password'
    """
    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    # # Validate that both email and password are provided
    # if not email or not password:
    #     return jsonify({"message": "Missing email or password"}), 400

    try:
        # Try to register the user using the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        # If the user is already registered, return a 400 response
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
