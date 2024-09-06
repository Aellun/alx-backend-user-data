#!/usr/bin/env python3
""" User module
"""
import hashlib
from models.base import Base
from models.user_session import UserSession


class User(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def create_user_session(self, session_id: str) -> UserSession:
        """
        Create a session for the user and store it in UserSession.
        Returns:
            UserSession: The created UserSession instance.
        """
        if session_id is None or self.id is None:
            return None
        user_session = UserSession(user_id=self.id, session_id=session_id)
        user_session.save()
        return user_session

    def get_user_session(self, session_id: str) -> UserSession:
        """
        Fetches an existing session for the user.
        Returns:
            UserSession: The UserSession instance, or None if not found.
        """
        sessions = UserSession.search({"session_id": session_id,
                                       "user_id": self.id})
        if sessions and len(sessions) > 0:
            return sessions[0]
        return None

    def destroy_user_session(self, session_id: str) -> bool:
        """
        Destroy the session by removing it from the UserSession model.
        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        session = self.get_user_session(session_id)
        if session:
            session.remove()
            return True
        return False
