#!/usr/bin/env python3
"""
DB module for managing user operations
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class for interacting with the database"""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for interacting with the db
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the db.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The User object created and added to the db.
        """
        # Creates a new user instance
        new_user = User(email=email, hashed_password=hashed_password)

        # Adds the new user to the session
        self._session.add(new_user)

        # Commits the transaction to the db
        self._session.commit()

        # Returns the newly created user object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds the first user that matches the filters
        specified in the keyword arguments.

        Args:
            kwargs: Arbitrary keyword arguments representing the filters.

        Returns:
            User: The first user found that matches the criteria.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If the query contains invalid fields.
        """
        # Ensure that the kwargs are valid columns of the User model
        if not kwargs:
            raise InvalidRequestError("No keyword arguments provided")

        # Validate if the keyword args correspond
        # to valid fields in the User model
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid field: {key}")

        # Attempt to filter and return
        # the first user matching the criteria
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found matching the criteria")
            return user
        except NoResultFound as e:
            raise NoResultFound from e
        except Exception as e:
            raise InvalidRequestError(f"Error executing query: {e}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes and commits the changes
        to the database.
        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments representing
            the new attribute values.

        Returns:
            None

        Raises:
            ValueError: If a keyword argument
            does not correspond to a valid User attribute.
        """
        # Find the user by user_id
        user = self.find_user_by(id=user_id)

        # Loop through the keyword arguments and update
        # the user attributes
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        # Commit the changes to the database
        self._session.commit()
