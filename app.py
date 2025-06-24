import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import bcrypt

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
    page_title="Aufraumenbee - Cleaning Service Management",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logging
if LOGGING_ENABLED:
    logger = get_realtime_logger()
    log_user_action('app', 'app_start', {'timestamp': datetime.now().isoformat()})

# Database setup
@st.cache_resource
def init_database():
    """Initialize SQLite database with all required tables"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            preferences TEXT,
            rating REAL DEFAULT 0,
            total_jobs INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            skills TEXT,
            hourly_rate REAL,
            employment_type TEXT, -- 'permanent' or 'contract'
            availability TEXT,
            background_check BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            scheduled_date DATE,
            scheduled_time TEXT,
            duration INTEGER, -- in minutes
            status TEXT DEFAULT 'pending', -- pending, approved, assigned, in_progress, completed, cancelled
            service_type TEXT,
            location TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            customer_id INTEGER,
            amount REAL,
            tax_amount REAL,
            discount REAL DEFAULT 0,
            status TEXT DEFAULT 'pending', -- pending, paid, overdue
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER,
            unit_price REAL,
            minimum_stock INTEGER DEFAULT 10,
            supplier TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Customer portal tables
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
    
    # Create default admin user if not exists
    admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
    conn.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role, full_name, email)
        VALUES (?, ?, ?, ?, ?)
    ''', ("admin", admin_password.decode('utf-8'), "admin", "System Administrator", "admin@aufraumenbee.com"))
    
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

# Authentication functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def authenticate_user(username, password):
    conn = init_database()
    cursor = conn.execute("SELECT password_hash, role, full_name FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user and verify_password(password, user[0]):
        user_info = {"username": username, "role": user[1], "full_name": user[2]}
        log_user_action('auth', 'login_success', {'username': username, 'role': user[1]})
        log_database_operation('SELECT', 'users', {'action': 'authenticate', 'username': username})
        return user_info
    else:
        log_user_action('auth', 'login_failed', {'username': username})
    return None

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

def login_page():
    """Login page"""
    st.title("🧹 Aufraumenbee")
    st.subheader("Cleaning Service Management System")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Please Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with st.expander("Default Credentials"):
            st.info("Username: admin | Password: admin123")

def logout():
    """Logout function"""
    if st.session_state.user:
        log_user_action('auth', 'logout', {'username': st.session_state.user['username']})
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

def main_app():
    """Main application after authentication"""
    
    # Sidebar
    with st.sidebar:
        st.title("🧹 Aufraumenbee")
        st.write(f"Welcome, {st.session_state.user['full_name']}")
        st.write(f"Role: {st.session_state.user['role'].title()}")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=[
                "Dashboard", 
                "Customer Management", 
                "Employee Management", 
                "Job Management", 
                "Booking Requests",
                "Scheduling",
                "Invoicing", 
                "Inventory",
                "Analytics",
                "Portal Management",
                "Settings"
            ],
            icons=[
                "house", 
                "people", 
                "person-badge", 
                "briefcase", 
                "calendar-check",
                "calendar3",
                "receipt", 
                "box",
                "graph-up",
                "globe",
                "gear"
            ],
            menu_icon="app-indicator",
            default_index=0,
        )
        
        if st.button("Logout", use_container_width=True):
            logout()
    
    # Main content area
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Customer Management":
        show_customer_management()
    elif selected == "Employee Management":
        show_employee_management()
    elif selected == "Job Management":
        show_job_management()
    elif selected == "Booking Requests":
        show_booking_requests()
    elif selected == "Scheduling":
        show_scheduling()
    elif selected == "Invoicing":
        show_invoicing()
    elif selected == "Inventory":
        show_inventory()
    elif selected == "Analytics":
        show_analytics()
    elif selected == "Portal Management":
        show_portal_management()
    elif selected == "Settings":
        show_settings()

def show_dashboard():
    """Dashboard with key metrics and overview"""
    st.title("📊 Dashboard")
    
    conn = init_database()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        st.metric("Total Customers", total_customers)
    
    with col2:
        total_employees = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        st.metric("Total Employees", total_employees)
    
    with col3:
        pending_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE status = 'pending'").fetchone()[0]
        st.metric("Pending Bookings", pending_jobs)
    
    with col4:
        today_jobs = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE scheduled_date = date('now') AND status IN ('approved', 'assigned', 'in_progress')"
        ).fetchone()[0]
        st.metric("Today's Jobs", today_jobs)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    # Get recent jobs
    recent_jobs = pd.read_sql_query('''
        SELECT j.title, c.name as customer, j.status, j.scheduled_date, j.created_at
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        ORDER BY j.created_at DESC
        LIMIT 10
    ''', conn)
    
    if not recent_jobs.empty:
        st.dataframe(recent_jobs, use_container_width=True)
    else:
        st.info("No recent activity")

def show_customer_management():
    """Customer management interface"""
    st.title("👥 Customer Management")
    
    tab1, tab2 = st.tabs(["Customer List", "Add New Customer"])
    
    conn = init_database()
    
    with tab1:
        customers = pd.read_sql_query("SELECT * FROM customers ORDER BY created_at DESC", conn)
        
        if not customers.empty:
            # Search functionality
            search_term = st.text_input("Search customers...")
            if search_term:
                customers = customers[customers['name'].str.contains(search_term, case=False, na=False)]
            
            # Display customers
            for _, customer in customers.iterrows():
                with st.expander(f"{customer['name']} - {customer['email']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Phone:** {customer['phone']}")
                        st.write(f"**Address:** {customer['address']}")
                        st.write(f"**Total Jobs:** {customer['total_jobs']}")
                    with col2:
                        st.write(f"**Rating:** ⭐ {customer['rating']:.1f}")
                        st.write(f"**Joined:** {customer['created_at']}")
                        
                        if st.button(f"View Details", key=f"customer_{customer['id']}"):
                            st.session_state.selected_customer = customer['id']
        else:
            st.info("No customers found")
    
    with tab2:
        st.subheader("Add New Customer")
        
        with st.form("add_customer"):
            name = st.text_input("Customer Name*")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            preferences = st.text_area("Service Preferences")
            
            if st.form_submit_button("Add Customer"):
                if name:
                    conn.execute('''
                        INSERT INTO customers (name, email, phone, address, preferences)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, email, phone, address, preferences))
                    conn.commit()
                    st.success("Customer added successfully!")
                    st.rerun()
                else:
                    st.error("Customer name is required")

def show_employee_management():
    """Employee management interface"""
    st.title("👤 Employee Management")
    
    tab1, tab2 = st.tabs(["Employee List", "Add New Employee"])
    
    conn = init_database()
    
    with tab1:
        employees = pd.read_sql_query("SELECT * FROM employees ORDER BY created_at DESC", conn)
        
        if not employees.empty:
            for _, employee in employees.iterrows():
                with st.expander(f"{employee['name']} - {employee['employment_type'].title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {employee['email']}")
                        st.write(f"**Phone:** {employee['phone']}")
                        st.write(f"**Skills:** {employee['skills']}")
                        st.write(f"**Employment Type:** {employee['employment_type'].title()}")
                    with col2:
                        st.write(f"**Hourly Rate:** ${employee['hourly_rate']:.2f}")
                        st.write(f"**Background Check:** {'✅' if employee['background_check'] else '❌'}")
                        st.write(f"**Availability:** {employee['availability']}")
        else:
            st.info("No employees found")
    
    with tab2:
        st.subheader("Add New Employee")
        
        with st.form("add_employee"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Employee Name*")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                employment_type = st.selectbox("Employment Type", ["permanent", "contract"])
            
            with col2:
                hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=0.50)
                skills = st.text_input("Skills (comma-separated)")
                availability = st.text_input("Availability")
                background_check = st.checkbox("Background Check Completed")
            
            if st.form_submit_button("Add Employee"):
                if name:
                    conn.execute('''
                        INSERT INTO employees (name, email, phone, skills, hourly_rate, employment_type, availability, background_check)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, email, phone, skills, hourly_rate, employment_type, availability, background_check))
                    conn.commit()
                    st.success("Employee added successfully!")
                    st.rerun()
                else:
                    st.error("Employee name is required")

def show_booking_requests():
    """Booking requests from customers"""
    st.title("📅 Booking Requests")
    
    tab1, tab2 = st.tabs(["Pending Requests", "Customer Booking Form"])
    
    conn = init_database()
    
    with tab1:
        # Show pending booking requests
        pending_jobs = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name, c.phone as customer_phone
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            WHERE j.status = 'pending'
            ORDER BY j.created_at DESC
        ''', conn)
        
        if not pending_jobs.empty:
            st.subheader("Pending Approval")
            
            for _, job in pending_jobs.iterrows():
                with st.expander(f"Request from {job['customer_name']} - {job['title']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Service:** {job['title']}")
                        st.write(f"**Customer:** {job['customer_name']}")
                        st.write(f"**Phone:** {job['customer_phone']}")
                        st.write(f"**Requested Date:** {job['scheduled_date']}")
                        st.write(f"**Time:** {job['scheduled_time']}")
                    
                    with col2:
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Duration:** {job['duration']} minutes")
                        st.write(f"**Service Type:** {job['service_type']}")
                        st.write(f"**Estimated Price:** ${job['price']:.2f}")
                        st.write(f"**Description:** {job['description']}")
                    
                    with col3:
                        if st.button("✅ Approve", key=f"approve_{job['id']}"):
                            conn.execute("UPDATE jobs SET status = 'approved' WHERE id = ?", (job['id'],))
                            conn.commit()
                            st.success("Request approved!")
                            st.rerun()
                        
                        if st.button("❌ Reject", key=f"reject_{job['id']}"):
                            conn.execute("UPDATE jobs SET status = 'cancelled' WHERE id = ?", (job['id'],))
                            conn.commit()
                            st.success("Request rejected!")
                            st.rerun()
        else:
            st.info("No pending requests")
    
    with tab2:
        st.subheader("Customer Booking Form")
        st.info("This form simulates a customer booking request")
        
        # Get customers for dropdown
        customers = pd.read_sql_query("SELECT id, name FROM customers", conn)
        
        if not customers.empty:
            with st.form("booking_request"):
                col1, col2 = st.columns(2)
                
                with col1:
                    customer_id = st.selectbox(
                        "Select Customer", 
                        customers['id'].tolist(), 
                        format_func=lambda x: customers[customers['id'] == x]['name'].iloc[0]
                    )
                    service_type = st.selectbox(
                        "Service Type", 
                        ["Regular Cleaning", "Deep Cleaning", "Move-in/Move-out", "Post-Construction", "Office Cleaning"]
                    )
                    title = st.text_input("Service Title*")
                    location = st.text_input("Service Location*")
                
                with col2:
                    scheduled_date = st.date_input("Preferred Date")
                    scheduled_time = st.time_input("Preferred Time")
                    duration = st.number_input("Estimated Duration (minutes)", min_value=30, max_value=480, value=120)
                    price = st.number_input("Estimated Price ($)", min_value=0.0, step=10.0)
                
                description = st.text_area("Special Instructions")
                
                if st.form_submit_button("Submit Booking Request"):
                    if title and location:
                        conn.execute('''
                            INSERT INTO jobs (customer_id, title, description, scheduled_date, scheduled_time, 
                                            duration, service_type, location, price, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                        ''', (customer_id, title, description, scheduled_date.strftime('%Y-%m-%d'), 
                             scheduled_time.strftime('%H:%M'), duration, service_type, location, price))
                        conn.commit()
                        st.success("Booking request submitted successfully!")
                        st.rerun()
                    else:
                        st.error("Title and location are required")
        else:
            st.warning("Please add customers first before creating booking requests")

def show_job_management():
    """Job management and assignment"""
    st.title("💼 Job Management")
    
    tab1, tab2 = st.tabs(["Approved Jobs", "Assign Employees"])
    
    conn = init_database()
    
    with tab1:
        # Show approved jobs that need assignment
        approved_jobs = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name, c.phone as customer_phone,
                   e.name as employee_name
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            LEFT JOIN employees e ON j.employee_id = e.id
            WHERE j.status IN ('approved', 'assigned', 'in_progress')
            ORDER BY j.scheduled_date, j.scheduled_time
        ''', conn)
        
        if not approved_jobs.empty:
            for _, job in approved_jobs.iterrows():
                status_color = {
                    'approved': '🟡',
                    'assigned': '🟠', 
                    'in_progress': '🔵',
                    'completed': '🟢'
                }.get(job['status'], '⚪')
                
                with st.expander(f"{status_color} {job['title']} - {job['customer_name']} ({job['status'].title()})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Customer:** {job['customer_name']}")
                        st.write(f"**Date:** {job['scheduled_date']}")
                        st.write(f"**Time:** {job['scheduled_time']}")
                        st.write(f"**Duration:** {job['duration']} min")
                    
                    with col2:
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Service:** {job['service_type']}")
                        st.write(f"**Price:** ${job['price']:.2f}")
                        st.write(f"**Status:** {job['status'].title()}")
                    
                    with col3:
                        current_employee = job['employee_name'] if job['employee_name'] else "Not assigned"
                        st.write(f"**Assigned to:** {current_employee}")
                        
                        if job['status'] == 'assigned':
                            if st.button("Start Job", key=f"start_{job['id']}"):
                                conn.execute("UPDATE jobs SET status = 'in_progress' WHERE id = ?", (job['id'],))
                                conn.commit()
                                st.rerun()
                        
                        if job['status'] == 'in_progress':
                            if st.button("Complete Job", key=f"complete_{job['id']}"):
                                conn.execute("UPDATE jobs SET status = 'completed' WHERE id = ?", (job['id'],))
                                conn.commit()
                                st.rerun()
        else:
            st.info("No approved jobs found")
    
    with tab2:
        st.subheader("Assign Employees to Jobs")
        
        # Get unassigned approved jobs
        unassigned_jobs = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            WHERE j.status = 'approved' AND j.employee_id IS NULL
        ''', conn)
        
        if not unassigned_jobs.empty:
            for _, job in unassigned_jobs.iterrows():
                with st.expander(f"Assign: {job['title']} - {job['customer_name']}"):
                    # Get available employees
                    employees = pd.read_sql_query("SELECT id, name, employment_type, hourly_rate FROM employees", conn)
                    
                    if not employees.empty:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Job:** {job['title']}")
                            st.write(f"**Date:** {job['scheduled_date']}")
                            st.write(f"**Duration:** {job['duration']} minutes")
                            st.write(f"**Location:** {job['location']}")
                        
                        with col2:
                            employee_id = st.selectbox(
                                "Select Employee",
                                employees['id'].tolist(),
                                format_func=lambda x: f"{employees[employees['id'] == x]['name'].iloc[0]} ({employees[employees['id'] == x]['employment_type'].iloc[0]})",
                                key=f"emp_select_{job['id']}"
                            )
                            
                            if st.button("Assign Employee", key=f"assign_{job['id']}"):
                                conn.execute("UPDATE jobs SET employee_id = ?, status = 'assigned' WHERE id = ?", 
                                           (employee_id, job['id']))
                                conn.commit()
                                st.success("Employee assigned successfully!")
                                st.rerun()
                    else:
                        st.warning("No employees available. Please add employees first.")
        else:
            st.info("No unassigned jobs found")

def show_scheduling():
    """Scheduling and calendar view"""
    st.title("📅 Scheduling")
    
    conn = init_database()
    
    # Calendar view would go here - for now showing a simple schedule
    st.subheader("Today's Schedule")
    
    today = datetime.now().strftime('%Y-%m-%d')
    today_jobs = pd.read_sql_query('''
        SELECT j.*, c.name as customer_name, e.name as employee_name
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        LEFT JOIN employees e ON j.employee_id = e.id
        WHERE j.scheduled_date = ? AND j.status IN ('assigned', 'in_progress')
        ORDER BY j.scheduled_time
    ''', conn, params=[today])
    
    if not today_jobs.empty:
        for _, job in today_jobs.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{job['scheduled_time']}**")
                with col2:
                    st.write(f"{job['title']}")
                with col3:
                    st.write(f"Customer: {job['customer_name']}")
                with col4:
                    employee = job['employee_name'] if job['employee_name'] else "Unassigned"
                    st.write(f"Employee: {employee}")
                st.divider()
    else:
        st.info("No jobs scheduled for today")

def show_invoicing():
    """Invoicing and billing"""
    st.title("🧾 Invoicing & Billing")
    
    tab1, tab2 = st.tabs(["Invoice List", "Create Invoice"])
    
    conn = init_database()
    
    with tab1:
        invoices = pd.read_sql_query('''
            SELECT i.*, c.name as customer_name, j.title as job_title
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
            LEFT JOIN jobs j ON i.job_id = j.id
            ORDER BY i.created_at DESC
        ''', conn)
        
        if not invoices.empty:
            st.dataframe(invoices, use_container_width=True)
        else:
            st.info("No invoices found")
    
    with tab2:
        st.subheader("Create New Invoice")
        
        # Get completed jobs without invoices
        completed_jobs = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            WHERE j.status = 'completed' AND j.id NOT IN (SELECT job_id FROM invoices WHERE job_id IS NOT NULL)
        ''', conn)
        
        if not completed_jobs.empty:
            with st.form("create_invoice"):
                job_id = st.selectbox(
                    "Select Completed Job",
                    completed_jobs['id'].tolist(),
                    format_func=lambda x: f"{completed_jobs[completed_jobs['id'] == x]['title'].iloc[0]} - {completed_jobs[completed_jobs['id'] == x]['customer_name'].iloc[0]}"
                )
                
                selected_job = completed_jobs[completed_jobs['id'] == job_id].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    amount = st.number_input("Amount ($)", value=float(selected_job['price']))
                    tax_rate = st.number_input("Tax Rate (%)", value=10.0)
                    discount = st.number_input("Discount ($)", value=0.0)
                
                with col2:
                    tax_amount = amount * (tax_rate / 100)
                    total_amount = amount + tax_amount - discount
                    st.write(f"**Tax Amount:** ${tax_amount:.2f}")
                    st.write(f"**Total Amount:** ${total_amount:.2f}")
                    
                    due_date = st.date_input("Due Date", value=datetime.now() + timedelta(days=30))
                
                if st.form_submit_button("Create Invoice"):
                    conn.execute('''
                        INSERT INTO invoices (job_id, customer_id, amount, tax_amount, discount, due_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (job_id, selected_job['customer_id'], amount, tax_amount, discount, due_date.strftime('%Y-%m-%d')))
                    conn.commit()
                    st.success("Invoice created successfully!")
                    st.rerun()
        else:
            st.info("No completed jobs available for invoicing")

def show_inventory():
    """Inventory management"""
    st.title("📦 Inventory Management")
    
    tab1, tab2 = st.tabs(["Inventory List", "Add Item"])
    
    conn = init_database()
    
    with tab1:
        inventory = pd.read_sql_query("SELECT * FROM inventory ORDER BY item_name", conn)
        
        if not inventory.empty:
            for _, item in inventory.iterrows():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**{item['item_name']}**")
                    st.write(f"Supplier: {item['supplier']}")
                
                with col2:
                    st.write(f"Quantity: {item['quantity']}")
                    if item['quantity'] <= item['minimum_stock']:
                        st.error("⚠️ Low Stock!")
                
                with col3:
                    st.write(f"Unit Price: ${item['unit_price']:.2f}")
                    st.write(f"Total Value: ${item['quantity'] * item['unit_price']:.2f}")
                
                with col4:
                    st.write(f"Min Stock: {item['minimum_stock']}")
                
                st.divider()
        else:
            st.info("No inventory items found")
    
    with tab2:
        st.subheader("Add Inventory Item")
        
        with st.form("add_inventory"):
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("Item Name*")
                quantity = st.number_input("Quantity", min_value=0)
                unit_price = st.number_input("Unit Price ($)", min_value=0.0, step=0.01)
            
            with col2:
                minimum_stock = st.number_input("Minimum Stock Level", min_value=0, value=10)
                supplier = st.text_input("Supplier")
            
            if st.form_submit_button("Add Item"):
                if item_name:
                    conn.execute('''
                        INSERT INTO inventory (item_name, quantity, unit_price, minimum_stock, supplier)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (item_name, quantity, unit_price, minimum_stock, supplier))
                    conn.commit()
                    st.success("Inventory item added successfully!")
                    st.rerun()
                else:
                    st.error("Item name is required")

def show_analytics():
    """Analytics and reporting"""
    st.title("📈 Analytics & Reporting")
    
    conn = init_database()
    
    # Revenue analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Overview")
        
        # Monthly revenue
        monthly_revenue = pd.read_sql_query('''
            SELECT strftime('%Y-%m', j.created_at) as month, SUM(j.price) as revenue
            FROM jobs j
            WHERE j.status = 'completed'
            GROUP BY strftime('%Y-%m', j.created_at)
            ORDER BY month
        ''', conn)
        
        if not monthly_revenue.empty:
            fig = px.line(monthly_revenue, x='month', y='revenue', title='Monthly Revenue')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available")
    
    with col2:
        st.subheader("Job Status Distribution")
        
        job_status = pd.read_sql_query('''
            SELECT status, COUNT(*) as count
            FROM jobs
            GROUP BY status
        ''', conn)
        
        if not job_status.empty:
            fig = px.pie(job_status, values='count', names='status', title='Job Status Distribution')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No job data available")

def show_settings():
    """Settings and configuration"""
    st.title("⚙️ Settings")
    
    tab1, tab2 = st.tabs(["User Management", "System Settings"])
    
    conn = init_database()
    
    with tab1:
        st.subheader("User Management")
        
        # Add new user
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                role = st.selectbox("Role", ["admin", "manager", "employee", "customer"])
            
            with col2:
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
            
            if st.form_submit_button("Add User"):
                if username and password:
                    password_hash = hash_password(password)
                    try:
                        conn.execute('''
                            INSERT INTO users (username, password_hash, role, full_name, email, phone)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (username, password_hash, role, full_name, email, phone))
                        conn.commit()
                        st.success("User added successfully!")
                    except sqlite3.IntegrityError:
                        st.error("Username already exists!")
                else:
                    st.error("Username and password are required")
        
        # List existing users
        st.subheader("Existing Users")
        users = pd.read_sql_query("SELECT username, role, full_name, email FROM users", conn)
        if not users.empty:
            st.dataframe(users, use_container_width=True)
    
    with tab2:
        st.subheader("System Settings")
        st.info("System settings configuration would go here")

def show_portal_management():
    """Customer portal management interface"""
    st.title("🌐 Customer Portal Management")
    
    tab1, tab2, tab3 = st.tabs(["Time Slots", "Services", "Customer Bookings"])
    
    conn = init_database()
    
    with tab1:
        show_slot_management_tab(conn)
    
    with tab2:
        show_service_management_tab(conn)
    
    with tab3:
        show_customer_bookings_tab(conn)

def show_slot_management_tab(conn):
    """Time slot management tab"""
    st.subheader("📅 Time Slot Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Add Time Slots")
        
        with st.form("add_slots"):
            slot_date = st.date_input("Date", value=date.today() + timedelta(days=1))
            start_time = st.time_input("Start Time", value=datetime.strptime("09:00", "%H:%M").time())
            end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
            max_bookings = st.number_input("Max Bookings", min_value=1, max_value=5, value=1)
            
            # Bulk options
            create_multiple = st.checkbox("Create for multiple days")
            if create_multiple:
                num_days = st.number_input("Number of days", min_value=1, max_value=30, value=7)
            
            if st.form_submit_button("Create Slots"):
                if start_time >= end_time:
                    st.error("End time must be after start time")
                else:
                    dates_to_create = [slot_date]
                    if create_multiple:
                        dates_to_create = [slot_date + timedelta(days=i) for i in range(num_days)]
                    
                    success_count = 0
                    for create_date in dates_to_create:
                        try:
                            conn.execute('''
                                INSERT INTO time_slots (date, start_time, end_time, max_bookings, available)
                                VALUES (?, ?, ?, ?, TRUE)
                            ''', (create_date.strftime('%Y-%m-%d'), start_time.strftime('%H:%M'), 
                                 end_time.strftime('%H:%M'), max_bookings))
                            success_count += 1
                        except sqlite3.IntegrityError:
                            pass  # Slot already exists
                    
                    conn.commit()
                    st.success(f"Created {success_count} time slots!")
                    st.rerun()
    
    with col2:
        st.markdown("### Current Slots")
        
        # Date range filter
        start_date = st.date_input("From", value=date.today())
        end_date = st.date_input("To", value=date.today() + timedelta(days=7))
        
        if start_date <= end_date:
            slots_df = pd.read_sql_query('''
                SELECT id, date, start_time, end_time, current_bookings, max_bookings, available
                FROM time_slots
                WHERE date BETWEEN ? AND ?
                ORDER BY date, start_time
            ''', conn, params=(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
            
            if not slots_df.empty:
                for idx, (_, slot) in enumerate(slots_df.iterrows()):
                    status = "🟢 Available" if slot['available'] else "🔴 Disabled"
                    bookings = f"{slot['current_bookings']}/{slot['max_bookings']}"
                    
                    # Create unique identifier for this slot row
                    slot_unique_id = f"{slot['id']}_{idx}_slot"
                    
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.write(f"**{slot['date']} {slot['start_time']}-{slot['end_time']}**")
                        st.write(f"{status} | Bookings: {bookings}")
                    
                    with col_b:
                        if slot['available']:
                            if st.button("Disable", key=f"disable_{slot_unique_id}"):
                                conn.execute("UPDATE time_slots SET available = FALSE WHERE id = ?", (slot['id'],))
                                conn.commit()
                                st.rerun()
                        else:
                            if st.button("Enable", key=f"enable_{slot_unique_id}"):
                                conn.execute("UPDATE time_slots SET available = TRUE WHERE id = ?", (slot['id'],))
                                conn.commit()
                                st.rerun()
                    
                    with col_c:
                        if slot['current_bookings'] == 0:
                            if st.button("Delete", key=f"delete_{slot_unique_id}"):
                                conn.execute("DELETE FROM time_slots WHERE id = ?", (slot['id'],))
                                conn.commit()
                                st.rerun()
                    
                    st.divider()
            else:
                st.info("No slots found for selected date range")

def show_service_management_tab(conn):
    """Service management tab"""
    st.subheader("🧹 Service Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Add/Edit Service")
        
        # Get existing services for editing
        services_df = pd.read_sql_query("SELECT id, name FROM service_types ORDER BY name", conn)
        
        edit_service = st.selectbox("Edit existing service (optional)", 
                                  ["Create New"] + services_df['name'].tolist() if not services_df.empty else ["Create New"])
        
        if edit_service != "Create New" and not services_df.empty:
            service_id = services_df[services_df['name'] == edit_service]['id'].iloc[0]
            service_data = conn.execute('''
                SELECT name, description, base_price, duration_minutes, category
                FROM service_types WHERE id = ?
            ''', (service_id,)).fetchone()
        else:
            service_id = None
            service_data = None
        
        with st.form("service_form"):
            name = st.text_input("Service Name", value=service_data[0] if service_data else "")
            description = st.text_area("Description", value=service_data[1] if service_data else "")
            base_price = st.number_input("Base Price ($)", min_value=0.0, step=5.0,
                                       value=float(service_data[2]) if service_data else 50.0)
            duration = st.number_input("Duration (minutes)", min_value=30, step=30,
                                     value=service_data[3] if service_data else 120)
            category = st.selectbox("Category", ["Residential", "Commercial", "Specialty"],
                                  index=["Residential", "Commercial", "Specialty"].index(service_data[4]) if service_data else 0)
            
            if st.form_submit_button("Save Service"):
                if name and description:
                    if service_id:
                        # Update existing
                        conn.execute('''
                            UPDATE service_types 
                            SET name = ?, description = ?, base_price = ?, duration_minutes = ?, category = ?
                            WHERE id = ?
                        ''', (name, description, base_price, duration, category, service_id))
                        st.success("Service updated!")
                    else:
                        # Create new
                        try:
                            conn.execute('''
                                INSERT INTO service_types (name, description, base_price, duration_minutes, category)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (name, description, base_price, duration, category))
                            st.success("Service created!")
                        except sqlite3.IntegrityError:
                            st.error("Service name already exists!")
                    
                    conn.commit()
                    st.rerun()
                else:
                    st.error("Name and description are required")
    
    with col2:
        st.markdown("### Current Services")
        
        services = pd.read_sql_query('''
            SELECT id, name, description, base_price, duration_minutes, category, active
            FROM service_types ORDER BY category, name
        ''', conn)
        
        if not services.empty:
            for idx, (_, service) in enumerate(services.iterrows()):
                # Create unique identifier for this service row
                service_unique_id = f"{service['id']}_{idx}_service"
                
                with st.expander(f"{service['name']} - ${service['base_price']}"):
                    st.write(f"**Category:** {service['category']}")
                    st.write(f"**Duration:** {service['duration_minutes']} minutes")
                    st.write(f"**Description:** {service['description']}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        status = "Active" if service['active'] else "Inactive"
                        st.write(f"**Status:** {status}")
                    
                    with col_b:
                        if service['active']:
                            if st.button("Deactivate", key=f"deact_{service_unique_id}"):
                                conn.execute("UPDATE service_types SET active = FALSE WHERE id = ?", (service['id'],))
                                conn.commit()
                                st.rerun()
                        else:
                            if st.button("Activate", key=f"act_{service_unique_id}"):
                                conn.execute("UPDATE service_types SET active = TRUE WHERE id = ?", (service['id'],))
                                conn.commit()
                                st.rerun()
                    
                    with col_c:
                        if st.button("Delete", key=f"del_serv_{service_unique_id}"):
                            conn.execute("DELETE FROM service_types WHERE id = ?", (service['id'],))
                            conn.commit()
                            st.rerun()
        else:
            st.info("No services found")

def show_customer_bookings_tab(conn):
    """Customer bookings management tab"""
    st.subheader("📋 Customer Bookings")
    
    # Get customer bookings from customer portal
    bookings = pd.read_sql_query('''
        SELECT cb.id, cu.first_name, cu.last_name, cu.email, cu.phone,
               st.name as service_name, cb.date, cb.start_time, cb.end_time,
               cb.address, cb.total_price, cb.status, cb.special_instructions,
               cb.created_at
        FROM customer_bookings cb
        JOIN customer_users cu ON cb.customer_user_id = cu.id
        JOIN service_types st ON cb.service_type_id = st.id
        ORDER BY cb.date DESC, cb.start_time DESC
    ''', conn)
    
    if not bookings.empty:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + bookings['status'].unique().tolist())
        
        with col2:
            date_filter = st.date_input("Filter by Date (Optional)", value=None)
        
        with col3:
            service_filter = st.selectbox("Filter by Service", ["All"] + bookings['service_name'].unique().tolist())
        
        # Apply filters
        filtered_bookings = bookings.copy()
        
        if status_filter != "All":
            filtered_bookings = filtered_bookings[filtered_bookings['status'] == status_filter]
        
        if date_filter:
            filtered_bookings = filtered_bookings[filtered_bookings['date'] == date_filter.strftime('%Y-%m-%d')]
        
        if service_filter != "All":
            filtered_bookings = filtered_bookings[filtered_bookings['service_name'] == service_filter]
        
        # Display bookings
        for idx, (_, booking) in enumerate(filtered_bookings.iterrows()):
            status_icon = {
                'pending': '🟡',
                'confirmed': '🟢',
                'completed': '✅',
                'cancelled': '❌'
            }.get(booking['status'], '🔵')
            
            # Create unique identifier for this booking row
            unique_id = f"{booking['id']}_{idx}"
            
            with st.expander(f"{status_icon} {booking['first_name']} {booking['last_name']} - {booking['service_name']} - {booking['date']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Customer:** {booking['first_name']} {booking['last_name']}")
                    st.write(f"**Email:** {booking['email']}")
                    st.write(f"**Phone:** {booking['phone']}")
                    st.write(f"**Service:** {booking['service_name']}")
                    st.write(f"**Date:** {booking['date']}")
                    st.write(f"**Time:** {booking['start_time']} - {booking['end_time']}")
                
                with col2:
                    st.write(f"**Address:** {booking['address']}")
                    st.write(f"**Price:** ${booking['total_price']}")
                    st.write(f"**Status:** {booking['status'].title()}")
                    st.write(f"**Booked:** {booking['created_at']}")
                    if booking['special_instructions']:
                        st.write(f"**Instructions:** {booking['special_instructions']}")
                
                # Status management buttons with unique keys
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if booking['status'] == 'pending':
                        if st.button("Confirm", key=f"confirm_{unique_id}"):
                            conn.execute("UPDATE customer_bookings SET status = 'confirmed' WHERE id = ?", (booking['id'],))
                            conn.commit()
                            st.success("Booking confirmed!")
                            st.rerun()
                
                with col2:
                    if booking['status'] in ['confirmed', 'pending']:
                        if st.button("Complete", key=f"complete_{unique_id}"):
                            conn.execute("UPDATE customer_bookings SET status = 'completed' WHERE id = ?", (booking['id'],))
                            conn.commit()
                            st.success("Booking completed!")
                            st.rerun()
                
                with col3:
                    if booking['status'] not in ['completed', 'cancelled']:
                        if st.button("Cancel", key=f"cancel_{unique_id}"):
                            # Free up the time slot
                            conn.execute('''
                                UPDATE time_slots 
                                SET current_bookings = current_bookings - 1
                                WHERE id = (SELECT slot_id FROM customer_bookings WHERE id = ?)
                                AND current_bookings > 0
                            ''', (booking['id'],))
                            
                            conn.execute("UPDATE customer_bookings SET status = 'cancelled' WHERE id = ?", (booking['id'],))
                            conn.commit()
                            st.warning("Booking cancelled!")
                            st.rerun()
                
                with col4:
                    if st.button("Delete", key=f"delete_{unique_id}"):
                        # Free up the time slot and delete booking
                        conn.execute('''
                            UPDATE time_slots 
                            SET current_bookings = current_bookings - 1
                            WHERE id = (SELECT slot_id FROM customer_bookings WHERE id = ?)
                            AND current_bookings > 0
                        ''', (booking['id'],))
                        
                        conn.execute("DELETE FROM customer_bookings WHERE id = ?", (booking['id'],))
                        conn.commit()
                        st.error("Booking deleted!")
                        st.rerun()
    else:
        st.info("No customer bookings found from the customer portal.")

# Main application
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
