#!/usr/bin/env python3
"""
SQLAlchemy model for the users table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Declare a base class for our models
Base = declarative_base()

class User(Base):
    """
    users table model
    
    Attributes:
        id (int): The primary key of the user.
        email (str): The email of the user
        hashed_password (str):hashed password of the user.
        session_id (str): Nullable session ID for user sessions.
        reset_token (str): Nullable reset token for password resets.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        String representation of the User instance.
        """
        return f"<User(id={self.id}, email={self.email})>"

