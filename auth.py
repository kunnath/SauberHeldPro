"""
Authentication utilities for Aufraumenbee
"""

import streamlit as st
import bcrypt
import sqlite3
from typing import Optional, Dict

class AuthManager:
    def __init__(self, db_path: str = "aufraumenbee.db"):
        self.db_path = db_path
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate a user and return user info if successful"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT id, password_hash, role, full_name, email FROM users WHERE username = ?", 
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user and self.verify_password(password, user[1]):
            return {
                "id": user[0],
                "username": username,
                "role": user[2],
                "full_name": user[3],
                "email": user[4]
            }
        return None
    
    def create_user(self, username: str, password: str, role: str, 
                   full_name: str = "", email: str = "", phone: str = "") -> bool:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            password_hash = self.hash_password(password)
            
            conn.execute('''
                INSERT INTO users (username, password_hash, role, full_name, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, role, full_name, email, phone))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.authenticate_user(username, old_password)
        if not user:
            return False
        
        conn = sqlite3.connect(self.db_path)
        new_hash = self.hash_password(new_password)
        
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (new_hash, username)
        )
        
        conn.commit()
        conn.close()
        return True
    
    def has_permission(self, user_role: str, required_role: str) -> bool:
        """Check if user role has required permission"""
        role_hierarchy = {
            "customer": 1,
            "employee": 2,
            "manager": 3,
            "admin": 4
        }
        
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)

# Decorators for role-based access control
def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("Please log in to access this feature")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authenticated', False):
                st.error("Please log in to access this feature")
                return None
            
            user_role = st.session_state.get('user', {}).get('role', '')
            auth_manager = AuthManager()
            
            if not auth_manager.has_permission(user_role, required_role):
                st.error(f"Access denied. {required_role.title()} role required.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Session state management
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = None

def logout():
    """Clear session state and logout user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.last_activity = None
    st.rerun()

def check_session_timeout(timeout_minutes: int = 30):
    """Check if session has timed out"""
    import datetime
    
    if st.session_state.get('last_activity'):
        time_diff = datetime.datetime.now() - st.session_state.last_activity
        if time_diff.total_seconds() > (timeout_minutes * 60):
            logout()
    
    st.session_state.last_activity = datetime.datetime.now()
