#!/usr/bin/env python3
"""
Auth class for managing API authentication
"""
from typing import List, TypeVar
from flask import request

User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        Returns:
            boolean
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.
        Returns:
            str: Always returns None for now.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Get the current user from the request.
        Returns:
            User: Always returns None for now.
        """
        return None
