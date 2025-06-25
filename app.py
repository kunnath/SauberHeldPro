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
        # Count customers from both tables
        manual_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        portal_customers = conn.execute("SELECT COUNT(*) FROM customer_users").fetchone()[0]
        total_customers = manual_customers + portal_customers
        st.metric("Total Customers", total_customers, help=f"Manual: {manual_customers}, Portal: {portal_customers}")
    
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
        # Get customers from both tables using UNION
        customers_query = """
        SELECT 
            id,
            name,
            email,
            phone,
            address,
            preferences,
            rating,
            total_jobs,
            created_at,
            'Manual' as source
        FROM customers
        UNION ALL
        SELECT 
            id,
            first_name || ' ' || last_name as name,
            email,
            phone,
            address,
            'Registered via customer portal' as preferences,
            0 as rating,
            0 as total_jobs,
            created_at,
            'Portal Registration' as source
        FROM customer_users
        ORDER BY created_at DESC
        """
        
        customers = pd.read_sql_query(customers_query, conn)
        
        if not customers.empty:
            # Search functionality
            search_term = st.text_input("Search customers by name or email...")
            if search_term:
                customers = customers[
                    (customers['name'].str.contains(search_term, case=False, na=False)) |
                    (customers['email'].str.contains(search_term, case=False, na=False))
                ]
            
            # Display total count
            st.info(f"📊 Total customers: {len(customers)} (from both admin and portal registrations)")
            
            # Display customers
            for _, customer in customers.iterrows():
                # Add source indicator in the title
                source_icon = "🌐" if customer['source'] == 'Portal Registration' else "👤"
                with st.expander(f"{source_icon} {customer['name']} - {customer['email']} ({customer['source']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Phone:** {customer['phone'] if customer['phone'] else 'Not provided'}")
                        st.write(f"**Address:** {customer['address'] if customer['address'] else 'Not provided'}")
                        st.write(f"**Total Jobs:** {customer['total_jobs']}")
                        st.write(f"**Source:** {customer['source']}")
                    with col2:
                        st.write(f"**Rating:** ⭐ {customer['rating']:.1f}")
                        st.write(f"**Joined:** {customer['created_at']}")
                        st.write(f"**Preferences:** {customer['preferences'] if customer['preferences'] else 'None'}")
                        
                        if st.button(f"View Details", key=f"customer_{customer['source']}_{customer['id']}"):
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
    """Enhanced job management and assignment system for managers"""
    st.title("💼 Job Management & Assignment")
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 All Jobs", 
        "👥 Assign Employees", 
        "📊 Job Board", 
        "📦 Bulk Operations",
        "📈 Assignment Analytics"
    ])
    
    conn = init_database()
    
    with tab1:
        show_all_jobs_dashboard(conn)
    
    with tab2:
        show_employee_assignment_interface(conn)
    
    with tab3:
        show_job_board_view(conn)
    
    with tab4:
        show_bulk_operations(conn)
    
    with tab5:
        show_assignment_analytics(conn)

def show_all_jobs_dashboard(conn):
    """Enhanced dashboard showing all jobs with filters and quick actions"""
    st.subheader("📋 Jobs Dashboard")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "pending", "approved", "assigned", "in_progress", "completed", "cancelled"]
        )
    
    with col2:
        date_filter = st.date_input("From Date", value=date.today() - timedelta(days=7))
    
    with col3:
        end_date_filter = st.date_input("To Date", value=date.today() + timedelta(days=7))
    
    with col4:
        employee_filter = st.selectbox(
            "Filter by Employee",
            ["All"] + [emp[1] for emp in conn.execute("SELECT id, name FROM employees").fetchall()]
        )
    
    # Build query with filters
    base_query = '''
        SELECT j.*, c.name as customer_name, c.phone as customer_phone,
               e.name as employee_name, e.hourly_rate as employee_rate
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        LEFT JOIN employees e ON j.employee_id = e.id
        WHERE j.scheduled_date BETWEEN ? AND ?
    '''
    
    params = [date_filter.strftime('%Y-%m-%d'), end_date_filter.strftime('%Y-%m-%d')]
    
    if status_filter != "All":
        base_query += " AND j.status = ?"
        params.append(status_filter)
    
    if employee_filter != "All":
        base_query += " AND e.name = ?"
        params.append(employee_filter)
    
    base_query += " ORDER BY j.scheduled_date, j.scheduled_time"
    
    jobs = pd.read_sql_query(base_query, conn, params=params)
    
    if not jobs.empty:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", len(jobs))
        
        with col2:
            unassigned = len(jobs[jobs['employee_id'].isna()])
            st.metric("Unassigned", unassigned)
        
        with col3:
            in_progress = len(jobs[jobs['status'] == 'in_progress'])
            st.metric("In Progress", in_progress)
        
        with col4:
            total_value = jobs['price'].sum()
            st.metric("Total Value", f"${total_value:.2f}")
        
        st.divider()
        
        # Job cards with enhanced functionality
        for _, job in jobs.iterrows():
            status_colors = {
                'pending': '🟡',
                'approved': '🟠',
                'assigned': '🔵', 
                'in_progress': '🟣',
                'completed': '🟢',
                'cancelled': '🔴'
            }
            
            status_color = status_colors.get(job['status'], '⚪')
            
            with st.expander(f"{status_color} {job['title']} - {job['customer_name']} ({job['status'].title()})"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write("**📅 Schedule**")
                    st.write(f"Date: {job['scheduled_date']}")
                    st.write(f"Time: {job['scheduled_time']}")
                    st.write(f"Duration: {job['duration']} min")
                
                with col2:
                    st.write("**👤 Customer**")
                    st.write(f"Name: {job['customer_name']}")
                    st.write(f"Phone: {job['customer_phone']}")
                    st.write(f"Location: {job['location']}")
                
                with col3:
                    st.write("**💼 Job Details**")
                    st.write(f"Service: {job['service_type']}")
                    st.write(f"Price: ${job['price']:.2f}")
                    st.write(f"Status: {job['status'].title()}")
                
                with col4:
                    st.write("**👷 Assignment**")
                    current_employee = job['employee_name'] if job['employee_name'] else "Not assigned"
                    st.write(f"Employee: {current_employee}")
                    
                    if job['employee_name']:
                        est_cost = (job['duration'] / 60) * job['employee_rate']
                        st.write(f"Est. Cost: ${est_cost:.2f}")
                
                # Action buttons
                st.write("**🔧 Quick Actions**")
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if job['status'] == 'assigned' and st.button("▶️ Start", key=f"start_{job['id']}"):
                        conn.execute("UPDATE jobs SET status = 'in_progress' WHERE id = ?", (job['id'],))
                        conn.commit()
                        st.success("Job started!")
                        st.rerun()
                
                with action_col2:
                    if job['status'] == 'in_progress' and st.button("✅ Complete", key=f"complete_{job['id']}"):
                        conn.execute("UPDATE jobs SET status = 'completed' WHERE id = ?", (job['id'],))
                        conn.commit()
                        st.success("Job completed!")
                        st.rerun()
                
                with action_col3:
                    if job['status'] in ['pending', 'approved'] and st.button("🔄 Reassign", key=f"reassign_{job['id']}"):
                        st.session_state[f'reassign_mode_{job["id"]}'] = True
                        st.rerun()
                
                with action_col4:
                    if st.button("📝 Edit", key=f"edit_{job['id']}"):
                        st.session_state[f'edit_mode_{job["id"]}'] = True
                        st.rerun()
                
                # Reassignment interface
                if st.session_state.get(f'reassign_mode_{job["id"]}', False):
                    st.write("**🔄 Reassign Employee**")
                    employees = pd.read_sql_query("SELECT id, name, employment_type FROM employees", conn)
                    
                    if not employees.empty:
                        new_employee_id = st.selectbox(
                            "Select New Employee",
                            [None] + employees['id'].tolist(),
                            format_func=lambda x: "Remove Assignment" if x is None else f"{employees[employees['id'] == x]['name'].iloc[0]} ({employees[employees['id'] == x]['employment_type'].iloc[0]})",
                            key=f"new_emp_{job['id']}"
                        )
                        
                        reassign_col1, reassign_col2 = st.columns(2)
                        with reassign_col1:
                            if st.button("✅ Confirm Reassign", key=f"confirm_reassign_{job['id']}"):
                                if new_employee_id:
                                    conn.execute("UPDATE jobs SET employee_id = ?, status = 'assigned' WHERE id = ?", 
                                               (new_employee_id, job['id']))
                                else:
                                    conn.execute("UPDATE jobs SET employee_id = NULL, status = 'approved' WHERE id = ?", 
                                               (job['id'],))
                                conn.commit()
                                st.session_state[f'reassign_mode_{job["id"]}'] = False
                                st.success("Employee reassigned!")
                                st.rerun()
                        
                        with reassign_col2:
                            if st.button("❌ Cancel", key=f"cancel_reassign_{job['id']}"):
                                st.session_state[f'reassign_mode_{job["id"]}'] = False
                                st.rerun()
    else:
        st.info("No jobs found with the selected filters")

def show_employee_assignment_interface(conn):
    """Enhanced employee assignment interface"""
    st.subheader("👥 Employee Assignment")
    
    # Get unassigned approved jobs
    unassigned_jobs = pd.read_sql_query('''
        SELECT j.*, c.name as customer_name, c.phone as customer_phone
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        WHERE j.status = 'approved' AND j.employee_id IS NULL
        ORDER BY j.scheduled_date, j.scheduled_time
    ''', conn)
    
    # Get all employees with their current workload
    employees_workload = pd.read_sql_query('''
        SELECT e.id, e.name, e.employment_type, e.hourly_rate, e.skills,
               COUNT(j.id) as current_jobs,
               COALESCE(SUM(j.duration), 0) as total_minutes
        FROM employees e
        LEFT JOIN jobs j ON e.id = j.employee_id AND j.status IN ('assigned', 'in_progress')
        GROUP BY e.id, e.name, e.employment_type, e.hourly_rate, e.skills
        ORDER BY current_jobs, e.name
    ''', conn)
    
    if not unassigned_jobs.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**🎯 Unassigned Jobs**")
            
            for _, job in unassigned_jobs.iterrows():
                with st.expander(f"📋 {job['title']} - {job['customer_name']} ({job['scheduled_date']})"):
                    job_col1, job_col2 = st.columns(2)
                    
                    with job_col1:
                        st.write(f"**Customer:** {job['customer_name']}")
                        st.write(f"**Phone:** {job['customer_phone']}")
                        st.write(f"**Date:** {job['scheduled_date']} at {job['scheduled_time']}")
                        st.write(f"**Duration:** {job['duration']} minutes")
                        st.write(f"**Service:** {job['service_type']}")
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Price:** ${job['price']:.2f}")
                    
                    with job_col2:
                        if not employees_workload.empty:
                            # Smart assignment suggestions
                            st.write("**🤖 Smart Suggestions:**")
                            
                            # Find employees with matching skills
                            job_skills = job['service_type'].lower() if job['service_type'] else ""
                            suitable_employees = []
                            
                            for _, emp in employees_workload.iterrows():
                                emp_skills = emp['skills'].lower() if emp['skills'] else ""
                                skill_match = any(skill in emp_skills for skill in job_skills.split())
                                workload_score = max(0, 10 - emp['current_jobs'])
                                
                                suitable_employees.append({
                                    'id': emp['id'],
                                    'name': emp['name'],
                                    'score': (5 if skill_match else 0) + workload_score,
                                    'workload': emp['current_jobs'],
                                    'hours': emp['total_minutes'] / 60
                                })
                            
                            # Sort by suitability score
                            suitable_employees.sort(key=lambda x: x['score'], reverse=True)
                            
                            # Show top 3 suggestions
                            for i, emp in enumerate(suitable_employees[:3]):
                                icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                                st.write(f"{icon} {emp['name']} (Score: {emp['score']}, Jobs: {emp['workload']})")
                            
                            # Assignment interface
                            st.write("**👤 Assign Employee:**")
                            employee_id = st.selectbox(
                                "Select Employee",
                                employees_workload['id'].tolist(),
                                format_func=lambda x: f"{employees_workload[employees_workload['id'] == x]['name'].iloc[0]} ({employees_workload[employees_workload['id'] == x]['current_jobs'].iloc[0]} jobs)",
                                key=f"assign_emp_{job['id']}"
                            )
                            
                            # Calculate estimated cost
                            selected_emp = employees_workload[employees_workload['id'] == employee_id].iloc[0]
                            est_cost = (job['duration'] / 60) * selected_emp['hourly_rate']
                            
                            st.write(f"**💰 Estimated Cost:** ${est_cost:.2f}")
                            st.write(f"**⏱️ Employee Rate:** ${selected_emp['hourly_rate']:.2f}/hour")
                            
                            if st.button("🎯 Assign Employee", key=f"assign_{job['id']}"):
                                conn.execute("UPDATE jobs SET employee_id = ?, status = 'assigned' WHERE id = ?", 
                                           (employee_id, job['id']))
                                conn.commit()
                                
                                # Log the assignment
                                if LOGGING_ENABLED:
                                    log_user_action('job_management', 'employee_assigned', {
                                        'job_id': job['id'],
                                        'employee_id': employee_id,
                                        'assigned_by': st.session_state.get('username', 'Unknown')
                                    })
                                
                                st.success(f"✅ {selected_emp['name']} assigned to job!")
                                st.rerun()
                        else:
                            st.warning("❌ No employees available. Please add employees first.")
        
        with col2:
            st.write("**👥 Employee Workload**")
            
            if not employees_workload.empty:
                for _, emp in employees_workload.iterrows():
                    workload_color = "🔴" if emp['current_jobs'] >= 5 else "🟡" if emp['current_jobs'] >= 3 else "🟢"
                    
                    with st.container():
                        st.write(f"{workload_color} **{emp['name']}**")
                        st.write(f"Type: {emp['employment_type'].title()}")
                        st.write(f"Current Jobs: {emp['current_jobs']}")
                        st.write(f"Total Hours: {emp['total_minutes']/60:.1f}h")
                        st.write(f"Rate: ${emp['hourly_rate']:.2f}/hr")
                        if emp['skills']:
                            st.write(f"Skills: {emp['skills']}")
                        st.divider()
            else:
                st.info("No employees found")
    else:
        st.info("✅ All approved jobs have been assigned!")
        
        # Show recently assigned jobs
        recent_assignments = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name, e.name as employee_name
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            JOIN employees e ON j.employee_id = e.id
            WHERE j.status = 'assigned' AND j.scheduled_date >= date('now')
            ORDER BY j.created_at DESC
            LIMIT 5
        ''', conn)
        
        if not recent_assignments.empty:
            st.write("**🕒 Recent Assignments:**")
            for _, job in recent_assignments.iterrows():
                st.write(f"• {job['title']} → {job['employee_name']} ({job['scheduled_date']})")

def show_job_board_view(conn):
    """Kanban-style job board view"""
    st.subheader("📊 Job Board (Kanban View)")
    
    # Get jobs grouped by status
    jobs_by_status = {}
    statuses = ['approved', 'assigned', 'in_progress', 'completed']
    
    for status in statuses:
        jobs = pd.read_sql_query('''
            SELECT j.*, c.name as customer_name, e.name as employee_name
            FROM jobs j
            JOIN customers c ON j.customer_id = c.id
            LEFT JOIN employees e ON j.employee_id = e.id
            WHERE j.status = ? AND j.scheduled_date >= date('now', '-7 days')
            ORDER BY j.scheduled_date, j.scheduled_time
        ''', conn, params=[status])
        jobs_by_status[status] = jobs
    
    # Create columns for each status
    col1, col2, col3, col4 = st.columns(4)
    
    columns = [col1, col2, col3, col4]
    column_titles = ['🟠 Approved', '🔵 Assigned', '🟣 In Progress', '🟢 Completed']
    
    for i, (status, jobs) in enumerate(jobs_by_status.items()):
        with columns[i]:
            st.markdown(f"### {column_titles[i]}")
            st.markdown(f"**Count:** {len(jobs)}")
            
            if not jobs.empty:
                for _, job in jobs.iterrows():
                    with st.container():
                        st.markdown(f"**{job['title']}**")
                        st.write(f"Customer: {job['customer_name']}")
                        st.write(f"Date: {job['scheduled_date']}")
                        if job['employee_name']:
                            st.write(f"👤 {job['employee_name']}")
                        st.write(f"💰 ${job['price']:.2f}")
                        
                        # Quick action buttons
                        if status == 'assigned':
                            if st.button("▶️ Start", key=f"board_start_{job['id']}"):
                                conn.execute("UPDATE jobs SET status = 'in_progress' WHERE id = ?", (job['id'],))
                                conn.commit()
                                st.rerun()
                        elif status == 'in_progress':
                            if st.button("✅ Complete", key=f"board_complete_{job['id']}"):
                                conn.execute("UPDATE jobs SET status = 'completed' WHERE id = ?", (job['id'],))
                                conn.commit()
                                st.rerun()
                        
                        st.divider()
            else:
                st.info("No jobs in this status")

def show_bulk_operations(conn):
    """Bulk operations for job management"""
    st.subheader("📦 Bulk Operations")
    
    # Bulk assignment
    st.write("### 🎯 Bulk Assignment")
    
    # Get unassigned jobs
    unassigned_jobs = pd.read_sql_query('''
        SELECT j.id, j.title, j.scheduled_date, j.scheduled_time, c.name as customer_name
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        WHERE j.status = 'approved' AND j.employee_id IS NULL
        ORDER BY j.scheduled_date, j.scheduled_time
    ''', conn)
    
    if not unassigned_jobs.empty:
        # Multi-select jobs
        selected_jobs = st.multiselect(
            "Select Jobs for Bulk Assignment",
            unassigned_jobs['id'].tolist(),
            format_func=lambda x: f"{unassigned_jobs[unassigned_jobs['id'] == x]['title'].iloc[0]} - {unassigned_jobs[unassigned_jobs['id'] == x]['customer_name'].iloc[0]} ({unassigned_jobs[unassigned_jobs['id'] == x]['scheduled_date'].iloc[0]})"
        )
        
        if selected_jobs:
            # Select employee for bulk assignment
            employees = pd.read_sql_query("SELECT id, name, employment_type FROM employees", conn)
            
            if not employees.empty:
                bulk_employee_id = st.selectbox(
                    "Assign to Employee",
                    employees['id'].tolist(),
                    format_func=lambda x: f"{employees[employees['id'] == x]['name'].iloc[0]} ({employees[employees['id'] == x]['employment_type'].iloc[0]})"
                )
                
                if st.button("🎯 Bulk Assign Selected Jobs"):
                    for job_id in selected_jobs:
                        conn.execute("UPDATE jobs SET employee_id = ?, status = 'assigned' WHERE id = ?", 
                                   (bulk_employee_id, job_id))
                    conn.commit()
                    
                    employee_name = employees[employees['id'] == bulk_employee_id]['name'].iloc[0]
                    st.success(f"✅ {len(selected_jobs)} jobs assigned to {employee_name}!")
                    st.rerun()
    else:
        st.info("No unassigned jobs available for bulk operations")
    
    st.divider()
    
    # Bulk status update
    st.write("### 📋 Bulk Status Update")
    
    status_jobs = pd.read_sql_query('''
        SELECT j.id, j.title, j.status, j.scheduled_date, c.name as customer_name, e.name as employee_name
        FROM jobs j
        JOIN customers c ON j.customer_id = c.id
        LEFT JOIN employees e ON j.employee_id = e.id
        WHERE j.status IN ('assigned', 'in_progress')
        ORDER BY j.scheduled_date, j.scheduled_time
    ''', conn)
    
    if not status_jobs.empty:
        selected_status_jobs = st.multiselect(
            "Select Jobs for Status Update",
            status_jobs['id'].tolist(),
            format_func=lambda x: f"{status_jobs[status_jobs['id'] == x]['title'].iloc[0]} - {status_jobs[status_jobs['id'] == x]['customer_name'].iloc[0]} (Current: {status_jobs[status_jobs['id'] == x]['status'].iloc[0]})"
        )
        
        if selected_status_jobs:
            new_status = st.selectbox(
                "New Status",
                ['assigned', 'in_progress', 'completed', 'cancelled']
            )
            
            if st.button("📋 Update Status for Selected Jobs"):
                for job_id in selected_status_jobs:
                    conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))
                conn.commit()
                
                st.success(f"✅ {len(selected_status_jobs)} jobs updated to '{new_status}' status!")
                st.rerun()

def show_assignment_analytics(conn):
    """Analytics dashboard for job assignments"""
    st.subheader("📈 Assignment Analytics")
    
    # Time period selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To Date", value=date.today())
    
    # Employee performance metrics
    employee_metrics = pd.read_sql_query('''
        SELECT e.name, e.employment_type,
               COUNT(j.id) as total_jobs,
               SUM(CASE WHEN j.status = 'completed' THEN 1 ELSE 0 END) as completed_jobs,
               ROUND(AVG(j.duration), 2) as avg_duration,
               ROUND(SUM(j.price), 2) as total_revenue,
               ROUND(AVG(j.price), 2) as avg_job_value
        FROM employees e
        LEFT JOIN jobs j ON e.id = j.employee_id 
        WHERE j.scheduled_date BETWEEN ? AND ? OR j.scheduled_date IS NULL
        GROUP BY e.id, e.name, e.employment_type
        ORDER BY completed_jobs DESC
    ''', conn, params=[start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
    
    if not employee_metrics.empty:
        # Performance overview
        st.write("### 👤 Employee Performance")
        
        # Calculate completion rate
        employee_metrics['completion_rate'] = (
            employee_metrics['completed_jobs'] / 
            employee_metrics['total_jobs'].replace(0, 1) * 100
        ).round(2)
        
        # Display metrics
        for _, emp in employee_metrics.iterrows():
            with st.expander(f"📊 {emp['name']} ({emp['employment_type'].title()})"):
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("Total Jobs", emp['total_jobs'])
                    st.metric("Completed", emp['completed_jobs'])
                
                with metric_col2:
                    st.metric("Completion Rate", f"{emp['completion_rate']:.1f}%")
                    st.metric("Avg Duration", f"{emp['avg_duration']:.0f} min")
                
                with metric_col3:
                    st.metric("Total Revenue", f"${emp['total_revenue']:.2f}")
                    st.metric("Avg Job Value", f"${emp['avg_job_value']:.2f}")
                
                with metric_col4:
                    # Performance rating
                    if emp['completion_rate'] >= 90:
                        rating = "⭐⭐⭐⭐⭐ Excellent"
                    elif emp['completion_rate'] >= 80:
                        rating = "⭐⭐⭐⭐ Very Good"
                    elif emp['completion_rate'] >= 70:
                        rating = "⭐⭐⭐ Good"
                    else:
                        rating = "⭐⭐ Needs Improvement"
                    
                    st.write("**Performance Rating:**")
                    st.write(rating)
        
        # Charts
        st.write("### 📊 Visual Analytics")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Employee workload chart
            fig_workload = px.bar(
                employee_metrics,
                x='name',
                y='total_jobs',
                title='Jobs by Employee',
                color='employment_type'
            )
            st.plotly_chart(fig_workload, use_container_width=True)
        
        with chart_col2:
            # Completion rate chart
            fig_completion = px.bar(
                employee_metrics,
                x='name',
                y='completion_rate',
                title='Completion Rate by Employee (%)',
                color='completion_rate',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_completion, use_container_width=True)
    
    # Job status overview
    st.write("### 📋 Job Status Overview")
    
    status_metrics = pd.read_sql_query('''
        SELECT status, COUNT(*) as count
        FROM jobs
        WHERE scheduled_date BETWEEN ? AND ?
        GROUP BY status
        ORDER BY count DESC
    ''', conn, params=[start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
    
    if not status_metrics.empty:
        fig_status = px.pie(
            status_metrics,
            values='count',
            names='status',
            title='Jobs by Status'
        )
        st.plotly_chart(fig_status, use_container_width=True)

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
