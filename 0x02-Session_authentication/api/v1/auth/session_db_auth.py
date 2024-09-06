#!/usr/bin/env python3
"""
SessionDBAuth class to store sessions in the database.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that stores session IDs in a database.
    """

    def create_session(self, user_id=None):
        """
        Create a session and store it in the database (UserSession).
        Returns:
            str: The session ID, or None if the user_id is invalid.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create and store the UserSession object in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Fetches the user ID associated with a session ID from the database.
        Returns:
            str: The user ID, or None if the session is invalid or expired.
        """
        if session_id is None:
            return None

        # Search the database for the session ID
        sessions = UserSession.search({"session_id": session_id})
        if not sessions or len(sessions) == 0:
            return None

        session = sessions[0]  # Assuming one session ID is unique
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """
        Destroy a session by removing it from the database.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        # Search for the session in the database
        sessions = UserSession.search({"session_id": session_cookie})
        if not sessions or len(sessions) == 0:
            return False

        # Delete the session from the database
        session = sessions[0]
        session.remove()

        return True
