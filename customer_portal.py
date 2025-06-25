"""
Public Customer Portal for Aufraumenbee Cleaning Service
Allows customers to register, login, and book cleaning services
"""

import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import re

# Import real-time logging system
try:
    from realtime_logger import get_realtime_logger, log_user_action, log_error, log_database_operation
    LOGGING_ENABLED = True
except ImportError:
    LOGGING_ENABLED = False
    # Fallback functions
    def log_user_action(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass
    def log_database_operation(*args, **kwargs): pass

# Page configuration
st.set_page_config(
    page_title="Aufraumenbee - Book Cleaning Services",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize logging
if LOGGING_ENABLED:
    logger = get_realtime_logger()
    log_user_action('customer_portal', 'portal_access', {'timestamp': datetime.now().isoformat()})

# Custom CSS for better styling
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
        transition: border-color 0.3s, transform 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .service-card:hover {
        border-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .price-tag {
        color: #FF6B6B;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .available-slot {
        background: #4ECDC4;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem;
        text-align: center;
    }
    .unavailable-slot {
        background: #ccc;
        color: #666;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem;
        text-align: center;
    }
    .booking-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Success animation keyframes */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .success-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 12px 24px;
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def init_database():
    """Initialize database connection"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    
    # Create customer users table if not exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customer_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Create service types table if not exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS service_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            base_price REAL NOT NULL,
            duration_minutes INTEGER NOT NULL,
            category TEXT,
            active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create time slots table if not exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            available BOOLEAN DEFAULT TRUE,
            employee_id INTEGER,
            max_bookings INTEGER DEFAULT 1,
            current_bookings INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customer bookings table if not exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customer_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_user_id INTEGER NOT NULL,
            service_type_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            date DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            address TEXT NOT NULL,
            special_instructions TEXT,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_user_id) REFERENCES customer_users (id),
            FOREIGN KEY (service_type_id) REFERENCES service_types (id),
            FOREIGN KEY (slot_id) REFERENCES time_slots (id)
        )
    ''')
    
    # Insert default service types if table is empty
    cursor = conn.execute("SELECT COUNT(*) FROM service_types")
    if cursor.fetchone()[0] == 0:
        default_services = [
            ("Regular Cleaning", "Standard house cleaning including dusting, vacuuming, mopping, and bathroom cleaning", 80.0, 120, "Residential"),
            ("Deep Cleaning", "Thorough cleaning including inside appliances, baseboards, and detailed cleaning", 150.0, 240, "Residential"), 
            ("Move-in/Move-out Cleaning", "Complete cleaning for moving situations including inside cabinets and appliances", 200.0, 300, "Residential"),
            ("Office Cleaning", "Professional office space cleaning including desks, meeting rooms, and common areas", 100.0, 180, "Commercial"),
            ("Post-Construction Cleaning", "Specialized cleaning after construction or renovation work", 250.0, 360, "Specialty"),
            ("Carpet Cleaning", "Professional carpet cleaning and stain removal", 120.0, 150, "Specialty"),
            ("Window Cleaning", "Interior and exterior window cleaning service", 80.0, 90, "Specialty")
        ]
        
        for service in default_services:
            conn.execute('''
                INSERT INTO service_types (name, description, base_price, duration_minutes, category)
                VALUES (?, ?, ?, ?, ?)
            ''', service)
    
    conn.commit()
    return conn

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
    """Validate phone number format"""
    pattern = r'^\+?[\d\s\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None

def register_customer(email: str, password: str, first_name: str, last_name: str, phone: str, address: str) -> bool:
    """Register new customer with enhanced error handling"""
    try:
        # Log the registration attempt
        log_database_operation('INSERT', 'customer_users', {
            'action': 'register_customer_attempt',
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        
        conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT email FROM customer_users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            log_error('customer_portal', 'Email already exists', {
                'email': email,
                'error_type': 'duplicate_email'
            })
            conn.close()
            return False
        
        # Hash password and insert new user
        password_hash = hash_password(password)
        
        # Insert into customer_users table (for portal login)
        cursor.execute('''
            INSERT INTO customer_users (email, password_hash, first_name, last_name, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, password_hash, first_name, last_name, phone, address))
        
        # Also insert into customers table (for admin management)
        full_name = f"{first_name} {last_name}".strip()
        cursor.execute('''
            INSERT INTO customers (name, email, phone, address, preferences)
            VALUES (?, ?, ?, ?, ?)
        ''', (full_name, email, phone, address, "Registered via customer portal"))
        
        conn.commit()
        
        # Verify the insertion
        user_id = cursor.lastrowid
        log_user_action('customer_portal', 'customer_registered_successfully', {
            'user_id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })
        
        conn.close()
        return True
        
    except sqlite3.IntegrityError as e:
        # Log registration failure
        log_error('customer_portal', e, {
            'email': email,
            'error_type': 'database_integrity_error',
            'error_message': str(e)
        })
        if 'conn' in locals():
            conn.close()
        return False
    except Exception as e:
        # Log unexpected error
        log_error('customer_portal', e, {
            'email': email,
            'error_type': 'unexpected_registration_error',
            'error_message': str(e)
        })
        if 'conn' in locals():
            conn.close()
        return False

def authenticate_customer(email: str, password: str) -> Optional[Dict]:
    """Authenticate customer login"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    cursor = conn.execute('''
        SELECT id, password_hash, first_name, last_name, phone, address
        FROM customer_users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[1]):
        return {
            'id': user[0],
            'email': email,
            'first_name': user[2],
            'last_name': user[3],
            'phone': user[4],
            'address': user[5]
        }
    return None

def get_service_types() -> List[Dict]:
    """Get all active service types"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    cursor = conn.execute('''
        SELECT id, name, description, base_price, duration_minutes, category
        FROM service_types WHERE active = TRUE
        ORDER BY category, name
    ''')
    services = []
    for row in cursor.fetchall():
        services.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'base_price': row[3],
            'duration_minutes': row[4],
            'category': row[5]
        })
    conn.close()
    return services
    return services

def get_available_slots(selected_date: date, service_duration: int) -> List[Dict]:
    """Get available time slots for a specific date"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    
    # First, get existing slots for the date
    cursor = conn.execute('''
        SELECT id, start_time, end_time, current_bookings, max_bookings
        FROM time_slots 
        WHERE date = ? AND available = TRUE
        ORDER BY start_time
    ''', (selected_date.strftime('%Y-%m-%d'),))
    
    existing_slots = cursor.fetchall()
    
    # If no slots exist for this date, generate default slots
    if not existing_slots:
        generate_default_slots(selected_date)
        # Re-fetch after generating
        cursor = conn.execute('''
            SELECT id, start_time, end_time, current_bookings, max_bookings
            FROM time_slots 
            WHERE date = ? AND available = TRUE
            ORDER BY start_time
        ''', (selected_date.strftime('%Y-%m-%d'),))
        existing_slots = cursor.fetchall()
    
    available_slots = []
    for slot in existing_slots:
        if slot[3] < slot[4]:  # current_bookings < max_bookings
            available_slots.append({
                'id': slot[0],
                'start_time': slot[1],
                'end_time': slot[2],
                'display_time': f"{slot[1]} - {slot[2]}"
            })
    
    conn.close()
    return available_slots

def generate_default_slots(selected_date: date):
    """Generate default time slots for a date"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    
    # Generate slots from 8 AM to 6 PM, 2-hour intervals
    time_slots = [
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("12:00", "14:00"),
        ("14:00", "16:00"),
        ("16:00", "18:00")
    ]
    
    for start_time, end_time in time_slots:
        try:
            conn.execute('''
                INSERT INTO time_slots (date, start_time, end_time, available, max_bookings)
                VALUES (?, ?, ?, TRUE, 2)
            ''', (selected_date.strftime('%Y-%m-%d'), start_time, end_time))
        except sqlite3.IntegrityError:
            # Slot already exists, skip
            pass
    
    conn.commit()
    conn.close()

def create_booking(customer_id: int, service_id: int, slot_id: int, booking_date: date, 
                  start_time: str, end_time: str, address: str, special_instructions: str, 
                  total_price: float) -> bool:
    """Create a new booking"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    try:
        # Insert booking
        conn.execute('''
            INSERT INTO customer_bookings 
            (customer_user_id, service_type_id, slot_id, date, start_time, end_time, 
             address, special_instructions, total_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer_id, service_id, slot_id, booking_date.strftime('%Y-%m-%d'),
              start_time, end_time, address, special_instructions, total_price))
        
        # Update slot booking count
        conn.execute('''
            UPDATE time_slots 
            SET current_bookings = current_bookings + 1
            WHERE id = ?
        ''', (slot_id,))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error creating booking: {e}")
        return False
    finally:
        conn.close()

def get_customer_bookings(customer_id: int) -> List[Dict]:
    """Get all bookings for a customer"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    cursor = conn.execute('''
        SELECT cb.id, st.name, cb.date, cb.start_time, cb.end_time, 
               cb.address, cb.total_price, cb.status, cb.created_at
        FROM customer_bookings cb
        JOIN service_types st ON cb.service_type_id = st.id
        WHERE cb.customer_user_id = ?
        ORDER BY cb.date DESC, cb.start_time DESC
    ''', (customer_id,))
    
    bookings = []
    for row in cursor.fetchall():
        bookings.append({
            'id': row[0],
            'service_name': row[1],
            'date': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'address': row[5],
            'total_price': row[6],
            'status': row[7],
            'created_at': row[8]
        })
    
    conn.close()
    return bookings

def check_email_exists(email: str) -> bool:
    """Check if an email address already exists in the customer database"""
    try:
        conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Check if email already exists in customer_users table
        cursor.execute('SELECT email FROM customer_users WHERE email = ?', (email.strip().lower(),))
        existing_user = cursor.fetchone()
        
        conn.close()
        
        # Return True if email exists, False if available
        return existing_user is not None
        
    except Exception as e:
        # Log the error but don't fail registration
        log_error('customer_portal', e, {
            'email': email,
            'error_type': 'email_check_error',
            'error_message': str(e)
        })
        # If we can't check, assume email doesn't exist (fail-safe)
        return False

# Session state initialization
if 'customer_logged_in' not in st.session_state:
    st.session_state.customer_logged_in = False
if 'customer_user' not in st.session_state:
    st.session_state.customer_user = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'registration_success' not in st.session_state:
    st.session_state.registration_success = False
if 'registration_just_completed' not in st.session_state:
    st.session_state.registration_just_completed = False
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # 0 for login, 1 for register

def show_header():
    """Show website header"""
    st.markdown('<h1 class="main-header">🧹 Aufraumenbee</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Professional Cleaning Services</p>', unsafe_allow_html=True)

def show_registration_form():
    """Show customer registration form"""
    st.subheader("Create Your Account")
    
    # Check if registration was just completed
    if st.session_state.get('registration_success', False):
        # Create a celebration animation with balloons (only show once)
        if st.session_state.get('registration_just_completed', False):
            # Log the celebration display
            log_user_action('customer_portal', 'celebration_displayed', 
                           {'customer_name': st.session_state.get('new_customer_name', 'Unknown')})
            
            # Multiple animation effects for maximum celebration impact
            st.balloons()
            # Show snow effect for extra celebration
            st.snow()
            
            # Mark that celebration was shown
            st.session_state.registration_just_completed = False
        
        # Show multiple success messages for maximum impact
        st.success("🎉 **CONGRATULATIONS! Your Account Has Been Created Successfully!** 🎉")
        st.info("🔥 **You're now part of the Aufraumenbee family!** Welcome aboard! 🔥")
        st.success("🌟 **FANTASTIC NEWS!** Your cleaning journey starts now! 🌟")
        st.info("🎊 **AMAZING!** Get ready for the best cleaning experience ever! 🎊")
        
        # Create an ultra-beautiful styled success container
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            text-align: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            border: 3px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
        ">
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 20px 20px; animation: sparkle 3s linear infinite;"></div>
            <div style="position: relative; z-index: 2;">
                <div style="font-size: 5rem; margin-bottom: 20px; animation: bounce 2s infinite;">🎉</div>
                <h1 style="margin: 0; color: white; font-weight: bold; text-shadow: 3px 3px 6px rgba(0,0,0,0.4); font-size: 2.5rem;">
                    🌟 WELCOME TO AUFRAUMENBEE! 🌟
                </h1>
                <div style="height: 4px; background: linear-gradient(90deg, #FFD700, #FFA500, #FF6B6B, #4ECDC4, #FFD700); margin: 20px auto; border-radius: 2px; width: 80%; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                <p style="margin: 20px 0; font-size: 20px; line-height: 1.8; font-weight: 500;">
                    � <strong>FANTASTIC!</strong> Your account has been successfully created! 🎊<br>
                    <span style="font-size: 18px;">You're now officially part of our amazing community of satisfied customers!</span>
                </p>
                <p style="margin: 15px 0; font-size: 18px; opacity: 0.95; font-weight: 500;">
                    ✨ <strong>Ready to transform your space?</strong> Let's make your home sparkle! ✨
                </p>
                <div style="margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                    <p style="margin: 0; font-size: 16px; font-style: italic;">
                        "Thank you for choosing Aufraumenbee - where cleaning dreams come true!" 💫
                    </p>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        @keyframes sparkle {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Add clear login instructions for the newly registered user
        if 'new_customer_email' in st.session_state:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            ">
                <h4 style="margin: 0 0 10px 0; color: white;">🎯 Next Step: Login with Your New Credentials</h4>
                <p style="margin: 0; font-size: 16px; opacity: 0.95;">
                    Click the "LOGIN TO MY ACCOUNT" button below to login with:<br>
                    📧 <strong>Email:</strong> {st.session_state.new_customer_email}<br>
                    🔒 <strong>Password:</strong> The password you just created during registration
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced action buttons with maximum visual appeal
        st.markdown("""
        <div style="margin: 30px 0; text-align: center;">
            <h4 style="color: #333; margin-bottom: 20px;">🎯 <strong>Ready to Get Started?</strong> 🎯</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        with col1:
            if st.button("🔐 **LOGIN TO MY ACCOUNT** - Let's Go!", use_container_width=True, type="primary"):
                # Clear success state and prepare for login
                st.session_state.registration_success = False
                st.session_state.registration_just_completed = False
                # Pre-populate login email with registered email
                if 'new_customer_email' in st.session_state:
                    st.session_state.login_email = st.session_state.new_customer_email
                st.session_state.active_tab = 0  # Switch to login tab
                st.success("🎯 **Redirecting to login...** Your email has been pre-filled for you!")
                st.rerun()
        with col2:
            if st.button("📧 Get Welcome Email", use_container_width=True):
                st.balloons()
                st.success("📬 **Welcome email sent!** Check your inbox for tips and offers!")
                st.info("💡 **Pro Tip:** Add our email to your contacts so you never miss our updates!")
        
        # Additional engagement buttons
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🎊 Share the Good News!", use_container_width=True):
                st.success("🌟 **Thanks for spreading the word!** Your friends will love Aufraumenbee too!")
                st.info("💝 **Referral Bonus:** Get $20 credit for each friend who books a service!")
        with col4:
            if st.button("📱 Download Our App", use_container_width=True):
                st.info("📲 **Mobile app coming soon!** We'll notify you when it's ready!")
        
        # Add button to dismiss success message and show registration form again
        if st.button("📝 Register Another Account", use_container_width=True):
            st.session_state.registration_success = False
            st.session_state.registration_just_completed = False
            st.rerun()
        
        return
    
    # Show simple registration form
    st.markdown("### 📝 Fill out the form below to create your account:")
    
    # Simple registration form
    with st.form("simple_registration_form", clear_on_submit=True):
        
        # Personal Information Section
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name*", 
                placeholder="Enter your first name"
            )
            email = st.text_input(
                "Email Address*", 
                placeholder="your.email@example.com"
            )
            password = st.text_input(
                "Password*", 
                type="password", 
                placeholder="Minimum 6 characters"
            )
            
        with col2:
            last_name = st.text_input(
                "Last Name*", 
                placeholder="Enter your last name"
            )
            phone = st.text_input(
                "Phone Number*", 
                placeholder="+1 (555) 123-4567"
            )
            confirm_password = st.text_input(
                "Confirm Password*", 
                type="password", 
                placeholder="Re-enter your password"
            )
        
        # Service Address
        address = st.text_area(
            "Service Address*", 
            placeholder="Enter your complete address where you need cleaning services",
            height=80
        )
        
        # Terms checkbox
        terms = st.checkbox("I agree to Terms & Conditions *")
        
        # Submit button - THIS DEFINES THE submitted VARIABLE
        submitted = st.form_submit_button("🚀 **CREATE ACCOUNT**", use_container_width=True, type="primary")
        
        if submitted:
            # Simple validation using list of errors
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
                errors.append("Complete address required (minimum 10 characters)")
            if not terms:
                errors.append("Must accept terms & conditions")
            
            if errors:
                st.error("❌ **Please fix these issues:**")
                for error in errors:
                    st.error(f"• {error}")
                return
            
            # Check if email already exists
            if check_email_exists(email.strip()):
                st.error("❌ **This email is already registered**")
                st.info("💡 **Try logging in instead or use a different email address**")
                return
            
            # All validation passed - create account
            st.success("✅ **Creating your account...**")
            
            with st.spinner("Please wait..."):
                try:
                    # Register the customer
                    registration_result = register_customer(
                        email.strip(), 
                        password, 
                        first_name.strip(), 
                        last_name.strip(), 
                        phone.strip(), 
                        address.strip()
                    )
                    
                    if registration_result:
                        # Success! Store success state
                        st.session_state.registration_success = True
                        st.session_state.registration_just_completed = True
                        st.session_state.new_customer_name = first_name.strip()
                        st.session_state.new_customer_email = email.strip()
                        
                        # Log successful registration
                        log_user_action('customer_portal', 'customer_registration_success', {
                            'email': email.strip(),
                            'first_name': first_name.strip(),
                            'last_name': last_name.strip()
                        })
                        
                        # Show success and trigger page refresh
                        st.success(f"🎉 **Account created successfully!** Welcome, {first_name}!")
                        st.balloons()
                        st.rerun()
                        
                    else:
                        st.error("❌ **Registration failed - Please try again**")
                        
                except Exception as e:
                    st.error("❌ **Something went wrong. Please try again.**")
                    log_error('customer_portal', e, {
                        'email': email.strip(),
                        'error_type': 'registration_error'
                    })

def show_login_form():
    """Show customer login form with enhanced flow for newly registered users"""
    st.subheader("Login to Your Account")
    
    # Check if user just came from registration
    if 'new_customer_email' in st.session_state:
        st.success(f"🎉 **Welcome! Your account has been created successfully!**")
        st.info(f"""
        **✅ Ready to log in:**
        - Your email (**{st.session_state.new_customer_email}**) has been pre-filled below
        - Just enter your password and click Login
        - You're all set to start booking cleaning services!
        """)
        st.markdown("---")
    
    # Add helpful demo credentials info (collapsed by default if coming from registration)
    with st.expander("🧪 Demo Credentials for Testing", expanded=('new_customer_email' not in st.session_state)):
        st.info("""
        **Option 1: Demo Customer**
        - 📧 Email: `demo.login@aufraumenbee.com`
        - 🔒 Password: `demo123`
        
        **Option 2: Integration Test Customer**
        - 📧 Email: `test.integration@example.com`
        - 🔒 Password: `testpass123`
        """)
    
    # Use a static form key to avoid form submission issues
    with st.form("customer_login_form", clear_on_submit=False):
        # Pre-populate email if coming from registration
        default_email = st.session_state.get('new_customer_email', '')
        email = st.text_input(
            "Email Address", 
            placeholder="your.email@example.com", 
            key="login_email",
            value=default_email
        )
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        # Add contextual help message
        if 'new_customer_email' in st.session_state:
            st.caption("💡 **Your email is pre-filled** - just enter the password you created during registration")
        else:
            st.caption("💡 **Tip**: Copy and paste the demo credentials from above to test the login")
        
        submitted = st.form_submit_button("🔓 Login", use_container_width=True)
        
        if submitted:
            # Enhanced validation and debugging
            if not email or not password:
                st.error("❌ Please enter both email and password.")
                return
            
            if not email.strip() or not password.strip():
                st.error("❌ Email and password cannot be empty or just spaces.")
                return
            
            # Show login attempt info for debugging
            st.info(f"🔄 **Attempting login for**: {email}")
            
            try:
                user = authenticate_customer(email.strip(), password)
                
                if user:
                    # Log successful login
                    log_user_action('customer_portal', 'customer_login_success', {
                        'email': email,
                        'user_id': user['id'],
                        'user_name': f"{user['first_name']} {user['last_name']}"
                    })
                    
                    st.session_state.customer_logged_in = True
                    st.session_state.customer_user = user
                    # Clear registration success state on successful login
                    st.session_state.registration_success = False
                    st.session_state.registration_just_completed = False
                    # Clear the stored registration email
                    if 'new_customer_email' in st.session_state:
                        del st.session_state.new_customer_email
                    
                    # Enhanced welcome message
                    # Check if this is a newly registered user's first login
                    is_new_user = 'new_customer_email' in st.session_state and st.session_state.new_customer_email == email
                    
                    if is_new_user:
                        st.success(f"🎉 **FANTASTIC! Welcome to Aufraumenbee, {user['first_name']}!**")
                        st.success("✅ **Your registration and login are both successful!**")
                        st.balloons()  # Add celebration
                        st.snow()     # Extra celebration for new users
                        st.info("🌟 **You're now ready to book your first cleaning service!**")
                    else:
                        st.success(f"🎉 **Welcome back, {user['first_name']}!**")
                        st.balloons()  # Add celebration
                    
                    # Clear form fields on successful login
                    if 'login_email' in st.session_state:
                        del st.session_state.login_email
                    if 'login_password' in st.session_state:
                        del st.session_state.login_password
                
                    # Show welcome container
                    welcome_title = "🎉 Welcome to Aufraumenbee!" if is_new_user else "👋 Welcome Back!"
                    welcome_message = "You've successfully created your account and logged in!" if is_new_user else "You're successfully logged in"
                    action_message = "Ready to book your first cleaning service?" if is_new_user else "Ready to book your next cleaning service?"
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(90deg, #2196F3, #1976D2);
                        color: white;
                        padding: 15px;
                        border-radius: 10px;
                        margin: 15px 0;
                        text-align: center;
                    ">
                        <h4 style="margin: 0; color: white;">{welcome_title}</h4>
                        <p style="margin: 10px 0;">
                            {welcome_message} as <strong>{user['first_name']} {user['last_name']}</strong>
                        </p>
                        <p style="margin: 5px 0; font-size: 14px; opacity: 0.9;">
                            {action_message}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Trigger page refresh to show logged-in interface
                    st.rerun()
                    
                else:
                    # Log failed login attempt
                    log_error('customer_portal', 'Invalid login credentials', {
                        'email': email,
                        'error_type': 'invalid_credentials'
                    })
                    
                    st.error("❌ **Invalid email or password.**")
                    st.warning("""
                    **Login failed. Please check:**
                    - ✉️ Email address is correct
                    - 🔒 Password is correct (case-sensitive)
                    - 📧 You have an account with this email
                    
                    **Need help?**
                    - Try the demo credentials above
                    - Register a new account using the "Register" tab
                    """)
                    
            except Exception as e:
                # Handle unexpected login errors
                log_error('customer_portal', e, {
                    'email': email,
                    'error_type': 'login_exception',
                    'error_message': str(e)
                })
                
                st.error("❌ **Login Error**")
                st.error(f"Sorry, something went wrong during login: {str(e)}")
                st.info("🔄 **Please try again.** If the problem persists, contact support.")
    
    # Note: Removed the buttons that were incorrectly inside the form

def show_services():
    """Show available services"""
    st.subheader("Our Cleaning Services")
    
    services = get_service_types()
    
    # Group services by category
    categories = {}
    for service in services:
        category = service['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(service)
    
    for category, category_services in categories.items():
        st.markdown(f"### {category} Services")
        
        cols = st.columns(2)
        for idx, service in enumerate(category_services):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="service-card">
                        <h4>{service['name']}</h4>
                        <p>{service['description']}</p>
                        <div class="price-tag">${service['base_price']}</div>
                        <p><small>Duration: {service['duration_minutes']} minutes</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Book {service['name']}", key=f"book_{service['id']}", use_container_width=True):
                        st.session_state.selected_service = service
                        st.session_state.booking_step = 'datetime'
                        st.rerun()

def show_booking_form():
    """Show booking form"""
    if 'selected_service' not in st.session_state:
        st.error("Please select a service first.")
        return
    
    service = st.session_state.selected_service
    
    st.subheader(f"Book {service['name']}")
    
    # Step 1: Date and Time Selection
    if st.session_state.get('booking_step', 'datetime') == 'datetime':
        st.markdown("### Select Date and Time")
        
        # Date selection
        min_date = date.today() + timedelta(days=1)  # Tomorrow
        max_date = date.today() + timedelta(days=30)  # 30 days ahead
        
        selected_date = st.date_input(
            "Preferred Date",
            min_value=min_date,
            max_value=max_date,
            value=min_date
        )
        
        if selected_date:
            # Get available slots
            available_slots = get_available_slots(selected_date, service['duration_minutes'])
            
            if available_slots:
                st.markdown("### Available Time Slots")
                
                slot_options = {slot['display_time']: slot for slot in available_slots}
                selected_time = st.selectbox(
                    "Choose a time slot",
                    options=list(slot_options.keys()),
                    index=0
                )
                
                if selected_time:
                    selected_slot = slot_options[selected_time]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Continue to Details", use_container_width=True):
                            st.session_state.selected_slot = selected_slot
                            st.session_state.selected_date = selected_date
                            st.session_state.booking_step = 'details'
                            st.rerun()
                    
                    with col2:
                        if st.button("Back to Services", use_container_width=True):
                            if 'selected_service' in st.session_state:
                                del st.session_state.selected_service
                            if 'booking_step' in st.session_state:
                                del st.session_state.booking_step
                            st.rerun()
            else:
                st.warning("No available slots for this date. Please choose another date.")
    
    # Step 2: Booking Details
    elif st.session_state.get('booking_step') == 'details':
        selected_slot = st.session_state.selected_slot
        selected_date = st.session_state.selected_date
        
        st.markdown("### Booking Details")
        
        # Show booking summary
        st.info(f"""
        **Service:** {service['name']}  
        **Date:** {selected_date.strftime('%B %d, %Y')}  
        **Time:** {selected_slot['display_time']}  
        **Duration:** {service['duration_minutes']} minutes  
        **Base Price:** ${service['base_price']}
        """)
        
        with st.form("booking_details_form"):
            # Address (pre-filled from user profile, but editable)
            address = st.text_area(
                "Service Address*",
                value=st.session_state.customer_user.get('address', ''),
                placeholder="Enter the address where cleaning service is needed"
            )
            
            # Special instructions
            special_instructions = st.text_area(
                "Special Instructions (Optional)",
                placeholder="Any specific requirements, access instructions, or special requests..."
            )
            
            # Price calculation (you can add modifiers here)
            total_price = service['base_price']
            
            st.markdown(f"### Total Price: ${total_price}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("Confirm Booking", use_container_width=True):
                    if not address:
                        st.error("Please provide a service address.")
                    else:
                        # Create booking
                        if create_booking(
                            st.session_state.customer_user['id'],
                            service['id'],
                            selected_slot['id'],
                            selected_date,
                            selected_slot['start_time'],
                            selected_slot['end_time'],
                            address,
                            special_instructions,
                            total_price
                        ):
                            st.success("🎉 Booking confirmed successfully!")
                            st.markdown("""
                            <div class="booking-success">
                                <h4>Booking Confirmed!</h4>
                                <p>Your cleaning service has been booked. You will receive a confirmation email shortly.</p>
                                <p>Our team will contact you 24 hours before the scheduled service.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Clear booking session data
                            for key in ['selected_service', 'selected_slot', 'selected_date', 'booking_step']:
                                if key in st.session_state:
                                    del st.session_state[key]
                            
                            st.balloons()
                        else:
                            st.error("Failed to create booking. Please try again.")
            
            with col2:
                if st.form_submit_button("Back to Time Selection", use_container_width=True):
                    st.session_state.booking_step = 'datetime'
                    st.rerun()

def show_my_bookings():
    """Show customer's bookings"""
    st.subheader("My Bookings")
    
    bookings = get_customer_bookings(st.session_state.customer_user['id'])
    
    if not bookings:
        st.info("You don't have any bookings yet. Book your first cleaning service!")
        return
    
    for booking in bookings:
        status_color = {
            'pending': '🟡',
            'confirmed': '🟢', 
            'completed': '✅',
            'cancelled': '❌'
        }.get(booking['status'], '🔵')
        
        with st.expander(f"{status_color} {booking['service_name']} - {booking['date']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Date:** {booking['date']}")
                st.write(f"**Time:** {booking['start_time']} - {booking['end_time']}")
                st.write(f"**Service:** {booking['service_name']}")
                st.write(f"**Status:** {booking['status'].title()}")
            
            with col2:
                st.write(f"**Price:** ${booking['total_price']}")
                st.write(f"**Address:** {booking['address']}")
                st.write(f"**Booked:** {booking['created_at']}")
            
            if booking['status'] == 'pending':
                if st.button(f"Cancel Booking", key=f"cancel_{booking['id']}"):
                    # Add cancellation logic here
                    st.warning("Cancellation feature coming soon!")

def main():
    """Main application function"""
    # Initialize database tables on first run
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return
    
    # Navigation
    if not st.session_state.customer_logged_in:
        # If registration was successful, show special welcome header and success message
        if st.session_state.get('registration_success', False):
            # Special celebratory header for successful registration
            st.markdown("""
            <div style="text-align: center; margin: 20px 0;">
                <h1 style="
                    color: #FF6B6B; 
                    font-size: 3.5rem; 
                    font-weight: bold; 
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                    animation: pulse 2s infinite;
                ">🎉 AUFRAUMENBEE 🎉</h1>
                <p style="
                    font-size: 1.5rem; 
                    color: #28a745; 
                    font-weight: bold; 
                    margin: 10px 0;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                ">🌟 CONGRATULATIONS ON JOINING US! 🌟</p>
                <p style="font-size: 1.1rem; color: #666; font-style: italic;">
                    Your journey to a sparkling clean home starts now!
                </p>
            </div>
            
            <style>
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            </style>
            """, unsafe_allow_html=True)
            
            show_registration_form()  # This will show only the success message
        else:
            # Normal header for first-time visitors
            show_header()
            
            # Welcome message and tabs
            st.markdown("Book your next cleaning service with just a few clicks.")
            
            tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with tab1:
                show_login_form()
            
            with tab2:
                show_registration_form()
        
        st.markdown("---")
        st.markdown("### Why Choose Aufraumenbee?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🏆 **Professional Service**\nTrained and background-checked cleaners")
        with col2:
            st.markdown("💰 **Fair Pricing**\nTransparent pricing with no hidden fees")
        with col3:
            st.markdown("📅 **Flexible Scheduling**\nBook at your convenience")
        
        # Show services preview (without booking buttons)
        st.markdown("---")
        show_services()
        
    else:
        # Logged in customer interface - show header
        show_header()
        
        st.sidebar.markdown(f"### Welcome, {st.session_state.customer_user['first_name']}!")
        
        menu_options = ["Book Service", "My Bookings", "Account", "Logout"]
        selected_menu = st.sidebar.selectbox("Menu", menu_options)
        
        if selected_menu == "Book Service":
            if 'selected_service' in st.session_state and 'booking_step' in st.session_state:
                show_booking_form()
            else:
                show_services()
        
        elif selected_menu == "My Bookings":
            show_my_bookings()
        
        elif selected_menu == "Account":
            st.subheader("Account Information")
            user = st.session_state.customer_user
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {user['first_name']} {user['last_name']}")
                st.write(f"**Email:** {user['email']}")
            with col2:
                st.write(f"**Phone:** {user['phone']}")
                st.write(f"**Address:** {user['address']}")
        
        elif selected_menu == "Logout":
            st.session_state.customer_logged_in = False
            st.session_state.customer_user = None
            # Clear any booking session data
            for key in ['selected_service', 'selected_slot', 'selected_date', 'booking_step']:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("Logged out successfully!")
            st.rerun()

if __name__ == "__main__":
    main()
