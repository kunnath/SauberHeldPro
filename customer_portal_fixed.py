"""
Clean Customer Portal for Aufraumenbee - Demo Ready
Fixed registration and login with minimal features
"""

import streamlit as st
import sqlite3
import hashlib
import bcrypt
import re
from datetime import datetime, date, timedelta
from typing import Optional, Dict, List
import time

# Set page config
st.set_page_config(
    page_title="Aufraumenbee - Customer Portal",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Logging stubs (simplified for demo)
try:
    from realtime_logger import log_user_action, log_error, log_database_operation
except ImportError:
    def log_user_action(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass
    def log_database_operation(*args, **kwargs): pass

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: transparent;
        border-radius: 8px;
        color: #666;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Database connection
def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('aufraumenbee.db', check_same_thread=False)

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create service_types table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            duration_hours INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create time_slots table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            booking_date DATE NOT NULL,
            status TEXT DEFAULT 'pending',
            special_instructions TEXT,
            total_price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (service_id) REFERENCES service_types (id),
            FOREIGN KEY (slot_id) REFERENCES time_slots (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Basic phone validation"""
    cleaned = re.sub(r'[^\d]', '', phone)
    return len(cleaned) >= 10

def register_customer(email: str, password: str, first_name: str, last_name: str, phone: str, address: str) -> bool:
    """Register a new customer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert customer
        cursor.execute('''
            INSERT INTO customers (first_name, last_name, email, phone, address, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, address, password_hash))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        log_error('customer_portal', e, {'email': email, 'error_type': 'registration_error'})
        return False

def authenticate_customer(email: str, password: str) -> Optional[Dict]:
    """Authenticate customer login"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE email = ? AND is_active = 1', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and verify_password(password, user[6]):  # user[6] is password_hash
            return {
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'email': user[3],
                'phone': user[4],
                'address': user[5]
            }
        return None
        
    except Exception as e:
        log_error('customer_portal', e, {'email': email, 'error_type': 'authentication_error'})
        return None

def check_email_exists(email: str) -> bool:
    """Check if email already exists in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM customers WHERE email = ?', (email,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception as e:
        log_error('customer_portal', e, {'email': email, 'error_type': 'email_check_error'})
        return False

def get_service_types() -> List[Dict]:
    """Get available service types"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM service_types WHERE is_active = 1')
        services = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': service[0],
                'name': service[1],
                'description': service[2],
                'price': service[3],
                'duration_hours': service[4]
            }
            for service in services
        ]
    except Exception as e:
        log_error('customer_portal', e, {'error_type': 'get_services_error'})
        return []

def show_header():
    """Show application header"""
    st.markdown('<h1 class="main-header">🧹 Aufraumenbee</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Professional Cleaning Services</p>', unsafe_allow_html=True)

def show_registration_form():
    """Simple customer registration form"""
    st.subheader("Create Your Account")
    st.markdown("📝 Fill out the form below to create your account")
    
    # Show success celebration if registration completed
    if st.session_state.get('registration_success', False):
        if st.session_state.get('registration_just_completed', False):
            st.balloons()
            st.snow()
            st.session_state.registration_just_completed = False
        
        customer_name = st.session_state.get('new_customer_name', 'Customer')
        customer_email = st.session_state.get('new_customer_email', '')
        
        st.success("🎉 **ACCOUNT CREATED SUCCESSFULLY!** 🎉")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        ">
            <h2 style="margin: 0 0 10px 0;">🌟 Welcome, {customer_name}! 🌟</h2>
            <p style="margin: 0; font-size: 16px;">Your account: <strong>{customer_email}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **🎯 Next Steps:**
        1. **Login** - Use your email and password
        2. **Book Service** - Choose your cleaning service
        3. **Enjoy** - Relax while we clean!
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 **LOGIN NOW**", use_container_width=True, type="primary"):
                st.session_state.registration_success = False
                st.session_state.login_email = customer_email
                st.rerun()
        
        with col2:
            if st.button("📝 **New Account**", use_container_width=True):
                st.session_state.registration_success = False
                for key in ['new_customer_name', 'new_customer_email']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        return
    
    # Registration form
    with st.form("simple_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", placeholder="Enter first name")
            email = st.text_input("Email *", placeholder="your.email@example.com")
            password = st.text_input("Password *", type="password", placeholder="Min 6 characters")
            
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Enter last name")
            phone = st.text_input("Phone *", placeholder="+1 (555) 123-4567")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password")
        
        address = st.text_area("Service Address *", placeholder="Enter complete address for cleaning services", height=80)
        terms = st.checkbox("I agree to Terms & Conditions *")
        
        submitted = st.form_submit_button("🚀 **CREATE ACCOUNT**", use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            errors = []
            
            if not first_name or not first_name.strip():
                errors.append("First Name required")
            if not last_name or not last_name.strip():
                errors.append("Last Name required")
            if not email or not email.strip():
                errors.append("Email required")
            elif not validate_email(email.strip()):
                errors.append("Valid email format required")
            if not phone or not phone.strip():
                errors.append("Phone number required")
            if not password or len(password) < 6:
                errors.append("Password must be at least 6 characters")
            if password != confirm_password:
                errors.append("Passwords must match")
            if not address or len(address.strip()) < 10:
                errors.append("Complete address required")
            if not terms:
                errors.append("Must accept terms & conditions")
            
            if errors:
                st.error("❌ **Please fix these issues:**")
                for error in errors:
                    st.error(f"• {error}")
                return
            
            # Check email availability
            if check_email_exists(email.strip()):
                st.error("❌ **Email already registered**")
                st.warning(f"The email **{email.strip()}** is already in use. Please use a different email.")
                if st.button("🔐 **Login Instead**", type="secondary"):
                    st.session_state.login_email = email.strip()
                    st.rerun()
                return
            
            # Create account
            st.success("✅ Creating your account...")
            
            with st.spinner("Processing..."):
                success = register_customer(
                    email.strip(),
                    password,
                    first_name.strip(),
                    last_name.strip(),
                    phone.strip(),
                    address.strip()
                )
                
                if success:
                    # Only set success state if data was actually stored
                    st.session_state.registration_success = True
                    st.session_state.registration_just_completed = True
                    st.session_state.new_customer_name = first_name.strip()
                    st.session_state.new_customer_email = email.strip()
                    
                    st.success(f"🎉 **SUCCESS!** Welcome, {first_name}!")
                    st.rerun()
                else:
                    st.error("❌ **Registration failed**")
                    st.error("Please try again or contact support if the problem persists.")

def show_login_form():
    """Simple login form for customers"""
    st.subheader("🔐 Login to Your Account")
    
    # Check if coming from registration
    default_email = st.session_state.get('login_email', '')
    if default_email:
        st.success(f"✅ **Ready to login with:** {default_email}")
    
    # Demo credentials info
    with st.expander("🧪 Demo Credentials", expanded=not default_email):
        st.info("""
        **Demo Account:**
        - 📧 Email: `demo.login@aufraumenbee.com`
        - 🔒 Password: `demo123`
        """)
    
    # Simple login form
    with st.form("simple_login", clear_on_submit=False):
        email = st.text_input(
            "Email Address", 
            placeholder="your.email@example.com",
            value=default_email
        )
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        login_submitted = st.form_submit_button("🔐 **LOGIN**", use_container_width=True, type="primary")
        
        if login_submitted:
            if not email or not password:
                st.error("❌ **Please enter both email and password**")
                return
            
            st.info("🔄 **Checking credentials...**")
            
            with st.spinner("Logging in..."):
                user = authenticate_customer(email.strip(), password)
                
                if user:
                    # Store user session
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    
                    # Clear login email
                    if 'login_email' in st.session_state:
                        del st.session_state['login_email']
                    
                    st.success(f"✅ **Welcome back, {user['first_name']}!**")
                    st.rerun()
                else:
                    st.error("❌ **Invalid email or password**")
                    st.error("Please check your credentials and try again.")

def show_customer_dashboard():
    """Simple customer dashboard"""
    user = st.session_state.user
    
    st.subheader(f"Welcome back, {user['first_name']}! 👋")
    
    # User info
    with st.expander("👤 **Account Information**", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {user['first_name']} {user['last_name']}")
            st.write(f"**Email:** {user['email']}")
        with col2:
            st.write(f"**Phone:** {user['phone']}")
            st.write(f"**Address:** {user['address']}")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 **Book Service**", use_container_width=True, type="primary"):
            st.session_state.current_page = 'booking'
            st.rerun()
    
    with col2:
        if st.button("📋 **My Bookings**", use_container_width=True):
            st.session_state.current_page = 'bookings'
            st.rerun()
    
    with col3:
        if st.button("🚪 **Logout**", use_container_width=True):
            # Clear session
            for key in ['user', 'authenticated', 'current_page']:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("✅ **Logged out successfully**")
            st.rerun()
    
    # Services overview
    st.markdown("### 🧹 Available Services")
    
    services = get_service_types()
    if services:
        for service in services:
            with st.container():
                st.markdown(f"""
                <div style="
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    border-left: 4px solid #4CAF50;
                ">
                    <h4 style="margin: 0 0 5px 0;">{service['name']}</h4>
                    <p style="margin: 0 0 10px 0; color: #666;">{service['description']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; color: #4CAF50;">${service['price']}</span>
                        <span style="color: #666;">{service['duration_hours']} hours</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📋 **No services available at the moment**")

def show_booking_form():
    """Simple booking form"""
    st.subheader("📅 Book a Service")
    
    if st.button("← **Back to Dashboard**", type="secondary"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.info("🚧 **Booking functionality coming soon!**")
    st.markdown("""
    **What you'll be able to do:**
    - Choose from available services
    - Select your preferred date and time
    - Add special instructions
    - Confirm your booking
    """)

def show_my_bookings():
    """Show customer bookings"""
    st.subheader("📋 My Bookings")
    
    if st.button("← **Back to Dashboard**", type="secondary"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.info("🚧 **Booking history coming soon!**")
    st.markdown("""
    **What you'll be able to see:**
    - Your upcoming bookings
    - Past service history
    - Booking status updates
    - Receipt downloads
    """)

def main():
    """Main application"""
    # Initialize database
    init_database()
    
    # Show header
    show_header()
    
    # Check authentication
    if st.session_state.get('authenticated', False):
        # User is logged in - show customer portal
        current_page = st.session_state.get('current_page', 'dashboard')
        
        if current_page == 'booking':
            show_booking_form()
        elif current_page == 'bookings':
            show_my_bookings()
        else:
            show_customer_dashboard()
    
    else:
        # User not logged in - show login/registration tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
        
        with tab1:
            show_login_form()
        
        with tab2:
            show_registration_form()

if __name__ == "__main__":
    main()
