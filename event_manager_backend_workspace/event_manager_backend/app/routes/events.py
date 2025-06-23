"""Event and authentication API endpoints for event_manager_backend."""

from flask import request, g
from flask.views import MethodView
from flask_smorest import Blueprint
from ..schemas import (
    RegisterSchema, LoginSchema,
    EventSchema, EventUpdateSchema
)
from ..models import EVENTS, Event
from ..auth import (
    register_user, authenticate_user, login_required, logout_user
)

blp = Blueprint(
    "Events", "events", url_prefix="/api", description="Event CRUD and Auth API"
)

# -- Auth endpoints --

# -- Auth endpoints --

@blp.route("/register")
class RegisterAPI(MethodView):
    """Endpoint for user registration."""

    @blp.arguments(RegisterSchema)
    def post(self, args):
        """Register a new user."""
        success = register_user(args["username"], args["password"])
        if not success:
            return {"message": "User already exists."}, 409
        return {"message": "User registered successfully."}, 201


@blp.route("/login")
class LoginAPI(MethodView):
    """Endpoint for user login."""

    @blp.arguments(LoginSchema)
    def post(self, args):
        """Issue token if username/password valid."""
        token = authenticate_user(args["username"], args["password"])
        if not token:
            return {"message": "Invalid username or password."}, 401
        return {"token": token}


@blp.route("/logout")
class LogoutAPI(MethodView):
    """Endpoint for user logout."""

    @login_required
    def post(self):
        """Invalidate current Bearer token."""
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")
        if logout_user(token):
            return {"message": "Logged out."}
        return {"message": "Invalid token."}, 401

# -- Event endpoints (require auth) --


@blp.route("/events")
class EventsListAPI(MethodView):
    """Create or list events."""

    @login_required
    @blp.arguments(EventSchema)
    def post(self, args):
        """Create new event. Owner is logged-in user."""
        owner = g.current_user
        event = Event(
            title=args["title"],
            description=args["description"],
            date=args["date"],
            owner=owner
        )
        EVENTS[event.id] = event
        return {"message": "Event created", "event": event.as_dict()}, 201

    @login_required
    def get(self):
        """List events owned by current user."""
        owner = g.current_user
        my_events = [e.as_dict() for e in EVENTS.values() if e.owner == owner]
        return {"events": my_events}


@blp.route("/events/<int:event_id>")
class EventDetailAPI(MethodView):
    """Update or delete a single event."""

    @login_required
    @blp.arguments(EventUpdateSchema)
    def patch(self, args, event_id):
        """Update fields of specified event if owned by user."""
        owner = g.current_user
        event = EVENTS.get(event_id)
        if not event or event.owner != owner:
            return {"message": "Not found or unauthorized."}, 404
        for key in ["title", "description", "date"]:
            if key in args:
                setattr(event, key, args[key])
        return {"message": "Event updated.", "event": event.as_dict()}

    @login_required
    def delete(self, event_id):
        """Delete event by id if owned by user."""
        owner = g.current_user
        event = EVENTS.get(event_id)
        if not event or event.owner != owner:
            return {"message": "Not found or unauthorized."}, 404
        del EVENTS[event_id]
        return {"message": "Event deleted."}

    @login_required
    def get(self, event_id):
        """Get a single event by id (owned by user)."""
        owner = g.current_user
        event = EVENTS.get(event_id)
        if not event or event.owner != owner:
            return {"message": "Not found or unauthorized."}, 404
        return {"event": event.as_dict()}
