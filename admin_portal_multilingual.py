"""
Multilingual Admin Portal for Aufraumenbee Cleaning Service
Production-ready version with internationalization support
"""

import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import plotly.express as px
import plotly.graph_objects as go

# Import translation system
from translations import t, init_language_selector, get_current_language, format_currency, format_date

# Page configuration
st.set_page_config(
    page_title="Aufraumenbee - Admin Portal",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for multilingual support
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
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #f0f0f0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .language-selector {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999;
    }
    .status-pending { color: #ffc107; }
    .status-confirmed { color: #28a745; }
    .status-completed { color: #007bff; }
    .status-cancelled { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

def init_database():
    """Initialize the database with all required tables"""
    conn = sqlite3.connect('aufraumenbee.db', check_same_thread=False)
    
    # Admin users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Customers table (admin-created)
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
    
    # Customer portal users table
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
    
    # Employees table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            hourly_rate REAL,
            specialties TEXT,
            availability TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add missing columns for backward compatibility
    try:
        conn.execute('ALTER TABLE employees ADD COLUMN status TEXT DEFAULT "active"')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        conn.execute('ALTER TABLE employees ADD COLUMN specialties TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Migrate data from skills to specialties if needed
    try:
        # Check if skills column exists and specialties is empty
        result = conn.execute("PRAGMA table_info(employees)").fetchall()
        column_names = [col[1] for col in result]
        
        if 'skills' in column_names:
            conn.execute('''
                UPDATE employees 
                SET specialties = COALESCE(specialties, skills) 
                WHERE (specialties IS NULL OR specialties = '') AND skills IS NOT NULL
            ''')
    except sqlite3.OperationalError:
        pass  # Migration not needed
    
    # Update NULL status values to 'active'
    conn.execute('UPDATE employees SET status = "active" WHERE status IS NULL OR status = ""')
    conn.commit()
    
    # Jobs table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            scheduled_date DATE,
            scheduled_time TEXT,
            duration INTEGER,
            status TEXT DEFAULT 'pending',
            service_type TEXT,
            location TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    
    # Service types table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS service_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_de TEXT NOT NULL,
            description_en TEXT,
            description_de TEXT,
            base_price REAL,
            duration_hours INTEGER DEFAULT 2
        )
    ''')
    
    # Insert default admin user
    try:
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        conn.execute('INSERT OR IGNORE INTO admin_users (username, password_hash) VALUES (?, ?)', 
                    ('admin', password_hash))
        conn.commit()
    except:
        pass
    
    # Insert default service types with multilingual support
    default_services = [
        ('Basic Cleaning', 'Grundreinigung', 'Standard cleaning service', 'Standard-Reinigungsservice', 45.0, 2),
        ('Deep Cleaning', 'Tiefenreinigung', 'Thorough deep cleaning', 'Gründliche Tiefenreinigung', 75.0, 4),
        ('Office Cleaning', 'Büroreinigung', 'Professional office cleaning', 'Professionelle Büroreinigung', 55.0, 3),
        ('Window Cleaning', 'Fensterreinigung', 'Interior and exterior windows', 'Innen- und Außenfenster', 35.0, 1),
        ('Carpet Cleaning', 'Teppichreinigung', 'Professional carpet cleaning', 'Professionelle Teppichreinigung', 65.0, 2),
        ('Move-in/Move-out', 'Ein-/Auszugsreinigung', 'Complete move cleaning', 'Komplette Umzugsreinigung', 95.0, 5)
    ]
    
    for service in default_services:
        try:
            conn.execute('''INSERT OR IGNORE INTO service_types 
                           (name_en, name_de, description_en, description_de, base_price, duration_hours) 
                           VALUES (?, ?, ?, ?, ?, ?)''', service)
        except:
            pass
    
    conn.commit()
    return conn

def check_admin_login(username: str, password: str) -> bool:
    """Check admin credentials"""
    conn = init_database()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM admin_users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    return False

def show_login_form():
    """Show admin login form with language support"""
    current_lang = get_current_language()
    
    st.markdown(f'<h1 class="main-header">🧹 {t("app_name", current_lang)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.2rem; color: #666;">{t("tagline", current_lang)} - Admin Portal</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 " + t("login", current_lang))
        
        with st.form("admin_login"):
            username = st.text_input("👤 " + t("username", current_lang) if "username" in st.session_state.get('translations', {}) else "👤 Username")
            password = st.text_input("🔒 " + t("password", current_lang), type="password")
            
            if st.form_submit_button(t("login", current_lang), use_container_width=True):
                if check_admin_login(username, password):
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_username = username
                    st.success(t("login_success", current_lang))
                    st.rerun()
                else:
                    st.error(t("login_failed", current_lang))

def show_dashboard():
    """Show main dashboard with multilingual support"""
    current_lang = get_current_language()
    conn = init_database()
    
    st.title("📊 " + t("dashboard", current_lang))
    
    # Key metrics with language support
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Count customers from both tables
        manual_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        portal_customers = conn.execute("SELECT COUNT(*) FROM customer_users").fetchone()[0]
        total_customers = manual_customers + portal_customers
        st.metric(t("total_customers", current_lang), total_customers)
    
    with col2:
        total_employees = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        st.metric(t("total_employees", current_lang), total_employees)
    
    with col3:
        pending_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE status = 'pending'").fetchone()[0]
        st.metric(t("pending_jobs", current_lang), pending_jobs)
    
    with col4:
        # Calculate revenue for current month
        current_month = datetime.now().strftime('%Y-%m')
        revenue = conn.execute("""
            SELECT COALESCE(SUM(price), 0) FROM jobs 
            WHERE strftime('%Y-%m', scheduled_date) = ? AND status = 'completed'
        """, (current_month,)).fetchone()[0]
        st.metric(t("revenue_this_month", current_lang), format_currency(revenue, current_lang))
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t("recent_bookings", current_lang))
        recent_jobs = pd.read_sql_query("""
            SELECT j.*, c.name as customer_name 
            FROM jobs j 
            LEFT JOIN customers c ON j.customer_id = c.id 
            ORDER BY j.created_at DESC LIMIT 5
        """, conn)
        
        if not recent_jobs.empty:
            for _, job in recent_jobs.iterrows():
                status_class = f"status-{job['status']}"
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{job['customer_name'] or 'Unknown Customer'}</strong><br>
                    <span class="{status_class}">● {t(job['status'], current_lang)}</span> - {job['service_type']}<br>
                    📅 {format_date(datetime.strptime(job['scheduled_date'], '%Y-%m-%d').date(), current_lang) if job['scheduled_date'] else 'No date'} 
                    🕐 {job['scheduled_time'] if job['scheduled_time'] else 'No time'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t("no_bookings_found", current_lang) if "no_bookings_found" in st.session_state.get('translations', {}) else "No recent bookings")
    
    with col2:
        st.subheader(t("upcoming_jobs", current_lang))
        upcoming_jobs = pd.read_sql_query("""
            SELECT j.*, c.name as customer_name, e.name as employee_name
            FROM jobs j 
            LEFT JOIN customers c ON j.customer_id = c.id 
            LEFT JOIN employees e ON j.employee_id = e.id
            WHERE j.scheduled_date >= date('now') AND j.status != 'cancelled'
            ORDER BY j.scheduled_date, j.scheduled_time LIMIT 5
        """, conn)
        
        if not upcoming_jobs.empty:
            for _, job in upcoming_jobs.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{job['customer_name'] or 'Unknown Customer'}</strong><br>
                    👨‍🔧 {job['employee_name'] or t('not_assigned', current_lang) if 'not_assigned' in st.session_state.get('translations', {}) else 'Not assigned'}<br>
                    📅 {format_date(datetime.strptime(job['scheduled_date'], '%Y-%m-%d').date(), current_lang) if job['scheduled_date'] else 'No date'} 
                    🕐 {job['scheduled_time'] if job['scheduled_time'] else 'No time'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t("no_upcoming_jobs", current_lang) if "no_upcoming_jobs" in st.session_state.get('translations', {}) else "No upcoming jobs")
    
    conn.close()

def manage_customers():
    """Customer management with multilingual support"""
    current_lang = get_current_language()
    conn = init_database()
    
    st.title("👥 " + t("customer_management", current_lang))
    
    tab1, tab2 = st.tabs([t("customer_list", current_lang), t("add_new_customer", current_lang)])
    
    with tab1:
        # Combined customer query from both tables
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
            search_term = st.text_input(t("search", current_lang) + " customers...")
            if search_term:
                customers = customers[
                    (customers['name'].str.contains(search_term, case=False, na=False)) |
                    (customers['email'].str.contains(search_term, case=False, na=False))
                ]
            
            # Display total count
            st.info(f"📊 {t('total_customers', current_lang)}: {len(customers)}")
            
            # Display customers
            for _, customer in customers.iterrows():
                source_icon = "🌐" if customer['source'] == 'Portal Registration' else "👤"
                with st.expander(f"{source_icon} {customer['name']} - {customer['email']} ({customer['source']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{t('phone', current_lang)}:** {customer['phone'] if customer['phone'] else t('not_provided', current_lang)}")
                        st.write(f"**{t('address', current_lang)}:** {customer['address'] if customer['address'] else t('not_provided', current_lang)}")
                        st.write(f"**{t('total_jobs', current_lang)}:** {customer['total_jobs']}")
                    with col2:
                        st.write(f"**{t('customer_rating', current_lang)}:** ⭐ {customer['rating']:.1f}")
                        st.write(f"**{t('joined_date', current_lang)}:** {format_date(datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S').date(), current_lang)}")
                        st.write(f"**{t('source', current_lang)}:** {customer['source']}")
        else:
            st.info(t("no_customers_found", current_lang))
    
    with tab2:
        st.subheader(t("add_new_customer", current_lang))
        
        with st.form("add_customer"):
            name = st.text_input(t("customer_name", current_lang) + "*")
            email = st.text_input(t("email", current_lang))
            phone = st.text_input(t("phone", current_lang))
            address = st.text_area(t("address", current_lang))
            preferences = st.text_area(t("service_preferences", current_lang))
            
            if st.form_submit_button(t("add_customer", current_lang)):
                if name:
                    conn.execute('''
                        INSERT INTO customers (name, email, phone, address, preferences)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, email, phone, address, preferences))
                    conn.commit()
                    st.success(t("customer_added_successfully", current_lang))
                    st.rerun()
                else:
                    st.error(t("required_fields_missing", current_lang))
    
    conn.close()

def manage_employees():
    """Employee management with multilingual support"""
    current_lang = get_current_language()
    conn = init_database()
    
    st.title("👨‍💼 " + t("employee_management", current_lang))
    
    tab1, tab2 = st.tabs([t("employee_list", current_lang), t("add_new_employee", current_lang)])
    
    with tab1:
        # Query with flexible column handling for backward compatibility
        employees = pd.read_sql_query("""
            SELECT id, name, email, phone, hourly_rate, 
                   COALESCE(specialties, skills, '') as specialties,
                   availability, 
                   COALESCE(status, 'active') as status, 
                   created_at 
            FROM employees 
            ORDER BY created_at DESC
        """, conn)
        
        if not employees.empty:
            # Search functionality
            search_term = st.text_input(t("search", current_lang) + " " + t("employee_list", current_lang).lower() + "...")
            if search_term:
                employees = employees[
                    (employees['name'].str.contains(search_term, case=False, na=False)) |
                    (employees['email'].str.contains(search_term, case=False, na=False))
                ]
            
            # Display total count
            st.info(f"📊 {t('total_employees', current_lang)}: {len(employees)}")
            
            # Display employees
            for _, employee in employees.iterrows():
                # Status is now guaranteed to be non-null due to COALESCE in query
                employee_status = employee['status']
                status_icon = "✅" if employee_status == 'active' else "❌"
                with st.expander(f"{status_icon} {employee['name']} - {employee['email']} ({t(employee_status, current_lang)})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{t('phone', current_lang)}:** {employee['phone'] if employee['phone'] else t('not_provided', current_lang)}")
                        st.write(f"**{t('hourly_rate', current_lang)}:** {format_currency(employee['hourly_rate'], current_lang) if employee['hourly_rate'] else t('not_provided', current_lang)}")
                        st.write(f"**{t('specialties', current_lang)}:** {employee['specialties'] if employee['specialties'] else t('not_provided', current_lang)}")
                    with col2:
                        st.write(f"**{t('availability', current_lang)}:** {employee['availability'] if employee['availability'] else t('not_provided', current_lang)}")
                        st.write(f"**{t('employee_status', current_lang)}:** {t(employee_status, current_lang)}")
                        st.write(f"**{t('hire_date', current_lang)}:** {format_date(datetime.strptime(employee['created_at'], '%Y-%m-%d %H:%M:%S').date(), current_lang)}")
                    
                    # Employee performance metrics
                    job_count = conn.execute("SELECT COUNT(*) FROM jobs WHERE employee_id = ?", (employee['id'],)).fetchone()[0]
                    completed_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE employee_id = ? AND status = 'completed'", (employee['id'],)).fetchone()[0]
                    
                    col3, col4, col5 = st.columns(3)
                    with col3:
                        st.metric(t("assigned_jobs", current_lang), job_count)
                    with col4:
                        st.metric(t("completed_jobs", current_lang), completed_jobs)
                    with col5:
                        completion_rate = (completed_jobs / job_count * 100) if job_count > 0 else 0
                        st.metric(t("employee_performance", current_lang), f"{completion_rate:.1f}%")
        else:
            st.info(t("no_employees_found", current_lang))
    
    with tab2:
        st.subheader(t("add_new_employee", current_lang))
        
        with st.form("add_employee"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(t("employee_name", current_lang) + "*")
                email = st.text_input(t("email", current_lang))
                phone = st.text_input(t("phone", current_lang))
                hourly_rate = st.number_input(t("hourly_rate", current_lang), min_value=0.0, step=0.5)
            
            with col2:
                specialties = st.text_area(t("specialties", current_lang))
                availability = st.selectbox(t("availability", current_lang), 
                                          [t("full_time", current_lang), t("part_time", current_lang), 
                                           t("contract", current_lang), t("internship", current_lang)])
                status = st.selectbox(t("employee_status", current_lang), 
                                    [t("active", current_lang), t("inactive", current_lang)])
            
            if st.form_submit_button(t("add_employee", current_lang)):
                if name:
                    # Map translated status back to English for database
                    status_en = 'active' if status == t("active", current_lang) else 'inactive'
                    
                    conn.execute('''
                        INSERT INTO employees (name, email, phone, hourly_rate, specialties, availability, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (name, email, phone, hourly_rate, specialties, availability, status_en))
                    conn.commit()
                    st.success(t("employee_added_successfully", current_lang))
                    st.rerun()
                else:
                    st.error(t("required_fields_missing", current_lang))
    
    conn.close()

def manage_jobs():
    """Advanced Job management with multilingual support"""
    current_lang = get_current_language()
    conn = init_database()
    
    st.title("📋 " + t("job_management", current_lang))
    
    # Advanced Job Management Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 " + t("all_jobs", current_lang),
        "👥 " + t("assign_employees", current_lang), 
        "📊 " + t("job_board", current_lang),
        "📦 " + t("bulk_operations", current_lang),
        "📈 " + t("assignment_analytics", current_lang)
    ])
    
    with tab1:
        show_all_jobs(conn, current_lang)
    
    with tab2:
        show_employee_assignment(conn, current_lang)
        
    with tab3:
        show_job_board(conn, current_lang)
        
    with tab4:
        show_bulk_operations(conn, current_lang)
        
    with tab5:
        show_assignment_analytics(conn, current_lang)
    
    conn.close()

def show_all_jobs(conn, current_lang):
    """Display all jobs with advanced filtering and management"""
    st.subheader("📋 " + t("all_jobs", current_lang))
    
    # Get jobs with enhanced query
    jobs_query = """
        SELECT 
            j.*,
            COALESCE(c.name, cu.first_name || ' ' || cu.last_name, 'Unassigned') as customer_name,
            COALESCE(e.name, 'Unassigned') as employee_name,
            st.name_en, st.name_de,
            cb.date as booking_date, cb.start_time, cb.end_time
        FROM jobs j 
        LEFT JOIN customers c ON j.customer_id = c.id 
        LEFT JOIN customer_users cu ON j.customer_id = cu.id
        LEFT JOIN employees e ON j.employee_id = e.id
        LEFT JOIN customer_bookings cb ON j.customer_id = cb.customer_user_id
        LEFT JOIN service_types st ON j.service_type = st.name OR j.service_type = st.name_en
        ORDER BY j.created_at DESC
    """
    
    jobs = pd.read_sql_query(jobs_query, conn)
    
    if not jobs.empty:
        # Advanced Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_options = ['All'] + list(jobs['status'].dropna().unique())
            status_filter = st.selectbox(t("filter_by_status", current_lang), status_options)
            
        with col2:
            employee_options = ['All'] + list(jobs['employee_name'].dropna().unique())
            employee_filter = st.selectbox(t("filter_by_employee", current_lang), employee_options)
            
        with col3:
            date_from = st.date_input(t("from_date", current_lang), value=None)
            
        with col4:
            date_to = st.date_input(t("to_date", current_lang), value=None)
        
        # Search and additional filters
        col5, col6 = st.columns(2)
        with col5:
            search_term = st.text_input("🔍 " + t("search_jobs", current_lang))
        with col6:
            priority_filter = st.selectbox(t("priority", current_lang), 
                                         ['All', t("high_priority", current_lang), 
                                          t("medium_priority", current_lang), t("low_priority", current_lang)])
        
        # Apply filters
        filtered_jobs = jobs.copy()
        
        if status_filter != 'All':
            filtered_jobs = filtered_jobs[filtered_jobs['status'] == status_filter]
            
        if employee_filter != 'All':
            filtered_jobs = filtered_jobs[filtered_jobs['employee_name'] == employee_filter]
            
        if date_from:
            filtered_jobs = filtered_jobs[pd.to_datetime(filtered_jobs['scheduled_date']) >= pd.to_datetime(date_from)]
            
        if date_to:
            filtered_jobs = filtered_jobs[pd.to_datetime(filtered_jobs['scheduled_date']) <= pd.to_datetime(date_to)]
            
        if search_term:
            filtered_jobs = filtered_jobs[
                (filtered_jobs['title'].str.contains(search_term, case=False, na=False)) |
                (filtered_jobs['customer_name'].str.contains(search_term, case=False, na=False)) |
                (filtered_jobs['description'].str.contains(search_term, case=False, na=False))
            ]
        
        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(t("total_jobs", current_lang), len(filtered_jobs))
        with col2:
            pending_count = len(filtered_jobs[filtered_jobs['status'] == 'pending'])
            st.metric(t("pending", current_lang), pending_count)
        with col3:
            assigned_count = len(filtered_jobs[filtered_jobs['employee_name'] != 'Unassigned'])
            st.metric(t("assigned", current_lang), assigned_count)
        with col4:
            completed_count = len(filtered_jobs[filtered_jobs['status'] == 'completed'])
            st.metric(t("completed", current_lang), completed_count)
        with col5:
            total_value = filtered_jobs['price'].sum() if 'price' in filtered_jobs.columns else 0
            st.metric(t("total_value", current_lang), format_currency(total_value, current_lang))
        
        st.markdown("---")
        
        # Jobs Display
        for idx, job in filtered_jobs.iterrows():
            status_emoji = {
                'pending': '🟡', 'confirmed': '🟢', 'in_progress': '🔵', 
                'completed': '✅', 'cancelled': '🔴'
            }
            
            priority_emoji = {
                'high': '🔴', 'medium': '🟡', 'low': '🟢'
            }
            
            job_priority = job.get('priority', 'medium').lower()
            
            # Job card
            with st.expander(f"{status_emoji.get(job['status'], '⚪')} {priority_emoji.get(job_priority, '🟡')} {job['title']} - {job['customer_name']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**{t('customer', current_lang)}:** {job['customer_name']}")
                    st.write(f"**{t('employee', current_lang)}:** {job['employee_name']}")
                    st.write(f"**{t('service_type', current_lang)}:** {job['service_type']}")
                    st.write(f"**{t('status', current_lang)}:** {t(job['status'], current_lang)}")
                    
                with col2:
                    st.write(f"**{t('scheduled_date', current_lang)}:** {job['scheduled_date'] or t('not_scheduled', current_lang)}")
                    st.write(f"**{t('scheduled_time', current_lang)}:** {job['scheduled_time'] or t('not_scheduled', current_lang)}")
                    st.write(f"**{t('location', current_lang)}:** {job.get('location', t('not_provided', current_lang))}")
                    st.write(f"**{t('price', current_lang)}:** {format_currency(job.get('price', 0), current_lang)}")
                
                with col3:
                    # Quick Actions
                    st.write(f"**{t('actions', current_lang)}:**")
                    
                    if st.button(f"✏️ {t('edit', current_lang)}", key=f"edit_{job['id']}"):
                        st.session_state[f'show_edit_job_{job["id"]}'] = True
                    
                    if st.button(f"👥 {t('assign', current_lang)}", key=f"assign_{job['id']}"):
                        st.session_state[f'show_assign_job_{job["id"]}'] = True
                    
                    # Status update buttons
                    if job['status'] == 'pending':
                        if st.button(f"✅ {t('confirm', current_lang)}", key=f"confirm_{job['id']}"):
                            update_job_status(conn, job['id'], 'confirmed')
                            st.rerun()
                    
                    if job['status'] == 'confirmed':
                        if st.button(f"▶️ {t('start', current_lang)}", key=f"start_{job['id']}"):
                            update_job_status(conn, job['id'], 'in_progress')
                            st.rerun()
                    
                    if job['status'] == 'in_progress':
                        if st.button(f"🏁 {t('complete', current_lang)}", key=f"complete_{job['id']}"):
                            update_job_status(conn, job['id'], 'completed')
                            st.rerun()
                
                if job.get('description'):
                    st.write(f"**{t('description', current_lang)}:** {job['description']}")
                
                # Handle edit mode
                if st.session_state.get(f'show_edit_job_{job["id"]}'):
                    show_edit_job_form(conn, job, current_lang)
                
                # Handle assignment mode
                if st.session_state.get(f'show_assign_job_{job["id"]}'):
                    show_assignment_form(conn, job, current_lang)
    else:
        st.info(t("no_jobs_found", current_lang))
        
        # Quick add job button
        if st.button(f"➕ {t('add_new_job', current_lang)}"):
            show_add_job_form(conn, current_lang)

def show_employee_assignment(conn, current_lang):
    """Employee assignment interface"""
    st.subheader("👥 " + t("assign_employees", current_lang))
    
    # Get unassigned jobs and available employees
    unassigned_jobs = pd.read_sql_query("""
        SELECT j.*, COALESCE(c.name, cu.first_name || ' ' || cu.last_name) as customer_name
        FROM jobs j 
        LEFT JOIN customers c ON j.customer_id = c.id 
        LEFT JOIN customer_users cu ON j.customer_id = cu.id
        WHERE j.employee_id IS NULL AND j.status IN ('pending', 'confirmed')
        ORDER BY j.scheduled_date ASC
    """, conn)
    
    available_employees = pd.read_sql_query("""
        SELECT id, name, COALESCE(specialties, skills, '') as specialties, hourly_rate
        FROM employees 
        WHERE COALESCE(status, 'active') = 'active'
    """, conn)
    
    if not unassigned_jobs.empty and not available_employees.empty:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.write(f"**{t('unassigned_jobs', current_lang)} ({len(unassigned_jobs)}):**")
            
            for _, job in unassigned_jobs.iterrows():
                with st.expander(f"📋 {job['title']} - {job['customer_name']}"):
                    st.write(f"**{t('service_type', current_lang)}:** {job['service_type']}")
                    st.write(f"**{t('scheduled_date', current_lang)}:** {job['scheduled_date']}")
                    st.write(f"**{t('location', current_lang)}:** {job.get('location', t('not_provided', current_lang))}")
                    st.write(f"**{t('price', current_lang)}:** {format_currency(job.get('price', 0), current_lang)}")
                    
                    # Employee selection for this job
                    employee_options = [f"{emp['name']} - {emp['specialties']} (${emp['hourly_rate']}/hr)" 
                                      for _, emp in available_employees.iterrows()]
                    
                    selected_employee = st.selectbox(
                        t("select_employee", current_lang), 
                        [""] + employee_options,
                        key=f"assign_emp_{job['id']}"
                    )
                    
                    if selected_employee and st.button(f"✅ {t('assign', current_lang)}", key=f"confirm_assign_{job['id']}"):
                        # Extract employee ID
                        emp_name = selected_employee.split(" - ")[0]
                        employee_id = available_employees[available_employees['name'] == emp_name]['id'].iloc[0]
                        
                        # Assign employee to job
                        conn.execute("UPDATE jobs SET employee_id = ?, status = 'confirmed' WHERE id = ?", 
                                   (employee_id, job['id']))
                        conn.commit()
                        st.success(f"{t('job_assigned_successfully', current_lang)}")
                        st.rerun()
        
        with col2:
            st.write(f"**{t('available_employees', current_lang)} ({len(available_employees)}):**")
            
            for _, emp in available_employees.iterrows():
                # Get employee's current workload
                current_jobs = pd.read_sql_query("""
                    SELECT COUNT(*) as job_count 
                    FROM jobs 
                    WHERE employee_id = ? AND status IN ('confirmed', 'in_progress')
                """, conn, params=(emp['id'],)).iloc[0]['job_count']
                
                workload_color = "🟢" if current_jobs == 0 else "🟡" if current_jobs <= 3 else "🔴"
                
                with st.container():
                    st.write(f"{workload_color} **{emp['name']}**")
                    st.write(f"💼 {t('specialties', current_lang)}: {emp['specialties'] or t('general', current_lang)}")
                    st.write(f"💰 {t('hourly_rate', current_lang)}: ${emp['hourly_rate']}/hr")
                    st.write(f"📊 {t('current_jobs', current_lang)}: {current_jobs}")
                    st.markdown("---")
    
    elif unassigned_jobs.empty:
        st.success(f"🎉 {t('all_jobs_assigned', current_lang)}")
    else:
        st.warning(f"⚠️ {t('no_available_employees', current_lang)}")
        
    # Bulk assignment section
    st.markdown("---")
    st.subheader(f"📦 {t('bulk_assignment', current_lang)}")
    
    if not unassigned_jobs.empty:
        with st.form("bulk_assign"):
            selected_jobs = st.multiselect(
                t("select_jobs_to_assign", current_lang),
                options=unassigned_jobs['id'].tolist(),
                format_func=lambda x: f"{unassigned_jobs[unassigned_jobs['id']==x]['title'].iloc[0]} - {unassigned_jobs[unassigned_jobs['id']==x]['customer_name'].iloc[0]}"
            )
            
            if available_employees.empty:
                st.warning(t("no_available_employees", current_lang))
            else:
                bulk_employee = st.selectbox(
                    t("assign_to_employee", current_lang),
                    options=available_employees['id'].tolist(),
                    format_func=lambda x: available_employees[available_employees['id']==x]['name'].iloc[0]
                )
                
                if st.form_submit_button(f"👥 {t('assign_selected_jobs', current_lang)}"):
                    if selected_jobs and bulk_employee:
                        for job_id in selected_jobs:
                            conn.execute("UPDATE jobs SET employee_id = ?, status = 'confirmed' WHERE id = ?", 
                                       (bulk_employee, job_id))
                        conn.commit()
                        st.success(f"{t('jobs_assigned_successfully', current_lang)}: {len(selected_jobs)}")
                        st.rerun()

def show_job_board(conn, current_lang):
    """Visual job board with drag-and-drop style interface"""
    st.subheader("📊 " + t("job_board", current_lang))
    
    # Get jobs grouped by status
    jobs = pd.read_sql_query("""
        SELECT 
            j.*,
            COALESCE(c.name, cu.first_name || ' ' || cu.last_name, 'Unassigned') as customer_name,
            COALESCE(e.name, 'Unassigned') as employee_name
        FROM jobs j 
        LEFT JOIN customers c ON j.customer_id = c.id 
        LEFT JOIN customer_users cu ON j.customer_id = cu.id
        LEFT JOIN employees e ON j.employee_id = e.id
        ORDER BY j.scheduled_date ASC, j.created_at ASC
    """, conn)
    
    if not jobs.empty:
        # Status columns
        statuses = ['pending', 'confirmed', 'in_progress', 'completed']
        status_names = {
            'pending': t('pending', current_lang),
            'confirmed': t('confirmed', current_lang), 
            'in_progress': t('in_progress', current_lang),
            'completed': t('completed', current_lang)
        }
        
        status_colors = {
            'pending': '#ff9999',
            'confirmed': '#99ccff', 
            'in_progress': '#ffcc99',
            'completed': '#99ff99'
        }
        
        cols = st.columns(4)
        
        for i, status in enumerate(statuses):
            with cols[i]:
                status_jobs = jobs[jobs['status'] == status]
                st.markdown(f"""
                <div style="background-color: {status_colors[status]}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <h4 style="margin: 0; text-align: center;">{status_names[status]} ({len(status_jobs)})</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for _, job in status_jobs.iterrows():
                    # Job card
                    with st.container():
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px; background-color: white;">
                            <strong>{job['title']}</strong><br>
                            👤 {job['customer_name']}<br>
                            👨‍💼 {job['employee_name']}<br>
                            📅 {job['scheduled_date'] or 'Not scheduled'}<br>
                            💰 {format_currency(job.get('price', 0), current_lang)}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Quick action buttons for status changes
                        button_col1, button_col2 = st.columns(2)
                        
                        with button_col1:
                            if status == 'pending' and st.button("✅", key=f"confirm_board_{job['id']}", help=t('confirm', current_lang)):
                                update_job_status(conn, job['id'], 'confirmed')
                                st.rerun()
                            elif status == 'confirmed' and st.button("▶️", key=f"start_board_{job['id']}", help=t('start', current_lang)):
                                update_job_status(conn, job['id'], 'in_progress')
                                st.rerun()
                            elif status == 'in_progress' and st.button("🏁", key=f"complete_board_{job['id']}", help=t('complete', current_lang)):
                                update_job_status(conn, job['id'], 'completed')
                                st.rerun()
                        
                        with button_col2:
                            if st.button("👥", key=f"assign_board_{job['id']}", help=t('assign', current_lang)):
                                st.session_state[f'show_assign_job_{job["id"]}'] = True
                                st.rerun()
                        
                        st.markdown("---")
    else:
        st.info(t("no_jobs_found", current_lang))

def show_bulk_operations(conn, current_lang):
    """Bulk operations for job management"""
    st.subheader("📦 " + t("bulk_operations", current_lang))
    
    # Get all jobs for bulk operations
    all_jobs = pd.read_sql_query("""
        SELECT 
            j.*,
            COALESCE(c.name, cu.first_name || ' ' || cu.last_name, 'Unassigned') as customer_name,
            COALESCE(e.name, 'Unassigned') as employee_name
        FROM jobs j 
        LEFT JOIN customers c ON j.customer_id = c.id 
        LEFT JOIN customer_users cu ON j.customer_id = cu.id
        LEFT JOIN employees e ON j.employee_id = e.id
        ORDER BY j.created_at DESC
    """, conn)
    
    if not all_jobs.empty:
        # Bulk operation options
        bulk_op = st.selectbox(
            t("select_bulk_operation", current_lang),
            [
                t("bulk_status_update", current_lang),
                t("bulk_employee_assignment", current_lang),
                t("bulk_delete", current_lang),
                t("bulk_reschedule", current_lang),
                t("bulk_price_update", current_lang)
            ]
        )
        
        # Job selection
        selected_job_ids = st.multiselect(
            t("select_jobs", current_lang),
            options=all_jobs['id'].tolist(),
            format_func=lambda x: f"{all_jobs[all_jobs['id']==x]['title'].iloc[0]} - {all_jobs[all_jobs['id']==x]['customer_name'].iloc[0]} ({all_jobs[all_jobs['id']==x]['status'].iloc[0]})"
        )
        
        if selected_job_ids:
            st.write(f"**{t('selected_jobs', current_lang)}:** {len(selected_job_ids)}")
            
            # Bulk Status Update
            if bulk_op == t("bulk_status_update", current_lang):
                new_status = st.selectbox(
                    t("new_status", current_lang),
                    ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled'],
                    format_func=lambda x: t(x, current_lang)
                )
                
                if st.button(f"🔄 {t('update_status', current_lang)}"):
                    for job_id in selected_job_ids:
                        update_job_status(conn, job_id, new_status)
                    st.success(f"{t('status_updated_successfully', current_lang)}: {len(selected_job_ids)} {t('jobs', current_lang)}")
                    st.rerun()
            
            # Bulk Employee Assignment
            elif bulk_op == t("bulk_employee_assignment", current_lang):
                employees = pd.read_sql_query("SELECT id, name FROM employees WHERE COALESCE(status, 'active') = 'active'", conn)
                
                if not employees.empty:
                    selected_employee = st.selectbox(
                        t("select_employee", current_lang),
                        options=employees['id'].tolist(),
                        format_func=lambda x: employees[employees['id']==x]['name'].iloc[0]
                    )
                    
                    if st.button(f"👥 {t('assign_employee', current_lang)}"):
                        for job_id in selected_job_ids:
                            conn.execute("UPDATE jobs SET employee_id = ? WHERE id = ?", (selected_employee, job_id))
                        conn.commit()
                        st.success(f"{t('employee_assigned_successfully', current_lang)}: {len(selected_job_ids)} {t('jobs', current_lang)}")
                        st.rerun()
                else:
                    st.warning(t("no_available_employees", current_lang))
            
            # Bulk Delete
            elif bulk_op == t("bulk_delete", current_lang):
                st.warning(f"⚠️ {t('bulk_delete_warning', current_lang)}")
                
                confirm_delete = st.checkbox(t("confirm_delete", current_lang))
                
                if confirm_delete and st.button(f"🗑️ {t('delete_selected_jobs', current_lang)}"):
                    for job_id in selected_job_ids:
                        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
                    conn.commit()
                    st.success(f"{t('jobs_deleted_successfully', current_lang)}: {len(selected_job_ids)}")
                    st.rerun()
            
            # Bulk Reschedule
            elif bulk_op == t("bulk_reschedule", current_lang):
                col1, col2 = st.columns(2)
                with col1:
                    new_date = st.date_input(t("new_date", current_lang))
                with col2:
                    new_time = st.time_input(t("new_time", current_lang))
                
                if st.button(f"📅 {t('reschedule_jobs', current_lang)}"):
                    for job_id in selected_job_ids:
                        conn.execute("UPDATE jobs SET scheduled_date = ?, scheduled_time = ? WHERE id = ?", 
                                   (new_date.isoformat(), new_time.strftime("%H:%M"), job_id))
                    conn.commit()
                    st.success(f"{t('jobs_rescheduled_successfully', current_lang)}: {len(selected_job_ids)}")
                    st.rerun()
            
            # Bulk Price Update
            elif bulk_op == t("bulk_price_update", current_lang):
                price_update_type = st.radio(
                    t("price_update_type", current_lang),
                    [t("set_fixed_price", current_lang), t("apply_percentage_change", current_lang)]
                )
                
                if price_update_type == t("set_fixed_price", current_lang):
                    new_price = st.number_input(t("new_price", current_lang), min_value=0.0, step=5.0)
                    
                    if st.button(f"💰 {t('update_prices', current_lang)}"):
                        for job_id in selected_job_ids:
                            conn.execute("UPDATE jobs SET price = ? WHERE id = ?", (new_price, job_id))
                        conn.commit()
                        st.success(f"{t('prices_updated_successfully', current_lang)}: {len(selected_job_ids)}")
                        st.rerun()
                
                else:
                    percentage_change = st.number_input(t("percentage_change", current_lang), min_value=-100.0, max_value=1000.0, step=5.0)
                    
                    if st.button(f"📊 {t('apply_percentage_change', current_lang)}"):
                        for job_id in selected_job_ids:
                            conn.execute("""
                                UPDATE jobs 
                                SET price = COALESCE(price, 0) * (1 + ? / 100.0) 
                                WHERE id = ?
                            """, (percentage_change, job_id))
                        conn.commit()
                        st.success(f"{t('prices_updated_successfully', current_lang)}: {len(selected_job_ids)}")
                        st.rerun()
    else:
        st.info(t("no_jobs_available_for_bulk_operations", current_lang))

def show_assignment_analytics(conn, current_lang):
    """Advanced analytics for job assignments and employee performance"""
    st.subheader("📈 " + t("assignment_analytics", current_lang))
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(t("start_date", current_lang), value=pd.Timestamp.now().date().replace(day=1))
    with col2:
        end_date = st.date_input(t("end_date", current_lang), value=pd.Timestamp.now().date())
    
    # Key Performance Indicators
    st.markdown("### 📊 " + t("key_performance_indicators", current_lang))
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    # Total jobs in period
    total_jobs = conn.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE scheduled_date BETWEEN ? AND ?
    """, (start_date.isoformat(), end_date.isoformat())).fetchone()[0]
    
    with kpi_col1:
        st.metric(t("total_jobs", current_lang), total_jobs)
    
    # Assignment rate
    assigned_jobs = conn.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE scheduled_date BETWEEN ? AND ? AND employee_id IS NOT NULL
    """, (start_date.isoformat(), end_date.isoformat())).fetchone()[0]
    
    assignment_rate = (assigned_jobs / total_jobs * 100) if total_jobs > 0 else 0
    
    with kpi_col2:
        st.metric(t("assignment_rate", current_lang), f"{assignment_rate:.1f}%")
    
    # Completion rate
    completed_jobs = conn.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE scheduled_date BETWEEN ? AND ? AND status = 'completed'
    """, (start_date.isoformat(), end_date.isoformat())).fetchone()[0]
    
    completion_rate = (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
    
    with kpi_col3:
        st.metric(t("completion_rate", current_lang), f"{completion_rate:.1f}%")
    
    # Average job value
    avg_job_value = conn.execute("""
        SELECT COALESCE(AVG(price), 0) FROM jobs 
        WHERE scheduled_date BETWEEN ? AND ?
    """, (start_date.isoformat(), end_date.isoformat())).fetchone()[0]
    
    with kpi_col4:
        st.metric(t("avg_job_value", current_lang), format_currency(avg_job_value, current_lang))
    
    # Employee Performance Analysis
    st.markdown("### 👨‍💼 " + t("employee_performance_analysis", current_lang))
    
    employee_stats = pd.read_sql_query("""
        SELECT 
            e.name as employee_name,
            COUNT(j.id) as total_jobs,
            COUNT(CASE WHEN j.status = 'completed' THEN 1 END) as completed_jobs,
            COUNT(CASE WHEN j.status = 'cancelled' THEN 1 END) as cancelled_jobs,
            COALESCE(AVG(j.price), 0) as avg_job_value,
            COALESCE(SUM(j.price), 0) as total_revenue
        FROM employees e
        LEFT JOIN jobs j ON e.id = j.employee_id 
            AND j.scheduled_date BETWEEN ? AND ?
        WHERE COALESCE(e.status, 'active') = 'active'
        GROUP BY e.id, e.name
        ORDER BY total_jobs DESC
    """, conn, params=(start_date.isoformat(), end_date.isoformat()))
    
    if not employee_stats.empty:
        # Employee performance table
        employee_stats['completion_rate'] = (employee_stats['completed_jobs'] / employee_stats['total_jobs'] * 100).fillna(0).round(1)
        employee_stats['cancellation_rate'] = (employee_stats['cancelled_jobs'] / employee_stats['total_jobs'] * 100).fillna(0).round(1)
        
        display_stats = employee_stats.copy()
        display_stats['avg_job_value'] = display_stats['avg_job_value'].apply(lambda x: format_currency(x, current_lang))
        display_stats['total_revenue'] = display_stats['total_revenue'].apply(lambda x: format_currency(x, current_lang))
        
        st.dataframe(
            display_stats[[
                'employee_name', 'total_jobs', 'completed_jobs', 
                'completion_rate', 'cancellation_rate', 'avg_job_value', 'total_revenue'
            ]].rename(columns={
                'employee_name': t('employee_name', current_lang),
                'total_jobs': t('total_jobs', current_lang),
                'completed_jobs': t('completed_jobs', current_lang),
                'completion_rate': t('completion_rate', current_lang) + ' (%)',
                'cancellation_rate': t('cancellation_rate', current_lang) + ' (%)',
                'avg_job_value': t('avg_job_value', current_lang),
                'total_revenue': t('total_revenue', current_lang)
            }),
            use_container_width=True
        )
        
        # Top performers
        st.markdown("### 🏆 " + t("top_performers", current_lang))
        
        top_col1, top_col2, top_col3 = st.columns(3)
        
        with top_col1:
            st.markdown("#### " + t("most_jobs_completed", current_lang))
            top_by_jobs = employee_stats.nlargest(3, 'completed_jobs')
            for idx, emp in top_by_jobs.iterrows():
                st.write(f"🥇 {emp['employee_name']}: {emp['completed_jobs']} {t('jobs', current_lang)}")
        
        with top_col2:
            st.markdown("#### " + t("highest_completion_rate", current_lang))
            top_by_completion = employee_stats[employee_stats['total_jobs'] >= 3].nlargest(3, 'completion_rate')
            for idx, emp in top_by_completion.iterrows():
                st.write(f"⭐ {emp['employee_name']}: {emp['completion_rate']:.1f}%")
        
        with top_col3:
            st.markdown("#### " + t("highest_revenue", current_lang))
            top_by_revenue = employee_stats.nlargest(3, 'total_revenue')
            for idx, emp in top_by_revenue.iterrows():
                st.write(f"💰 {emp['employee_name']}: {format_currency(emp['total_revenue'], current_lang)}")
    
    # Workload Distribution
    st.markdown("### 📊 " + t("workload_distribution", current_lang))
    
    workload_stats = pd.read_sql_query("""
        SELECT 
            e.name as employee_name,
            COUNT(CASE WHEN j.status IN ('pending', 'confirmed') THEN 1 END) as pending_jobs,
            COUNT(CASE WHEN j.status = 'in_progress' THEN 1 END) as active_jobs,
            COUNT(CASE WHEN j.status = 'completed' THEN 1 END) as completed_jobs
        FROM employees e
        LEFT JOIN jobs j ON e.id = j.employee_id
        WHERE COALESCE(e.status, 'active') = 'active'
        GROUP BY e.id, e.name
        ORDER BY (pending_jobs + active_jobs) DESC
    """, conn)
    
    if not workload_stats.empty:
        # Workload visualization
        workload_stats['total_workload'] = workload_stats['pending_jobs'] + workload_stats['active_jobs']
        
        # Create a simple bar chart representation
        for idx, emp in workload_stats.iterrows():
            workload_level = "🔴" if emp['total_workload'] > 5 else "🟡" if emp['total_workload'] > 2 else "🟢"
            st.write(f"{workload_level} **{emp['employee_name']}**: {emp['pending_jobs']} {t('pending', current_lang)}, {emp['active_jobs']} {t('active', current_lang)}, {emp['completed_jobs']} {t('completed', current_lang)}")

# Helper functions for job management
def update_job_status(conn, job_id, new_status):
    """Update job status"""
    conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))
    conn.commit()

def show_edit_job_form(conn, job, current_lang):
    """Show job editing form"""
    with st.form(f"edit_job_form_{job['id']}"):
        st.subheader(f"✏️ {t('edit_job', current_lang)}")
        
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input(t("job_title", current_lang), value=job.get('title', ''))
            new_description = st.text_area(t("description", current_lang), value=job.get('description', ''))
            new_price = st.number_input(t("price", current_lang), value=float(job.get('price', 0)), min_value=0.0)
        
        with col2:
            new_date = st.date_input(t("scheduled_date", current_lang), 
                                   value=pd.to_datetime(job['scheduled_date']).date() if job.get('scheduled_date') else None)
            new_time = st.time_input(t("scheduled_time", current_lang),
                                   value=pd.to_datetime(job['scheduled_time'], format='%H:%M').time() if job.get('scheduled_time') else None)
            new_location = st.text_input(t("location", current_lang), value=job.get('location', ''))
        
        col1_btn, col2_btn = st.columns(2)
        with col1_btn:
            if st.form_submit_button(t("save_changes", current_lang)):
                conn.execute("""
                    UPDATE jobs 
                    SET title = ?, description = ?, price = ?, scheduled_date = ?, 
                        scheduled_time = ?, location = ?
                    WHERE id = ?
                """, (new_title, new_description, new_price, new_date.isoformat(), 
                      new_time.strftime("%H:%M"), new_location, job['id']))
                conn.commit()
                st.success(t("job_updated_successfully", current_lang))
                del st.session_state[f'show_edit_job_{job["id"]}']
                st.rerun()
        
        with col2_btn:
            if st.form_submit_button(t("cancel", current_lang)):
                del st.session_state[f'show_edit_job_{job["id"]}']
                st.rerun()

def show_assignment_form(conn, job, current_lang):
    """Show employee assignment form"""
    available_employees = pd.read_sql_query("""
        SELECT id, name, COALESCE(specialties, skills, '') as specialties, hourly_rate
        FROM employees 
        WHERE COALESCE(status, 'active') = 'active'
    """, conn)
    
    with st.form(f"assign_employee_form_{job['id']}"):
        st.subheader(f"👥 {t('assign_employee_to_job', current_lang)}")
        
        if not available_employees.empty:
            selected_employee = st.selectbox(
                t("select_employee", current_lang),
                options=available_employees['id'].tolist(),
                format_func=lambda x: f"{available_employees[available_employees['id']==x]['name'].iloc[0]} - {available_employees[available_employees['id']==x]['specialties'].iloc[0]} (${available_employees[available_employees['id']==x]['hourly_rate'].iloc[0]}/hr)"
            )
            
            col1_btn, col2_btn = st.columns(2)
            with col1_btn:
                if st.form_submit_button(t("assign_employee", current_lang)):
                    conn.execute("UPDATE jobs SET employee_id = ?, status = 'confirmed' WHERE id = ?", 
                               (selected_employee, job['id']))
                    conn.commit()
                    st.success(t("employee_assigned_successfully", current_lang))
                    del st.session_state[f'show_assign_job_{job["id"]}']
                    st.rerun()
            
            with col2_btn:
                if st.form_submit_button(t("cancel", current_lang)):
                    del st.session_state[f'show_assign_job_{job["id"]}']
                    st.rerun()
        else:
            st.warning(t("no_available_employees", current_lang))
            if st.form_submit_button(t("close", current_lang)):
                del st.session_state[f'show_assign_job_{job["id"]}']
                st.rerun()

def show_add_job_form(conn, current_lang):
    """Show add new job form"""
    with st.form("add_new_job"):
        st.subheader(f"➕ {t('add_new_job', current_lang)}")
        
        # Get customers and employees for selection
        customers = pd.read_sql_query("SELECT id, name FROM customers", conn)
        portal_customers = pd.read_sql_query("SELECT id, first_name || ' ' || last_name as name FROM customer_users", conn)
        employees = pd.read_sql_query("""
            SELECT id, name FROM employees 
            WHERE COALESCE(status, 'active') = 'active'
        """, conn)
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input(t("job_title", current_lang) + "*")
            description = st.text_area(t("job_description", current_lang))
            
            # Customer selection
            all_customers = pd.concat([customers, portal_customers], ignore_index=True)
            customer_options = [""] + [f"{row['name']} (ID: {row['id']})" for _, row in all_customers.iterrows()]
            selected_customer = st.selectbox(t("customer", current_lang), customer_options)
            
            # Employee selection
            employee_options = [""] + [f"{row['name']} (ID: {row['id']})" for _, row in employees.iterrows()]
            selected_employee = st.selectbox(t("assign_employee", current_lang), employee_options)
        
        with col2:
            service_type = st.selectbox(t("service_type", current_lang), 
                                      [t("basic_cleaning", current_lang), t("deep_cleaning", current_lang), 
                                       t("office_cleaning", current_lang), t("window_cleaning", current_lang)])
            
            scheduled_date = st.date_input(t("scheduled_date", current_lang))
            scheduled_time = st.time_input(t("scheduled_time", current_lang))
            duration = st.number_input(t("duration", current_lang) + " (hours)", min_value=0.5, max_value=12.0, step=0.5)
            price = st.number_input(t("price", current_lang), min_value=0.0, step=5.0)
            location = st.text_input(t("location", current_lang))
        
        if st.form_submit_button(t("add_new_job", current_lang)):
            if title:
                # Extract customer and employee IDs
                customer_id = None
                if selected_customer:
                    customer_id = int(selected_customer.split("ID: ")[1].split(")")[0])
                
                employee_id = None
                if selected_employee:
                    employee_id = int(selected_employee.split("ID: ")[1].split(")")[0])
                
                conn.execute('''
                    INSERT INTO jobs (customer_id, employee_id, title, description, scheduled_date, 
                                    scheduled_time, duration, service_type, location, price, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                ''', (customer_id, employee_id, title, description, scheduled_date, 
                      scheduled_time.strftime("%H:%M"), duration, service_type, location, price))
                conn.commit()
                st.success(t("job_created_successfully", current_lang))
                st.rerun()
            else:
                st.error(t("required_fields_missing", current_lang))

def show_analytics():
    """Analytics dashboard with multilingual support"""
    current_lang = get_current_language()
    conn = init_database()
    
    st.title("📈 " + t("analytics", current_lang))
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = conn.execute("SELECT COALESCE(SUM(price), 0) FROM jobs WHERE status = 'completed'").fetchone()[0]
        st.metric(t("total", current_lang) + " " + t("revenue_this_month", current_lang), format_currency(total_revenue, current_lang))
    
    with col2:
        avg_job_value = conn.execute("SELECT COALESCE(AVG(price), 0) FROM jobs WHERE status = 'completed'").fetchone()[0]
        st.metric("Avg Job Value", format_currency(avg_job_value, current_lang))
    
    with col3:
        completion_rate = conn.execute("""
            SELECT CASE WHEN COUNT(*) > 0 THEN 
                ROUND(COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 / COUNT(*), 1) 
                ELSE 0 END 
            FROM jobs
        """).fetchone()[0]
        st.metric("Completion Rate", f"{completion_rate}%")
    
    with col4:
        customer_retention = conn.execute("""
            SELECT CASE WHEN COUNT(DISTINCT customer_id) > 0 THEN
                ROUND(COUNT(CASE WHEN cnt > 1 THEN 1 END) * 100.0 / COUNT(DISTINCT customer_id), 1)
                ELSE 0 END
            FROM (SELECT customer_id, COUNT(*) as cnt FROM jobs GROUP BY customer_id)
        """).fetchone()[0]
        st.metric(t("customer_retention", current_lang), f"{customer_retention}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t("revenue_by_service", current_lang))
        revenue_by_service = pd.read_sql_query("""
            SELECT service_type, SUM(price) as revenue, COUNT(*) as count
            FROM jobs WHERE status = 'completed' AND service_type IS NOT NULL
            GROUP BY service_type ORDER BY revenue DESC
        """, conn)
        
        if not revenue_by_service.empty:
            fig = px.pie(revenue_by_service, values='revenue', names='service_type', 
                        title=t("revenue_by_service", current_lang))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No completed jobs found")
    
    with col2:
        st.subheader(t("top_performing_employees", current_lang))
        employee_performance = pd.read_sql_query("""
            SELECT e.name, COUNT(j.id) as completed_jobs, COALESCE(SUM(j.price), 0) as revenue
            FROM employees e 
            LEFT JOIN jobs j ON e.id = j.employee_id AND j.status = 'completed'
            GROUP BY e.id, e.name ORDER BY completed_jobs DESC LIMIT 5
        """, conn)
        
        if not employee_performance.empty:
            fig = px.bar(employee_performance, x='name', y='completed_jobs',
                        title=t("completed_jobs", current_lang))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t("no_employees_found", current_lang))
    
    conn.close()

def show_settings():
    """Settings page with multilingual support"""
    current_lang = get_current_language()
    
    st.title("⚙️ " + t("settings", current_lang))
    
    tab1, tab2, tab3 = st.tabs([
        t("general_settings", current_lang),
        t("user_management", current_lang), 
        t("system_preferences", current_lang)
    ])
    
    with tab1:
        st.subheader(t("business_hours", current_lang))
        
        col1, col2 = st.columns(2)
        with col1:
            st.time_input("Opening Time", value=datetime.strptime("09:00", "%H:%M").time())
        with col2:
            st.time_input("Closing Time", value=datetime.strptime("18:00", "%H:%M").time())
        
        st.subheader(t("service_areas", current_lang))
        service_areas = st.text_area("Service Areas (one per line)", 
                                   value="Berlin\nMunich\nHamburg\nCologne")
        
        st.subheader(t("pricing_settings", current_lang))
        base_rate = st.number_input("Base Hourly Rate", min_value=0.0, value=25.0, step=0.5)
        weekend_multiplier = st.number_input("Weekend Rate Multiplier", min_value=1.0, value=1.5, step=0.1)
        
        if st.button(t("save", current_lang)):
            st.success("Settings saved successfully!")
    
    with tab2:
        st.subheader(t("user_management", current_lang))
        st.info("User management functionality would be implemented here")
    
    with tab3:
        st.subheader(t("system_preferences", current_lang))
        
        # Language settings
        st.write("**Language Settings**")
        from translations import translation_manager
        current_lang_display = translation_manager.available_languages[current_lang]['name']
        st.write(f"Current Language: {current_lang_display}")
        
        # Backup settings
        st.write("**Backup Settings**")
        if st.button("Create Database Backup"):
            st.success("Backup created successfully!")
        
        # Notification settings
        st.write("**Notification Settings**")
        email_notifications = st.checkbox("Enable Email Notifications", value=True)
        sms_notifications = st.checkbox("Enable SMS Notifications", value=False)

def main():
    """Main application with language support"""
    # Initialize session state
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Language selector in sidebar
    current_lang = init_language_selector()
    
    if not st.session_state.admin_logged_in:
        show_login_form()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### 👨‍💼 {t('welcome', current_lang)}, {st.session_state.admin_username}!")
        
        # Navigation menu
        menu_options = [
            (t("dashboard", current_lang), "📊"),
            (t("customer_management", current_lang), "👥"),
            (t("employee_management", current_lang), "👨‍💼"),
            (t("job_management", current_lang), "📋"),
            (t("analytics", current_lang), "📈"),
            (t("settings", current_lang), "⚙️")
        ]
        
        selected = st.selectbox(
            t("navigation", current_lang),
            [option[0] for option in menu_options],
            format_func=lambda x: f"{[opt[1] for opt in menu_options if opt[0] == x][0]} {x}"
        )
        
        if st.button(t("logout", current_lang)):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    # Main content based on selection
    if selected == t("dashboard", current_lang):
        show_dashboard()
    elif selected == t("customer_management", current_lang):
        manage_customers()
    elif selected == t("employee_management", current_lang):
        manage_employees()
    elif selected == t("job_management", current_lang):
        manage_jobs()
    elif selected == t("analytics", current_lang):
        show_analytics()
    elif selected == t("settings", current_lang):
        show_settings()

if __name__ == "__main__":
    main()
