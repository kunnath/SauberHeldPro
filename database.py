"""
Database utilities for Aufraumenbee cleaning service management system
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "aufraumenbee.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def init_database(self):
        """Initialize database with all tables"""
        conn = self.get_connection()
        
        # Users table
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
        
        # Customers table
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
        
        # Employees table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                skills TEXT,
                hourly_rate REAL,
                employment_type TEXT,
                availability TEXT,
                background_check BOOLEAN DEFAULT FALSE,
                rating REAL DEFAULT 0,
                total_jobs INTEGER DEFAULT 0,
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
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Invoices table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                customer_id INTEGER,
                amount REAL,
                tax_amount REAL,
                discount REAL DEFAULT 0,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                due_date DATE,
                paid_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Inventory table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER,
                unit_price REAL,
                minimum_stock INTEGER DEFAULT 10,
                supplier TEXT,
                last_restocked DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job feedback table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS job_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                customer_id INTEGER,
                rating INTEGER,
                comments TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs (id),
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_sample_data(self):
        """Add sample data for testing"""
        conn = self.get_connection()
        
        # Sample customers
        customers = [
            ("John Smith", "john@email.com", "555-0101", "123 Main St", "Prefers eco-friendly products"),
            ("Sarah Johnson", "sarah@email.com", "555-0102", "456 Oak Ave", "Has cats, needs pet-safe products"),
            ("Michael Brown", "michael@email.com", "555-0103", "789 Pine Rd", "Weekly deep cleaning"),
        ]
        
        for customer in customers:
            conn.execute('''
                INSERT OR IGNORE INTO customers (name, email, phone, address, preferences)
                VALUES (?, ?, ?, ?, ?)
            ''', customer)
        
        # Sample employees
        employees = [
            ("Alice Wilson", "alice@aufraumenbee.com", "555-0201", "Residential cleaning, deep cleaning", 25.0, "permanent", "Mon-Fri 8AM-6PM", True),
            ("Bob Davis", "bob@aufraumenbee.com", "555-0202", "Office cleaning, carpet cleaning", 22.0, "permanent", "Flexible", True),
            ("Carol Martinez", "carol@aufraumenbee.com", "555-0203", "Move-out cleaning, organizing", 20.0, "contract", "Weekends only", False),
        ]
        
        for employee in employees:
            conn.execute('''
                INSERT OR IGNORE INTO employees (name, email, phone, skills, hourly_rate, employment_type, availability, background_check)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', employee)
        
        # Sample inventory
        inventory_items = [
            ("All-Purpose Cleaner", "Chemicals", 50, 8.99, 20, "CleanCorp"),
            ("Microfiber Cloths", "Equipment", 100, 2.50, 30, "SupplyCo"),
            ("Vacuum Bags", "Equipment", 25, 12.99, 15, "VacuumPlus"),
            ("Toilet Paper", "Supplies", 200, 1.25, 50, "PaperGoods Inc"),
        ]
        
        for item in inventory_items:
            conn.execute('''
                INSERT OR IGNORE INTO inventory (item_name, category, quantity, unit_price, minimum_stock, supplier)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', item)
        
        conn.commit()
        conn.close()
    
    def get_customers(self) -> pd.DataFrame:
        """Get all customers"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM customers ORDER BY created_at DESC", conn)
        conn.close()
        return df
    
    def get_employees(self) -> pd.DataFrame:
        """Get all employees"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM employees ORDER BY created_at DESC", conn)
        conn.close()
        return df
    
    def get_jobs(self, status: Optional[str] = None) -> pd.DataFrame:
        """Get jobs, optionally filtered by status"""
        conn = self.get_connection()
        if status:
            query = '''
                SELECT j.*, c.name as customer_name, e.name as employee_name
                FROM jobs j
                JOIN customers c ON j.customer_id = c.id
                LEFT JOIN employees e ON j.employee_id = e.id
                WHERE j.status = ?
                ORDER BY j.scheduled_date, j.scheduled_time
            '''
            df = pd.read_sql_query(query, conn, params=[status])
        else:
            query = '''
                SELECT j.*, c.name as customer_name, e.name as employee_name
                FROM jobs j
                JOIN customers c ON j.customer_id = c.id
                LEFT JOIN employees e ON j.employee_id = e.id
                ORDER BY j.created_at DESC
            '''
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        conn = self.get_connection()
        
        stats = {}
        
        # Total customers
        stats['total_customers'] = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        
        # Total employees
        stats['total_employees'] = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
        
        # Pending jobs
        stats['pending_jobs'] = conn.execute("SELECT COUNT(*) FROM jobs WHERE status = 'pending'").fetchone()[0]
        
        # Today's jobs
        stats['today_jobs'] = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE scheduled_date = date('now') AND status IN ('approved', 'assigned', 'in_progress')"
        ).fetchone()[0]
        
        # This month's revenue
        stats['monthly_revenue'] = conn.execute(
            "SELECT COALESCE(SUM(price), 0) FROM jobs WHERE status = 'completed' AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')"
        ).fetchone()[0]
        
        # Low stock items
        stats['low_stock_items'] = conn.execute(
            "SELECT COUNT(*) FROM inventory WHERE quantity <= minimum_stock"
        ).fetchone()[0]
        
        conn.close()
        return stats
