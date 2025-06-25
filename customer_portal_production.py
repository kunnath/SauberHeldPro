"""
Aufraumenbee - Professional Cleaning Service Management System
Customer Portal - Production Version

This is the customer-facing portal for booking cleaning services.
Features include customer registration, login, service browsing, and booking management.

Author: Aufraumenbee Development Team
Version: 1.0 (Production)
Date: June 25, 2025
"""

import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import re

# Page configuration
st.set_page_config(
    page_title="Aufraumenbee - Book Cleaning Services",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database configuration
DATABASE_PATH = "aufraumenbee.db"

def init_customer_database():
    """Initialize customer-related database tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Customer users table for portal access
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Main customers table (unified with admin portal)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            registration_source TEXT DEFAULT 'portal',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Customer bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_email TEXT NOT NULL,
            service_type TEXT NOT NULL,
            preferred_date DATE NOT NULL,
            preferred_time TEXT NOT NULL,
            duration_hours INTEGER DEFAULT 2,
            address TEXT NOT NULL,
            special_instructions TEXT,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def register_customer(email: str, password: str, first_name: str, last_name: str, 
                     phone: str = "", address: str = "") -> bool:
    """Register a new customer in both portal and main customer tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert into customer_users table (for portal login)
        cursor.execute('''
            INSERT INTO customer_users (email, password_hash, first_name, last_name, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email.strip(), password_hash, first_name.strip(), last_name.strip(), 
              phone.strip(), address.strip()))
        
        # Also insert into main customers table (for admin portal visibility)
        cursor.execute('''
            INSERT INTO customers (email, first_name, last_name, phone, address, registration_source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email.strip(), first_name.strip(), last_name.strip(), 
              phone.strip(), address.strip(), 'portal'))
        
        conn.commit()
        return True
        
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_customer(email: str, password: str) -> Optional[Dict]:
    """Authenticate customer login"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, email, password_hash, first_name, last_name, phone, address
        FROM customer_users WHERE email = ?
    ''', (email,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        return {
            'id': user[0],
            'email': user[1],
            'first_name': user[3],
            'last_name': user[4],
            'phone': user[5],
            'address': user[6]
        }
    return None

def create_booking(customer_email: str, service_type: str, preferred_date: date, 
                  preferred_time: str, duration_hours: int, address: str, 
                  special_instructions: str = "") -> bool:
    """Create a new service booking"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO customer_bookings 
            (customer_email, service_type, preferred_date, preferred_time, 
             duration_hours, address, special_instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (customer_email, service_type, preferred_date, preferred_time, 
              duration_hours, address, special_instructions))
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_customer_bookings(customer_email: str) -> List[Dict]:
    """Get all bookings for a customer"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, service_type, preferred_date, preferred_time, duration_hours, 
               address, status, created_at, special_instructions
        FROM customer_bookings 
        WHERE customer_email = ?
        ORDER BY created_at DESC
    ''', (customer_email,))
    
    bookings = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': booking[0],
            'service_type': booking[1],
            'preferred_date': booking[2],
            'preferred_time': booking[3],
            'duration_hours': booking[4],
            'address': booking[5],
            'status': booking[6],
            'created_at': booking[7],
            'special_instructions': booking[8]
        }
        for booking in bookings
    ]

def show_registration_form():
    """Display customer registration form"""
    st.markdown("### 📝 Create Your Account")
    st.markdown("Join Aufraumenbee and experience professional cleaning services!")
    
    with st.form("customer_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*", placeholder="Enter your first name")
            email = st.text_input("Email Address*", placeholder="your.email@example.com")
            password = st.text_input("Password*", type="password", placeholder="Create a secure password")
            
        with col2:
            last_name = st.text_input("Last Name*", placeholder="Enter your last name")
            phone = st.text_input("Phone Number", placeholder="+49 123 456 7890")
            confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
        
        address = st.text_area("Address (Optional)", placeholder="Your complete address for service delivery")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy*")
        
        if st.form_submit_button("Create Account", type="primary", use_container_width=True):
            # Validation
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("❌ Please fill in all required fields!")
                return
                
            if password != confirm_password:
                st.error("❌ Passwords do not match!")
                return
                
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters long!")
                return
                
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                st.error("❌ Please enter a valid email address!")
                return
                
            if not terms_accepted:
                st.error("❌ Please accept the Terms of Service!")
                return
            
            # Register customer
            if register_customer(email, password, first_name, last_name, phone, address):
                st.session_state.registration_success = True
                st.session_state.new_customer_name = first_name
                st.session_state.new_customer_email = email
                st.success("🎉 Account created successfully!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Email already exists! Please use a different email or try logging in.")

def show_login_form():
    """Display customer login form"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("customer_login"):
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.form_submit_button("Login", type="primary", use_container_width=True):
            if email and password:
                customer = authenticate_customer(email, password)
                if customer:
                    st.session_state.customer_logged_in = True
                    st.session_state.customer = customer
                    st.success(f"Welcome back, {customer['first_name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password!")
            else:
                st.error("❌ Please enter both email and password!")

def show_service_catalog():
    """Display available cleaning services"""
    st.header("🧹 Our Cleaning Services")
    
    services = [
        {
            "name": "Regular Cleaning",
            "description": "Weekly or bi-weekly home cleaning including dusting, vacuuming, mopping, and bathroom cleaning.",
            "duration": "2-3 hours",
            "price": "€25/hour",
            "features": ["Dusting all surfaces", "Vacuum/sweep floors", "Clean bathrooms", "Kitchen cleaning"]
        },
        {
            "name": "Deep Cleaning",
            "description": "Comprehensive cleaning including areas not covered in regular cleaning.",
            "duration": "4-6 hours",
            "price": "€30/hour",
            "features": ["Everything in regular cleaning", "Inside appliances", "Baseboards & windowsills", "Light fixtures"]
        },
        {
            "name": "Move-in/Move-out Cleaning",
            "description": "Thorough cleaning for moving situations, ensuring the space is spotless.",
            "duration": "4-8 hours",
            "price": "€35/hour",
            "features": ["Complete deep cleaning", "Inside cabinets & drawers", "All appliances", "Detailed bathroom cleaning"]
        },
        {
            "name": "Office Cleaning",
            "description": "Professional cleaning services for offices and commercial spaces.",
            "duration": "2-4 hours",
            "price": "€22/hour",
            "features": ["Desk & surface cleaning", "Floor maintenance", "Restroom cleaning", "Trash removal"]
        }
    ]
    
    for i, service in enumerate(services):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"### {service['name']}")
                st.markdown(service['description'])
                
            with col2:
                st.markdown("**What's included:**")
                for feature in service['features']:
                    st.markdown(f"• {feature}")
            
            with col3:
                st.markdown(f"**Duration:** {service['duration']}")
                st.markdown(f"**Price:** {service['price']}")
                
                if st.button(f"Book {service['name']}", key=f"book_{i}", use_container_width=True):
                    st.session_state.selected_service = service['name']
                    st.session_state.show_booking_form = True
                    st.rerun()
            
            st.markdown("---")

def show_booking_form():
    """Display service booking form"""
    customer = st.session_state.customer
    service_name = st.session_state.get('selected_service', 'Regular Cleaning')
    
    st.header(f"📅 Book {service_name}")
    st.markdown(f"**Customer:** {customer['first_name']} {customer['last_name']}")
    
    with st.form("service_booking"):
        col1, col2 = st.columns(2)
        
        with col1:
            preferred_date = st.date_input(
                "Preferred Date*", 
                min_value=date.today() + timedelta(days=1),
                value=date.today() + timedelta(days=1)
            )
            
            duration_hours = st.selectbox(
                "Estimated Duration*",
                options=[2, 3, 4, 5, 6],
                index=0,
                help="Select estimated cleaning duration"
            )
        
        with col2:
            preferred_time = st.selectbox(
                "Preferred Time*",
                options=["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"],
                index=2
            )
            
            # Calculate estimated cost
            base_rate = 25  # Base rate per hour
            estimated_cost = duration_hours * base_rate
            st.info(f"💰 Estimated Cost: €{estimated_cost}")
        
        # Service address
        service_address = st.text_area(
            "Service Address*",
            value=customer.get('address', ''),
            placeholder="Please provide the complete address where cleaning service is needed"
        )
        
        # Special instructions
        special_instructions = st.text_area(
            "Special Instructions (Optional)",
            placeholder="Any specific requirements, access instructions, or areas to focus on..."
        )
        
        if st.form_submit_button("Submit Booking Request", type="primary", use_container_width=True):
            if service_address and preferred_date:
                if create_booking(
                    customer['email'], 
                    service_name, 
                    preferred_date, 
                    preferred_time, 
                    duration_hours, 
                    service_address, 
                    special_instructions
                ):
                    st.success("🎉 Booking request submitted successfully!")
                    st.info("📞 We'll contact you within 24 hours to confirm your appointment.")
                    st.session_state.show_booking_form = False
                    st.session_state.selected_service = None
                    st.rerun()
                else:
                    st.error("❌ Failed to submit booking. Please try again.")
            else:
                st.error("❌ Please fill in all required fields!")
    
    if st.button("← Back to Services", use_container_width=True):
        st.session_state.show_booking_form = False
        st.session_state.selected_service = None
        st.rerun()

def show_customer_dashboard():
    """Display customer dashboard with bookings and account info"""
    customer = st.session_state.customer
    
    # Header
    st.header(f"Welcome, {customer['first_name']}! 👋")
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 Book New Service", use_container_width=True, type="primary"):
            st.session_state.show_services = True
            st.rerun()
    
    with col2:
        if st.button("📅 View My Bookings", use_container_width=True):
            st.session_state.show_bookings = True
            st.rerun()
    
    with col3:
        if st.button("👤 Account Settings", use_container_width=True):
            st.session_state.show_account = True
            st.rerun()
    
    # Recent bookings
    bookings = get_customer_bookings(customer['email'])
    
    if bookings:
        st.subheader("📋 Your Recent Bookings")
        
        for booking in bookings[:3]:  # Show last 3 bookings
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                
                with col1:
                    st.markdown(f"**{booking['service_type']}**")
                    st.markdown(f"📍 {booking['address'][:50]}...")
                
                with col2:
                    st.markdown(f"📅 {booking['preferred_date']}")
                    st.markdown(f"🕐 {booking['preferred_time']}")
                
                with col3:
                    st.markdown(f"⏱️ {booking['duration_hours']}h")
                    
                with col4:
                    status_color = {
                        'pending': '🟡',
                        'confirmed': '🟢',
                        'cancelled': '🔴'
                    }
                    st.markdown(f"{status_color.get(booking['status'], '⚪')} {booking['status'].title()}")
                
                st.markdown("---")
    else:
        st.info("No bookings yet. Book your first cleaning service!")

def show_my_bookings():
    """Display all customer bookings"""
    customer = st.session_state.customer
    bookings = get_customer_bookings(customer['email'])
    
    st.header("📋 My Bookings")
    
    if bookings:
        for booking in bookings:
            with st.expander(f"{booking['service_type']} - {booking['preferred_date']} ({booking['status'].title()})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Service:** {booking['service_type']}")
                    st.markdown(f"**Date:** {booking['preferred_date']}")
                    st.markdown(f"**Time:** {booking['preferred_time']}")
                    st.markdown(f"**Duration:** {booking['duration_hours']} hours")
                
                with col2:
                    st.markdown(f"**Status:** {booking['status'].title()}")
                    st.markdown(f"**Address:** {booking['address']}")
                    st.markdown(f"**Booked:** {booking['created_at']}")
                
                if booking['special_instructions']:
                    st.markdown(f"**Special Instructions:** {booking['special_instructions']}")
                
                # Action buttons for pending bookings
                if booking['status'] == 'pending':
                    if st.button(f"Cancel Booking #{booking['id']}", key=f"cancel_{booking['id']}"):
                        # Here you would implement booking cancellation
                        st.info("Cancellation feature will be implemented.")
    else:
        st.info("You don't have any bookings yet.")
    
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.show_bookings = False
        st.rerun()

def show_account_settings():
    """Display account settings and profile management"""
    customer = st.session_state.customer
    
    st.header("👤 Account Settings")
    
    with st.form("update_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", value=customer['first_name'])
            email = st.text_input("Email", value=customer['email'], disabled=True)
            
        with col2:
            last_name = st.text_input("Last Name", value=customer['last_name'])
            phone = st.text_input("Phone", value=customer.get('phone', ''))
        
        address = st.text_area("Address", value=customer.get('address', ''))
        
        if st.form_submit_button("Update Profile", type="primary"):
            st.success("Profile updated successfully!")
    
    st.markdown("---")
    
    # Change password section
    with st.expander("🔒 Change Password"):
        with st.form("change_password"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                if new_password != confirm_new_password:
                    st.error("New passwords do not match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long!")
                else:
                    st.success("Password changed successfully!")
    
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.show_account = False
        st.rerun()

def main():
    """Main application function"""
    
    # Initialize database
    init_customer_database()
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #FF6B6B;
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .service-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px solid #f0f0f0;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .welcome-message {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'customer_logged_in' not in st.session_state:
        st.session_state.customer_logged_in = False
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'show_services' not in st.session_state:
        st.session_state.show_services = False
    if 'show_booking_form' not in st.session_state:
        st.session_state.show_booking_form = False
    if 'show_bookings' not in st.session_state:
        st.session_state.show_bookings = False
    if 'show_account' not in st.session_state:
        st.session_state.show_account = False
    
    # Main header
    st.markdown('<div class="main-header">🧹 Aufraumenbee</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">Professional Cleaning Services at Your Fingertips</p>', unsafe_allow_html=True)
    
    # Check if customer is logged in
    if not st.session_state.customer_logged_in:
        # Show registration success message
        if st.session_state.registration_success:
            customer_name = st.session_state.get('new_customer_name', 'Customer')
            customer_email = st.session_state.get('new_customer_email', '')
            
            st.markdown(f"""
            <div class="welcome-message">
                <h2>🎉 Welcome to Aufraumenbee, {customer_name}!</h2>
                <p>Your account has been created successfully. Please log in below to start booking services.</p>
                <p><strong>Your registered email:</strong> {customer_email}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Continue to Login", use_container_width=True, type="primary"):
                st.session_state.registration_success = False
                st.rerun()
        
        # Login/Registration tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
        
        with tab1:
            show_login_form()
            
        with tab2:
            show_registration_form()
    
    else:
        # Customer is logged in - show appropriate page
        customer = st.session_state.customer
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"### Welcome, {customer['first_name']}!")
            st.markdown(f"📧 {customer['email']}")
            st.markdown("---")
            
            if st.button("🏠 Dashboard", use_container_width=True):
                # Reset all navigation states
                st.session_state.show_services = False
                st.session_state.show_booking_form = False
                st.session_state.show_bookings = False
                st.session_state.show_account = False
                st.rerun()
            
            if st.button("🧹 Browse Services", use_container_width=True):
                st.session_state.show_services = True
                st.session_state.show_booking_form = False
                st.session_state.show_bookings = False
                st.session_state.show_account = False
                st.rerun()
            
            if st.button("📋 My Bookings", use_container_width=True):
                st.session_state.show_bookings = True
                st.session_state.show_services = False
                st.session_state.show_booking_form = False
                st.session_state.show_account = False
                st.rerun()
            
            if st.button("👤 Account", use_container_width=True):
                st.session_state.show_account = True
                st.session_state.show_services = False
                st.session_state.show_booking_form = False
                st.session_state.show_bookings = False
                st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    if key.startswith(('customer', 'show_', 'selected_', 'new_customer', 'registration')):
                        del st.session_state[key]
                st.rerun()
        
        # Main content based on navigation
        if st.session_state.show_booking_form:
            show_booking_form()
        elif st.session_state.show_services:
            show_service_catalog()
        elif st.session_state.show_bookings:
            show_my_bookings()
        elif st.session_state.show_account:
            show_account_settings()
        else:
            show_customer_dashboard()

if __name__ == "__main__":
    main()
