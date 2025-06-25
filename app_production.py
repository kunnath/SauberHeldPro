"""
Aufraumenbee - Professional Cleaning Service Management System
Admin Portal - Production Version

This is the main administrative interface for managing the cleaning service business.
Features include customer management, employee management, job scheduling, invoicing,
inventory tracking, and business analytics.

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
    page_title="Aufraumenbee Admin Portal",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database configuration
DATABASE_PATH = "aufraumenbee.db"

def init_database():
    """Initialize the SQLite database with all required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table (admin, manager, employee access)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'manager', 'employee')),
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Customers table (unified customer data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            registration_source TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Customer users table (for customer portal login)
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
    
    # Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            position TEXT,
            hourly_rate REAL,
            hire_date DATE,
            status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            service_type TEXT NOT NULL,
            scheduled_date DATE NOT NULL,
            scheduled_time TEXT NOT NULL,
            duration_hours INTEGER DEFAULT 2,
            hourly_rate REAL DEFAULT 25.0,
            total_amount REAL,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled')),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    
    # Invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            job_id INTEGER,
            invoice_number TEXT UNIQUE,
            amount REAL NOT NULL,
            tax_amount REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'overdue', 'cancelled')),
            issued_date DATE DEFAULT CURRENT_DATE,
            due_date DATE,
            paid_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')
    
    # Inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            unit_price REAL,
            supplier TEXT,
            last_restocked DATE,
            minimum_stock INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    if cursor.fetchone()[0] == 0:
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        ''', ("admin", admin_password, "admin", "admin@aufraumenbee.com"))
    
    conn.commit()
    conn.close()

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate admin users"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password_hash, role, email FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        return {
            'id': user[0],
            'username': user[1],
            'role': user[3],
            'email': user[4]
        }
    return None

def get_dashboard_metrics() -> Dict:
    """Get key business metrics for the dashboard"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total customers (from both tables)
    cursor.execute("SELECT COUNT(*) FROM customers")
    admin_customers = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customer_users")
    portal_customers = cursor.fetchone()[0]
    total_customers = admin_customers + portal_customers
    
    # Total employees
    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'active'")
    total_employees = cursor.fetchone()[0]
    
    # Pending jobs
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'pending'")
    pending_jobs = cursor.fetchone()[0]
    
    # Monthly revenue
    cursor.execute('''
        SELECT COALESCE(SUM(total_amount), 0) 
        FROM invoices 
        WHERE status = 'paid' 
        AND strftime('%Y-%m', paid_date) = strftime('%Y-%m', 'now')
    ''')
    monthly_revenue = cursor.fetchone()[0]
    
    # Recent jobs
    cursor.execute('''
        SELECT j.id, c.first_name || ' ' || c.last_name as customer_name, 
               j.service_type, j.scheduled_date, j.status
        FROM jobs j
        LEFT JOIN customers c ON j.customer_id = c.id
        ORDER BY j.created_at DESC
        LIMIT 5
    ''')
    recent_jobs = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_customers': total_customers,
        'total_employees': total_employees,
        'pending_jobs': pending_jobs,
        'monthly_revenue': monthly_revenue,
        'recent_jobs': recent_jobs
    }

def show_dashboard():
    """Display the main dashboard with key metrics and overview"""
    st.header("📊 Dashboard Overview")
    
    metrics = get_dashboard_metrics()
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Customers",
            value=metrics['total_customers'],
            delta="+5 this month"
        )
    
    with col2:
        st.metric(
            label="👷 Active Employees",
            value=metrics['total_employees'],
            delta="+2 this month"
        )
    
    with col3:
        st.metric(
            label="📋 Pending Jobs",
            value=metrics['pending_jobs'],
            delta="-3 from yesterday"
        )
    
    with col4:
        st.metric(
            label="💰 Monthly Revenue",
            value=f"€{metrics['monthly_revenue']:.2f}",
            delta="+12.5% from last month"
        )
    
    # Recent activity
    st.subheader("🕒 Recent Jobs")
    if metrics['recent_jobs']:
        df = pd.DataFrame(metrics['recent_jobs'], 
                         columns=['Job ID', 'Customer', 'Service', 'Scheduled Date', 'Status'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No recent jobs to display")

def show_customer_management():
    """Customer management interface"""
    st.header("👥 Customer Management")
    
    tab1, tab2 = st.tabs(["📋 Customer List", "➕ Add New Customer"])
    
    with tab1:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Get customers from both tables
        query = '''
            SELECT id, first_name, last_name, email, phone, address, 'Admin' as source, created_at
            FROM customers
            UNION ALL
            SELECT id, first_name, last_name, email, phone, address, 'Portal' as source, created_at
            FROM customer_users
            ORDER BY created_at DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            # Search functionality
            search_term = st.text_input("🔍 Search customers by name or email:")
            if search_term:
                df = df[
                    df['first_name'].str.contains(search_term, case=False, na=False) |
                    df['last_name'].str.contains(search_term, case=False, na=False) |
                    df['email'].str.contains(search_term, case=False, na=False)
                ]
            
            st.dataframe(
                df[['first_name', 'last_name', 'email', 'phone', 'source', 'created_at']],
                column_config={
                    'first_name': 'First Name',
                    'last_name': 'Last Name',
                    'email': 'Email',
                    'phone': 'Phone',
                    'source': 'Registration Source',
                    'created_at': 'Registration Date'
                },
                use_container_width=True
            )
        else:
            st.info("No customers found")
    
    with tab2:
        with st.form("add_customer"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name*")
                email = st.text_input("Email*")
                address = st.text_area("Address")
            
            with col2:
                last_name = st.text_input("Last Name*")
                phone = st.text_input("Phone")
                notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Customer", type="primary"):
                if first_name and last_name and email:
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    
                    try:
                        cursor.execute('''
                            INSERT INTO customers (first_name, last_name, email, phone, address, notes, registration_source)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (first_name, last_name, email, phone, address, notes, 'admin'))
                        
                        conn.commit()
                        st.success(f"✅ Customer {first_name} {last_name} added successfully!")
                        st.rerun()
                        
                    except sqlite3.IntegrityError:
                        st.error("❌ Email already exists!")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Please fill in all required fields!")

def show_job_management():
    """Job management interface"""
    st.header("📋 Job Management")
    
    tab1, tab2 = st.tabs(["📋 All Jobs", "➕ Create New Job"])
    
    with tab1:
        conn = sqlite3.connect(DATABASE_PATH)
        
        query = '''
            SELECT j.id, c.first_name || ' ' || c.last_name as customer_name,
                   e.first_name || ' ' || e.last_name as employee_name,
                   j.service_type, j.scheduled_date, j.scheduled_time,
                   j.total_amount, j.status, j.created_at
            FROM jobs j
            LEFT JOIN customers c ON j.customer_id = c.id
            LEFT JOIN employees e ON j.employee_id = e.id
            ORDER BY j.scheduled_date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            # Filter by status
            status_filter = st.selectbox("Filter by Status", 
                                       ["All", "pending", "confirmed", "in_progress", "completed", "cancelled"])
            
            if status_filter != "All":
                df = df[df['status'] == status_filter]
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No jobs found")
    
    with tab2:
        # Get customers and employees for dropdowns
        conn = sqlite3.connect(DATABASE_PATH)
        
        customers_df = pd.read_sql_query("SELECT id, first_name || ' ' || last_name as name FROM customers", conn)
        employees_df = pd.read_sql_query("SELECT id, first_name || ' ' || last_name as name FROM employees WHERE status = 'active'", conn)
        
        with st.form("create_job"):
            col1, col2 = st.columns(2)
            
            with col1:
                if not customers_df.empty:
                    customer_options = dict(zip(customers_df['name'], customers_df['id']))
                    selected_customer = st.selectbox("Customer*", options=list(customer_options.keys()))
                    customer_id = customer_options[selected_customer] if selected_customer else None
                else:
                    st.warning("No customers available. Please add customers first.")
                    customer_id = None
                
                service_type = st.selectbox("Service Type*", 
                                          ["Regular Cleaning", "Deep Cleaning", "Move-in/out Cleaning", 
                                           "Office Cleaning", "Post-construction Cleanup"])
                
                scheduled_date = st.date_input("Scheduled Date*", min_value=date.today())
            
            with col2:
                if not employees_df.empty:
                    employee_options = dict(zip(employees_df['name'], employees_df['id']))
                    selected_employee = st.selectbox("Assign Employee", options=["None"] + list(employee_options.keys()))
                    employee_id = employee_options[selected_employee] if selected_employee != "None" else None
                else:
                    st.warning("No employees available.")
                    employee_id = None
                
                scheduled_time = st.time_input("Scheduled Time*")
                duration_hours = st.number_input("Duration (hours)", min_value=1, max_value=8, value=2)
                hourly_rate = st.number_input("Hourly Rate (€)", min_value=15.0, max_value=100.0, value=25.0)
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Create Job", type="primary"):
                if customer_id and service_type and scheduled_date:
                    total_amount = duration_hours * hourly_rate
                    
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO jobs (customer_id, employee_id, service_type, scheduled_date, 
                                        scheduled_time, duration_hours, hourly_rate, total_amount, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (customer_id, employee_id, service_type, scheduled_date, 
                         str(scheduled_time), duration_hours, hourly_rate, total_amount, notes))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("✅ Job created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields!")
        
        conn.close()

def show_employee_management():
    """Employee management interface"""
    st.header("👷 Employee Management")
    
    tab1, tab2 = st.tabs(["📋 Employee List", "➕ Add New Employee"])
    
    with tab1:
        conn = sqlite3.connect(DATABASE_PATH)
        df = pd.read_sql_query("SELECT * FROM employees ORDER BY created_at DESC", conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found")
    
    with tab2:
        with st.form("add_employee"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name*")
                email = st.text_input("Email")
                position = st.text_input("Position")
                hire_date = st.date_input("Hire Date", value=date.today())
            
            with col2:
                last_name = st.text_input("Last Name*")
                phone = st.text_input("Phone")
                hourly_rate = st.number_input("Hourly Rate (€)", min_value=15.0, max_value=100.0, value=20.0)
                status = st.selectbox("Status", ["active", "inactive"])
            
            if st.form_submit_button("Add Employee", type="primary"):
                if first_name and last_name:
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO employees (first_name, last_name, email, phone, position, 
                                             hourly_rate, hire_date, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (first_name, last_name, email, phone, position, hourly_rate, hire_date, status))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Employee {first_name} {last_name} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in required fields!")

def show_invoicing():
    """Invoicing and billing interface"""
    st.header("💰 Invoicing & Billing")
    
    tab1, tab2 = st.tabs(["📋 Invoice List", "➕ Create Invoice"])
    
    with tab1:
        conn = sqlite3.connect(DATABASE_PATH)
        
        query = '''
            SELECT i.id, i.invoice_number, c.first_name || ' ' || c.last_name as customer_name,
                   i.amount, i.tax_amount, i.total_amount, i.status, i.issued_date, i.due_date
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            ORDER BY i.created_at DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Payment tracking
            col1, col2, col3 = st.columns(3)
            with col1:
                total_pending = df[df['status'] == 'pending']['total_amount'].sum()
                st.metric("Pending Payments", f"€{total_pending:.2f}")
            with col2:
                total_paid = df[df['status'] == 'paid']['total_amount'].sum()
                st.metric("Paid This Month", f"€{total_paid:.2f}")
            with col3:
                overdue = len(df[df['status'] == 'overdue'])
                st.metric("Overdue Invoices", overdue)
        else:
            st.info("No invoices found")
    
    with tab2:
        # Create new invoice form
        conn = sqlite3.connect(DATABASE_PATH)
        customers_df = pd.read_sql_query("SELECT id, first_name || ' ' || last_name as name FROM customers", conn)
        
        if not customers_df.empty:
            with st.form("create_invoice"):
                customer_options = dict(zip(customers_df['name'], customers_df['id']))
                selected_customer = st.selectbox("Customer*", options=list(customer_options.keys()))
                customer_id = customer_options[selected_customer]
                
                col1, col2 = st.columns(2)
                with col1:
                    amount = st.number_input("Amount (€)*", min_value=0.01, value=50.0)
                    tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=30.0, value=19.0)
                    due_date = st.date_input("Due Date", value=date.today() + timedelta(days=30))
                
                with col2:
                    tax_amount = amount * (tax_rate / 100)
                    total_amount = amount + tax_amount
                    st.info(f"Tax Amount: €{tax_amount:.2f}")
                    st.info(f"Total Amount: €{total_amount:.2f}")
                
                if st.form_submit_button("Create Invoice", type="primary"):
                    cursor = conn.cursor()
                    
                    # Generate invoice number
                    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{customer_id:03d}"
                    
                    cursor.execute('''
                        INSERT INTO invoices (customer_id, invoice_number, amount, tax_amount, 
                                            total_amount, due_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (customer_id, invoice_number, amount, tax_amount, total_amount, due_date))
                    
                    conn.commit()
                    st.success(f"✅ Invoice {invoice_number} created successfully!")
                    st.rerun()
        else:
            st.warning("No customers available. Please add customers first.")
        
        conn.close()

def show_inventory():
    """Inventory management interface"""
    st.header("📦 Inventory Management")
    
    tab1, tab2 = st.tabs(["📋 Inventory List", "➕ Add Item"])
    
    with tab1:
        conn = sqlite3.connect(DATABASE_PATH)
        df = pd.read_sql_query("SELECT * FROM inventory ORDER BY item_name", conn)
        conn.close()
        
        if not df.empty:
            # Low stock alerts
            low_stock = df[df['quantity'] <= df['minimum_stock']]
            if not low_stock.empty:
                st.warning(f"⚠️ {len(low_stock)} items are low on stock!")
                with st.expander("View Low Stock Items"):
                    st.dataframe(low_stock[['item_name', 'quantity', 'minimum_stock']])
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No inventory items found")
    
    with tab2:
        with st.form("add_inventory"):
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("Item Name*")
                category = st.selectbox("Category", 
                                      ["Cleaning Supplies", "Equipment", "Safety Gear", "Office Supplies"])
                quantity = st.number_input("Initial Quantity", min_value=0, value=0)
            
            with col2:
                unit_price = st.number_input("Unit Price (€)", min_value=0.01, value=1.0)
                supplier = st.text_input("Supplier")
                minimum_stock = st.number_input("Minimum Stock Level", min_value=0, value=10)
            
            if st.form_submit_button("Add Item", type="primary"):
                if item_name:
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO inventory (item_name, category, quantity, unit_price, 
                                             supplier, minimum_stock, last_restocked)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (item_name, category, quantity, unit_price, supplier, minimum_stock, date.today()))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Item {item_name} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please enter an item name!")

def show_reports():
    """Reports and analytics interface"""
    st.header("📈 Reports & Analytics")
    
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Revenue analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Revenue Overview")
        
        # Monthly revenue
        monthly_revenue = pd.read_sql_query('''
            SELECT strftime('%Y-%m', paid_date) as month, SUM(total_amount) as revenue
            FROM invoices 
            WHERE status = 'paid' AND paid_date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', paid_date)
            ORDER BY month
        ''', conn)
        
        if not monthly_revenue.empty:
            st.line_chart(monthly_revenue.set_index('month'))
        else:
            st.info("No revenue data available")
    
    with col2:
        st.subheader("📊 Service Analytics")
        
        # Service type popularity
        service_stats = pd.read_sql_query('''
            SELECT service_type, COUNT(*) as count
            FROM jobs
            GROUP BY service_type
            ORDER BY count DESC
        ''', conn)
        
        if not service_stats.empty:
            st.bar_chart(service_stats.set_index('service_type'))
        else:
            st.info("No service data available")
    
    # Recent performance metrics
    st.subheader("📋 Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed_jobs = pd.read_sql_query("SELECT COUNT(*) as count FROM jobs WHERE status = 'completed'", conn)
        st.metric("Completed Jobs", completed_jobs.iloc[0]['count'])
    
    with col2:
        avg_rating = 4.8  # Placeholder - could be calculated from customer feedback
        st.metric("Average Rating", f"{avg_rating}⭐")
    
    with col3:
        active_customers = pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn)
        st.metric("Active Customers", active_customers.iloc[0]['count'])
    
    with col4:
        monthly_growth = 12.5  # Placeholder calculation
        st.metric("Monthly Growth", f"+{monthly_growth}%")
    
    conn.close()

def main():
    """Main application function"""
    
    # Initialize database
    init_database()
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #FF6B6B;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border: 2px solid #f0f0f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sidebar-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            color: white;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Login page
        st.markdown('<div class="main-header">🧹 Aufraumenbee Admin Portal</div>', unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("### 🔐 Admin Login")
                
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                    if st.form_submit_button("Login", type="primary", use_container_width=True):
                        user = authenticate_user(username, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.success(f"Welcome back, {user['username']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials!")
                
                # Demo credentials info
                with st.expander("ℹ️ Demo Credentials"):
                    st.info("""
                    **Default Admin Account:**
                    - Username: `admin`
                    - Password: `admin123`
                    """)
    
    else:
        # Main application interface
        user = st.session_state.user
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-header">
                <h2>🧹 Aufraumenbee</h2>
                <p>Welcome, {user['username']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation menu
            page = st.selectbox(
                "Navigation",
                ["📊 Dashboard", "👥 Customer Management", "📋 Job Management", 
                 "👷 Employee Management", "💰 Invoicing", "📦 Inventory", "📈 Reports"],
                label_visibility="collapsed"
            )
            
            # User info and logout
            st.markdown("---")
            st.markdown(f"**Role:** {user['role'].title()}")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
        
        # Main content area
        if page == "📊 Dashboard":
            show_dashboard()
        elif page == "👥 Customer Management":
            show_customer_management()
        elif page == "📋 Job Management":
            show_job_management()
        elif page == "👷 Employee Management":
            show_employee_management()
        elif page == "💰 Invoicing":
            show_invoicing()
        elif page == "📦 Inventory":
            show_inventory()
        elif page == "📈 Reports":
            show_reports()

if __name__ == "__main__":
    main()
