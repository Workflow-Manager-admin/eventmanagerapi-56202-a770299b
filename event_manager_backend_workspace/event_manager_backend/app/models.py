"""Defines SQLAlchemy models for User and Event"""
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory data storage for demonstration purposes
USERS = {}
EVENTS = {}
EVENT_COUNTER = [1]  # Mutable counter to simulate DB auto-increment


class User:
    """Represents a user with basic authentication."""
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event:
    """Represents an event object."""
    def __init__(self, title, description, date, owner):
        self.id = EVENT_COUNTER[0]
        EVENT_COUNTER[0] += 1
        self.title = title
        self.description = description
        self.date = date
        self.owner = owner  # username

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "owner": self.owner,
        }
