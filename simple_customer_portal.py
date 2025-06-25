"""
Simple Customer Registration Form - Clean Version
"""

import streamlit as st
import sqlite3
import bcrypt
import re
from datetime import datetime
from typing import Optional

# Initialize session state
if 'customer_logged_in' not in st.session_state:
    st.session_state.customer_logged_in = False
if 'registration_success' not in st.session_state:
    st.session_state.registration_success = False
if 'registration_just_completed' not in st.session_state:
    st.session_state.registration_just_completed = False

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_email_exists(email: str) -> bool:
    """Check if email already exists in database"""
    try:
        conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM customer_users WHERE email = ?', (email.lower(),))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking email: {e}")
        return False

def register_customer(email: str, password: str, first_name: str, last_name: str, phone: str, address: str) -> bool:
    """Register new customer - only stores data if successful"""
    try:
        conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Double-check email doesn't exist
        cursor.execute('SELECT email FROM customer_users WHERE email = ?', (email.lower(),))
        if cursor.fetchone():
            conn.close()
            return False
        
        # Hash password and insert user
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO customer_users (email, password_hash, first_name, last_name, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email.lower(), password_hash, first_name, last_name, phone, address))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Registration error: {e}")
        return False

def authenticate_customer(email: str, password: str) -> Optional[dict]:
    """Authenticate customer login"""
    try:
        conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, password_hash, first_name, last_name, phone, address
            FROM customer_users 
            WHERE email = ?
        ''', (email.lower(),))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return {
                'id': user[0],
                'email': user[1],
                'first_name': user[3],
                'last_name': user[4],
                'phone': user[5],
                'address': user[6]
            }
        return None
        
    except Exception as e:
        return None

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
    
    # Simple login form
    with st.form("simple_login", clear_on_submit=False):
        email = st.text_input(
            "Email Address", 
            placeholder="your.email@example.com",
            value=default_email
        )
        password = st.text_input(
            "Password", 
            type="password", 
            placeholder="Enter your password"
        )
        
        submitted = st.form_submit_button("🔓 **LOGIN**", use_container_width=True, type="primary")
        
        if submitted:
            if not email or not password:
                st.error("❌ Please enter both email and password")
                return
            
            # Attempt login
            user = authenticate_customer(email.strip(), password)
            
            if user:
                st.session_state.customer_logged_in = True
                st.session_state.customer_user = user
                
                # Clear any registration state
                for key in ['registration_success', 'login_email', 'new_customer_name', 'new_customer_email']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.success(f"🎉 **Welcome back, {user['first_name']}!**")
                st.rerun()
            else:
                st.error("❌ **Invalid email or password**")
                st.info("💡 **Check your credentials and try again**")

def main():
    """Main app"""
    st.set_page_config(
        page_title="Aufraumenbee - Customer Portal",
        page_icon="🧹",
        layout="wide"
    )
    
    st.title("🧹 Aufraumenbee")
    st.markdown("Professional Cleaning Services")
    
    if not st.session_state.customer_logged_in:
        if st.session_state.get('registration_success', False):
            show_registration_form()
        else:
            tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with tab1:
                show_login_form()
            
            with tab2:
                show_registration_form()
    else:
        # Customer dashboard
        user = st.session_state.customer_user
        st.success(f"🎉 **Welcome, {user['first_name']} {user['last_name']}!**")
        
        # Simple customer menu
        st.markdown("### Your Account")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"📧 **Email:** {user['email']}")
        with col2:
            st.info(f"📞 **Phone:** {user['phone']}")
        with col3:
            if st.button("🚪 **LOGOUT**", type="secondary"):
                st.session_state.customer_logged_in = False
                st.session_state.customer_user = None
                st.success("✅ **Logged out successfully**")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Available Services")
        st.info("🧹 **Book cleaning services** - Feature coming soon!")

if __name__ == "__main__":
    main()
