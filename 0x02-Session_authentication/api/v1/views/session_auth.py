#!/usr/bin/env python3
"""
Module for session-based authentication.
"""

from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from uuid import uuid4
import os
from api.v1.app import auth


class SessionAuth(Auth):
    """
    Class to manage creating and managing user sessions.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session ID for a given user ID.
        Returns:
            str: The newly generated session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Fetches the user ID associated with a given session ID.
        Returns:
            str: The associated user ID,
            or None if session ID is invalid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Fetchs the current user based on the session cookie from the request.
        Returns:
            User: The user associated with the session,
            or None if no valid session is found.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session associated with the request's session cookie.
        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login: Create a session for the user
    if credentials are valid.

    Returns:
        A JSON response with the user details and a session cookie set.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Email validation
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    # Password validation
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    try:
        users = User.search({"email": email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Password validation
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session and generate session ID
    session_id = auth.create_session(user.id)

    # Generate a response and set the session cookie
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
