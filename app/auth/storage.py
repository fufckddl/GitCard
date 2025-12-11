"""
Temporary in-memory state storage for OAuth flow.

SECURITY NOTE: The `state` parameter is used to prevent CSRF attacks.
We generate a random state value, store it server-side, and validate it
when GitHub redirects back to our callback endpoint.

In production, replace this with:
- Redis (recommended for distributed systems)
- Server-side session storage (e.g., Flask-Session, FastAPI-Session)
- Database-backed session store

The state should expire after a reasonable time (e.g., 10 minutes).
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional


# In-memory state store
# Key: state (str), Value: creation timestamp (datetime)
_state_store: Dict[str, datetime] = {}

# State expiration time (10 minutes)
STATE_EXPIRATION_MINUTES = 10


def generate_state() -> str:
    """
    Generate a random state value for OAuth flow.
    
    Returns:
        A UUID string to be used as the OAuth state parameter.
    """
    state = str(uuid.uuid4())
    _state_store[state] = datetime.utcnow()
    return state


def validate_state(state: str) -> bool:
    """
    Validate that the state exists and hasn't expired.
    
    Args:
        state: The state value to validate
        
    Returns:
        True if state is valid, False otherwise
    """
    if state not in _state_store:
        return False
    
    # Check expiration
    created_at = _state_store[state]
    expiration_time = created_at + timedelta(minutes=STATE_EXPIRATION_MINUTES)
    
    if datetime.utcnow() > expiration_time:
        # State expired, remove it
        del _state_store[state]
        return False
    
    # State is valid, remove it (one-time use)
    del _state_store[state]
    return True


def cleanup_expired_states():
    """
    Remove expired states from the store.
    Call this periodically in production (e.g., via background task).
    """
    now = datetime.utcnow()
    expired_states = [
        state
        for state, created_at in _state_store.items()
        if now > created_at + timedelta(minutes=STATE_EXPIRATION_MINUTES)
    ]
    for state in expired_states:
        del _state_store[state]

