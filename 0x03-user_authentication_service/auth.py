#!/usr/bin/env python3
"""Password hashing module"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt's hashpw with a salt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The salted, hashed password as a string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: A string representation of a new UUID.
    """
    id = uuid4()
    return str(id)


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

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user with the given email.
        Args:
            email (str): The user's email.
        Returns:
            str: The session ID.
        Raises:
            NoResultFound: If no user is found with the given email.
        """
        try:
            # Finds the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # raise an exception If no user is found,
            return None

        # Generate a new session ID (UUID)
        session_id = _generate_uuid()

        # Update the user's session_id in the db
        self._db.update_user(user.id, session_id=session_id)

        # Return the new session ID
        return session_id

    def get_user_from_session_id(
            self, session_id: Optional[str]) -> Optional[User]:
        """
        Takes a session_id string and returns the corresponding User or None.
        Returns:
            Optional[User]: The user associated with the session ID,
            or None if not found.
        """
        if session_id is None:
            return None

        try:
            # find the user by session_id
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # Return None if no user is found
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Takes a user_id and updates the user's session ID to None.
        Returns:
            None
        """
        try:
            # Find user user_id
            user = self._db.find_user_by(id=user_id)

        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Gets a user by email and generates a password reset token.
        Returns:
            str: The generated reset token (UUID).

        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # if user is not found, Raise a ValueError
            # Generate a new UUID token
            # Update the user's reset_token field with the new token
            # Return the generated token
        except NoResultFound:
            raise ValueError
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password using the reset_token.
        Raises:
            ValueError: If no user is found with the reset_token.
        """
        try:
            # Gets the user by the reset_token
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # Raise a ValueError if the reset_token is invalid,
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = self._hash_password(password)

        # Update the user's password and reset_token to None
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)
