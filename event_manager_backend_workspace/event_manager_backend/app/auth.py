"""Authentication helpers: registration, login, session token management."""

import secrets
from flask import request, jsonify, g
from functools import wraps
from .models import USERS

TOKENS = {}  # token -> username


# PUBLIC_INTERFACE
def register_user(username, password):
    """Register a new user. Returns True if created, False if exists."""
    if username in USERS:
        return False
    from .models import User
    USERS[username] = User(username, password)
    return True


# PUBLIC_INTERFACE
def authenticate_user(username, password):
    """Check username and password. Returns token string if valid, else None."""
    user = USERS.get(username)
    if user and user.check_password(password):
        token = secrets.token_hex(16)
        TOKENS[token] = username
        return token
    return None


# PUBLIC_INTERFACE
def get_current_user():
    """Returns current user from token, or None."""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    return TOKENS.get(token)


# PUBLIC_INTERFACE
def login_required(f):
    """Flask decorator to require login with Bearer token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        username = get_current_user()
        if not username:
            return jsonify({"message": "Authentication required"}), 401
        g.current_user = username
        return f(*args, **kwargs)
    return decorated


# PUBLIC_INTERFACE
def logout_user(token):
    """Log out (invalidate token)."""
    if token in TOKENS:
        del TOKENS[token]
        return True
    return False
