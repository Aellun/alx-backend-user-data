#!/usr/bin/env python3
"""
Module for Session Expiration Authentication.
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing session
    authentication with expiration.
    """

    def __init__(self):
        """Initializes the session expiration authentication system."""
        super().__init__()
        try:
            # Set session_duration from environment variable
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID and stores the user session
        information along with creation time.

        Returns:
            str: The session ID created or
            None if session creation fails.
        """
        # Call the parent method to create a session ID
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session info as a dictionary containing user_id and created_at
        session_info = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_info

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        fetches user ID based on the session ID,
        checking for session expiration.

        Returns:
            str: The user ID or None
            if session ID is invalid or expired.
        """
        if session_id is None:
            return None

        # Retrieve the session dictionary from user_id_by_session_id
        session_info = self.user_id_by_session_id.get(session_id)
        if session_info is None:
            return None

        # If session_duration is 0 or negative, session never expires
        if self.session_duration <= 0:
            return session_info.get('user_id')

        # Check if session has expired
        created_at = session_info.get('created_at')
        if created_at is None:
            return None

        # Calculate expiration time
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        # Return the user_id if session is still valid
        return session_info.get('user_id')
