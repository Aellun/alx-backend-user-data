#!/usr/bin/env python3
"""
Module for session authentication.
"""

from .auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    Manages user sessions using session IDs for authentication.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for a given user ID.
        Returns:
            str: The newly created session ID,
            or None if the user ID is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Fetches the user ID associated with a given session ID.
        Returns:
            str: The user ID associated with the session ID,
            or None if the session ID is invalid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Fetches the user associated with the current session
        based on the request's session cookie.

        Returns:
            User: The user object associated with the current session,
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
