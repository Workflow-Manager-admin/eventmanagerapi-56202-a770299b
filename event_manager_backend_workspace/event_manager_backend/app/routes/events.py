"""Event API endpoints for event_manager_backend."""


from flask.views import MethodView
from flask_smorest import Blueprint
from ..schemas import (
    EventSchema, EventUpdateSchema
)
from ..models import EVENTS, Event


blp = Blueprint(
    "Events", "events", url_prefix="/api", description="Event CRUD API"
)

# -- Event endpoints (OPEN) --

@blp.route("/events")
class EventsListAPI(MethodView):
    """Create or list events."""

    @blp.arguments(EventSchema)
    def post(self, args):
        """Create new event. Owner is 'anonymous'."""
        owner = "anonymous"
        event = Event(
            title=args["title"],
            description=args["description"],
            date=args["date"],
            owner=owner
        )
        EVENTS[event.id] = event
        return {"message": "Event created", "event": event.as_dict()}, 201

    def get(self):
        """List all events."""
        all_events = [e.as_dict() for e in EVENTS.values()]
        return {"events": all_events}


@blp.route("/events/<int:event_id>")
class EventDetailAPI(MethodView):
    """Update, delete, or get a single event."""

    @blp.arguments(EventUpdateSchema)
    def patch(self, args, event_id):
        """Update fields of specified event (anyone can update)."""
        event = EVENTS.get(event_id)
        if not event:
            return {"message": "Event not found."}, 404
        for key in ["title", "description", "date"]:
            if key in args:
                setattr(event, key, args[key])
        return {"message": "Event updated.", "event": event.as_dict()}

    def delete(self, event_id):
        """Delete event by id (anyone can delete)."""
        event = EVENTS.get(event_id)
        if not event:
            return {"message": "Event not found."}, 404
        del EVENTS[event_id]
        return {"message": "Event deleted."}

    def get(self, event_id):
        """Get a single event by id."""
        event = EVENTS.get(event_id)
        if not event:
            return {"message": "Event not found."}, 404
        return {"event": event.as_dict()}
