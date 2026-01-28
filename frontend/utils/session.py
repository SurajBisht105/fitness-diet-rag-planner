# frontend/utils/session.py
"""Session management utilities."""

import streamlit as st
from typing import Any, Optional


class SessionManager:
    """Manages Streamlit session state."""
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a value from session state."""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set a value in session state."""
        st.session_state[key] = value
    
    @staticmethod
    def delete(key: str) -> None:
        """Delete a key from session state."""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def clear() -> None:
        """Clear all session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def get_user_id() -> Optional[str]:
        """Get current user ID."""
        return st.session_state.get("user_id")
    
    @staticmethod
    def set_user(user_id: str, user_data: dict) -> None:
        """Set current user."""
        st.session_state["user_id"] = user_id
        st.session_state["user_data"] = user_data
    
    @staticmethod
    def clear_user() -> None:
        """Clear current user."""
        SessionManager.delete("user_id")
        SessionManager.delete("user_data")
    
    @staticmethod
    def is_logged_in() -> bool:
        """Check if user is logged in."""
        return st.session_state.get("user_id") is not None