#!/usr/bin/env python3
"""
Module for managing session authentication.
"""

from typing import List, TypeVar
from flask import request
import os


class Auth:
    """
    Base class for handling authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        finds if a given path requires authentication.
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return True

    def authorization_header(self, request=None) -> str:
        """
        Fetches the Authorization header from the request.
        Returns:
            str: The value of the Authorization header,
            or None if not found or invalid.
        """
        if request is None:
            return None
        # Get the 'Authorization' header from the request
        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Fetches the current user based on the request.

        Returns:
            User: The user object associated with the request,
            or None if not available.
        """
        return None

    def session_cookie(self, request=None):
        """
        Fetches the session cookie from the request.
        Returns:
            str: The session cookie value,
            or None if not found.
        """
        if request is None:
            return None
        # Retrieve the session name from the environment variable
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
