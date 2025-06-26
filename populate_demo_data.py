#!/usr/bin/env python3
"""
Demo Data Population Script for Admin Portal Testing
This script populates the database with sample data for demo purposes
"""

import sqlite3
from datetime import datetime, date, timedelta
import random

# Database configuration
DB_PATH = 'cleaning-service-app/backend/data/cleaning_service.db'

def get_db_connection():
    """Get a database connection"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def populate_employees():
    """Add sample employees"""
    conn = get_db_connection()
    
    employees = [
        ('Maria Schmidt', 'maria.schmidt@grk-dienstleistungen.de', '+49 30 12345678', 25.0, 'Deep cleaning, Kitchen, Bathroom', 'Full-time', 'active'),
        ('Thomas Mueller', 'thomas.mueller@grk-dienstleistungen.de', '+49 30 12345679', 22.0, 'Basic cleaning, Office cleaning', 'Part-time', 'active'),
        ('Anna Weber', 'anna.weber@grk-dienstleistungen.de', '+49 30 12345680', 28.0, 'Window cleaning, Move-in/Move-out', 'Full-time', 'active'),
        ('Stefan Fischer', 'stefan.fischer@grk-dienstleistungen.de', '+49 30 12345681', 24.0, 'Carpet cleaning, Basic cleaning', 'Contract', 'active'),
        ('Lisa Braun', 'lisa.braun@grk-dienstleistungen.de', '+49 30 12345682', 26.0, 'Deep cleaning, Office cleaning', 'Full-time', 'inactive'),
    ]
    
    for emp in employees:
        try:
            conn.execute('''
                INSERT OR IGNORE INTO employees (name, email, phone, hourly_rate, specialties, availability, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', emp)
            print(f"✅ Added employee: {emp[0]}")
        except Exception as e:
            print(f"❌ Error adding employee {emp[0]}: {e}")
    
    conn.commit()
    conn.close()

def populate_customers():
    """Add sample customers (admin-created)"""
    conn = get_db_connection()
    
    customers = [
        ('Hans Zimmermann', 'hans.zimmermann@email.de', '+49 30 11111111', 'Musterstraße 1, 10115 Berlin', 'Weekly cleaning, no harsh chemicals', 4.5, 12),
        ('Petra Hoffmann', 'petra.hoffmann@email.de', '+49 30 22222222', 'Alexanderplatz 2, 10178 Berlin', 'Bi-weekly deep cleaning', 4.8, 8),
        ('Klaus Richter', 'klaus.richter@email.de', '+49 30 33333333', 'Friedrichstraße 3, 10117 Berlin', 'Office cleaning only', 4.2, 15),
        ('Sabine König', 'sabine.koenig@email.de', '+49 30 44444444', 'Unter den Linden 4, 10117 Berlin', 'Move-out cleaning needed', 4.9, 3),
    ]
    
    for cust in customers:
        try:
            conn.execute('''
                INSERT OR IGNORE INTO customers (name, email, phone, address, preferences, rating, total_jobs)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', cust)
            print(f"✅ Added customer: {cust[0]}")
        except Exception as e:
            print(f"❌ Error adding customer {cust[0]}: {e}")
    
    conn.commit()
    conn.close()

def populate_jobs():
    """Add sample jobs/bookings"""
    conn = get_db_connection()
    
    # Get customer and employee IDs
    customers = conn.execute("SELECT id FROM customers").fetchall()
    employees = conn.execute("SELECT id FROM employees WHERE status = 'active'").fetchall()
    
    if not customers or not employees:
        print("❌ No customers or employees found. Adding customers and employees first.")
        return
    
    # Sample jobs
    service_types = ['Basic Cleaning', 'Deep Cleaning', 'Office Cleaning', 'Window Cleaning', 'Carpet Cleaning']
    statuses = ['pending', 'confirmed', 'in_progress', 'completed']
    
    jobs = []
    for i in range(20):  # Create 20 sample jobs
        customer_id = random.choice(customers)[0]
        employee_id = random.choice(employees)[0] if random.random() > 0.3 else None  # 70% assigned
        service_type = random.choice(service_types)
        status = random.choice(statuses)
        
        # Generate random date within next 30 days
        base_date = date.today()
        random_days = random.randint(-10, 30)
        scheduled_date = base_date + timedelta(days=random_days)
        
        # Generate random time
        hour = random.randint(9, 17)
        minute = random.choice([0, 30])
        scheduled_time = f"{hour:02d}:{minute:02d}"
        
        # Generate price based on service type
        base_prices = {
            'Basic Cleaning': 45,
            'Deep Cleaning': 75,
            'Office Cleaning': 55,
            'Window Cleaning': 35,
            'Carpet Cleaning': 65
        }
        price = base_prices[service_type] + random.randint(-10, 20)
        
        duration = random.choice([2, 3, 4, 5])
        
        job = (
            customer_id,
            employee_id,
            f"{service_type} for Customer {customer_id}",
            f"Detailed {service_type.lower()} service as requested.",
            scheduled_date.isoformat(),
            scheduled_time,
            duration,
            status,
            service_type,
            f"Address for Customer {customer_id}",
            price
        )
        jobs.append(job)
    
    for job in jobs:
        try:
            conn.execute('''
                INSERT INTO jobs (customer_id, employee_id, title, description, scheduled_date, 
                                scheduled_time, duration, status, service_type, location, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', job)
            print(f"✅ Added job: {job[2]}")
        except Exception as e:
            print(f"❌ Error adding job {job[2]}: {e}")
    
    conn.commit()
    conn.close()

def populate_demo_bookings():
    """Add some demo bookings that would come from the React frontend"""
    conn = get_db_connection()
    
    # Get existing users from customer portal
    users = conn.execute("SELECT id FROM users WHERE role = 'customer'").fetchall()
    service_types = conn.execute("SELECT id, name FROM service_types").fetchall()
    
    if not users:
        print("❌ No customer users found from React frontend")
        return
        
    if not service_types:
        print("❌ No service types found")
        return
    
    # Create sample bookings
    bookings = []
    for i in range(5):  # Create 5 sample bookings
        user_id = random.choice(users)[0]
        service_type_id = random.choice(service_types)[0]
        
        # Generate random date within next 14 days
        base_date = date.today()
        random_days = random.randint(1, 14)
        service_date = base_date + timedelta(days=random_days)
        
        # Generate random time
        hour = random.randint(9, 17)
        minute = random.choice([0, 30])
        service_time = f"{hour:02d}:{minute:02d}"
        
        price = random.choice([45, 55, 65, 75, 85])
        
        booking = (
            user_id,
            service_type_id,
            service_date.isoformat(),
            service_time,
            f"Demo booking {i+1} - customer requested service",
            random.choice(['Musterstraße 10, Berlin', 'Hauptstraße 20, Berlin', 'Berliner Allee 30, Berlin']),
            'pending',
            price,
            random.randint(2, 4)
        )
        bookings.append(booking)
    
    for booking in bookings:
        try:
            conn.execute('''
                INSERT INTO bookings (user_id, service_type_id, service_date, service_time, 
                                    special_instructions, address, status, total_price, estimated_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', booking)
            print(f"✅ Added booking from React frontend")
        except Exception as e:
            print(f"❌ Error adding booking: {e}")
    
    conn.commit()
    conn.close()

def main():
    """Main function to populate all demo data"""
    print("🚀 Populating Demo Data for GRK Dienstleistungen Admin Portal")
    print("=" * 60)
    
    print("\n📋 Adding Sample Employees...")
    populate_employees()
    
    print("\n👥 Adding Sample Customers...")
    populate_customers()
    
    print("\n📅 Adding Sample Jobs...")
    populate_jobs()
    
    print("\n🌐 Adding Sample Bookings from React Frontend...")
    populate_demo_bookings()
    
    print("\n✅ Demo data population completed!")
    print("🔧 Admin Portal: http://localhost:8502")
    print("👤 Login: admin / admin123")

if __name__ == "__main__":
    main()
