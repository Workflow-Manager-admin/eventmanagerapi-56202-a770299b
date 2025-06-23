"""Defines in-memory model for Event."""

# In-memory event storage for demonstration purposes
EVENTS = {}
EVENT_COUNTER = [1]  # Mutable counter to simulate DB auto-increment


class Event:
    """Represents an event object."""
    def __init__(self, title, description, date, owner):
        self.id = EVENT_COUNTER[0]
        EVENT_COUNTER[0] += 1
        self.title = title
        self.description = description
        self.date = date
        self.owner = owner  # for now, always 'anonymous' or public

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "owner": self.owner,
        }
