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
                        st.write(f"**{t('phone', current_lang)}:** {customer['phone'] if customer['phone'] else t('not_provided', current_lang) if 'not_provided' in st.session_state.get('translations', {}) else 'Not provided'}")
                        st.write(f"**{t('address', current_lang)}:** {customer['address'] if customer['address'] else t('not_provided', current_lang) if 'not_provided' in st.session_state.get('translations', {}) else 'Not provided'}")
                        st.write(f"**{t('total_jobs', current_lang)}:** {customer['total_jobs']}")
                    with col2:
                        st.write(f"**{t('customer_rating', current_lang)}:** ⭐ {customer['rating']:.1f}")
                        st.write(f"**{t('joined_date', current_lang)}:** {format_date(datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S').date(), current_lang)}")
                        st.write(f"**{t('source', current_lang) if 'source' in st.session_state.get('translations', {}) else 'Source'}:** {customer['source']}")
        else:
            st.info(t("no_customers_found", current_lang))
    
    with tab2:
        st.subheader(t("add_new_customer", current_lang))
        
        with st.form("add_customer"):
            name = st.text_input(t("customer_name", current_lang) if "customer_name" in st.session_state.get('translations', {}) else "Customer Name" + "*")
            email = st.text_input(t("email", current_lang))
            phone = st.text_input(t("phone", current_lang))
            address = st.text_area(t("address", current_lang))
            preferences = st.text_area(t("service_preferences", current_lang) if "service_preferences" in st.session_state.get('translations', {}) else "Service Preferences")
            
            if st.form_submit_button(t("add_customer", current_lang) if "add_customer" in st.session_state.get('translations', {}) else "Add Customer"):
                if name:
                    conn.execute('''
                        INSERT INTO customers (name, email, phone, address, preferences)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, email, phone, address, preferences))
                    conn.commit()
                    st.success(t("customer_added_successfully", current_lang) if "customer_added_successfully" in st.session_state.get('translations', {}) else "Customer added successfully!")
                    st.rerun()
                else:
                    st.error(t("required_fields_missing", current_lang))
    
    conn.close()

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
            t("navigation", current_lang) if "navigation" in st.session_state.get('translations', {}) else "Navigation",
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
        st.title("👨‍💼 " + t("employee_management", current_lang))
        st.info(t("feature_coming_soon", current_lang) if "feature_coming_soon" in st.session_state.get('translations', {}) else "Feature coming soon!")
    elif selected == t("job_management", current_lang):
        st.title("📋 " + t("job_management", current_lang))
        st.info(t("feature_coming_soon", current_lang) if "feature_coming_soon" in st.session_state.get('translations', {}) else "Feature coming soon!")
    elif selected == t("analytics", current_lang):
        st.title("📈 " + t("analytics", current_lang))
        st.info(t("feature_coming_soon", current_lang) if "feature_coming_soon" in st.session_state.get('translations', {}) else "Feature coming soon!")
    elif selected == t("settings", current_lang):
        st.title("⚙️ " + t("settings", current_lang))
        st.info(t("feature_coming_soon", current_lang) if "feature_coming_soon" in st.session_state.get('translations', {}) else "Feature coming soon!")

if __name__ == "__main__":
    main()
