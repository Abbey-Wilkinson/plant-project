"""
Script containing all of the custom errors.
"""


class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code


class DBConnectionError(Exception):
    """Describes an error triggered by a failing database connection."""

    def __init__(self, message: str, code: int):
        """Creates a new DBConnectionError instance."""
        self.message = message
        self.code = code
