#!/usr/bin/env python3
"""Password hashing module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


class Auth:
    """Auth class to interact with the authentication db."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hashes a password using bcrypt's hashpw with a salt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted, hashed password as a string.
        """
        # Encode the password string into bytes
        # Create the hashed password using bcrypt.hashpw
        hashed_password = bcrypt.hashpw(
              password.encode('utf-8'), bcrypt.gensalt())

        # Return the hashed password as string
        return hashed_password.decode('utf-8')

    def register_user(self, email: str, password: str) -> User:
        """Register a user with a given email and password.

            Args:
                email (str): User's email address.
                password (str): User's password

            Raises:
                ValueError: If the user with the
                provided email already exists.

            Returns:
                User: The newly created User object.
            """
        try:
            # Attempt to find the user with the given email
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        # If no user is found, add the user to the database
        hashed_password = self._hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a login attempt.

        Args:
            email (str): The user's email.
            password (str): The password provided.

        Returns:
            bool: True if the login is successful, False otherwise.
        """
        try:
            # try to locate the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Return False if no user is found
            return False

            # Check if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8'))
