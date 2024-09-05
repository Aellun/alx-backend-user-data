#!/usr/bin/env python3
"""
Module for user login and session management views.
"""

import os
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    """
    Handles user login and session creation.
    Returns:
    - 200: Successfully authenticated,
    returns user details and sets the session cookie.
    - 400: If email or password is missing.
    - 404: If no user is found for the provided email.
    - 401: If the password is incorrect.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password presence
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if any user matches the provided password
    for user in users:
        if user.is_valid_password(password):
            # Import the authentication system and create a session
            from api.v1.app import auth
            session_id = auth.create_session(user.id)

            # Generate response and set session cookie
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME', 'session_id')
            resp.set_cookie(session_name, session_id)

            return resp

    # If no valid password is found for any user
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handles user logout and session destruction.
    Returns:
    - 200: Session successfully destroyed, returns an empty JSON response.
    - 404: If the session cookie is not found or
    the session cannot be destroyed.
    """
    from api.v1.app import auth

    # Attempt to destroy the session
    if auth.destroy_session(request):
        return jsonify({}), 200

    # Return 404 if session destruction failed
    abort(404)
