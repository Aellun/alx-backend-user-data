#!/usr/bin/env python3
"""Password hashing module"""

import bcrypt


def _hash_password(password: str) -> str:
    """Hashes a password using bcrypt's hashpw with a salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password as a string.
    """
    # Encode the password string into bytes
    # Create the hashed password using bcrypt.hashpw
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Return the hashed password as string
    return hashed_password.decode('utf-8')
