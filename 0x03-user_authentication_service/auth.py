#!/usr/bin/env python3
"""Password hashing module"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt's hashpw with a salt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted, hashed password as a string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication db.
    """

    def __init__(self):
        """_summary_
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
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
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add user to database
            return self._db.add_user(email, _hash_password(password))

        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))

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
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def _generate_uuid() -> str:
        """
        Generates a new UUID.

        Returns:
            str: A string representation of a new UUID.
        """
        id = uuid4()
        return str(id)
