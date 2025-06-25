# Aufraumenbee - Cleaning Service Management System
## Production Documentation

### 🎯 System Overview

Aufraumenbee is a comprehensive cleaning service management system designed to streamline operations for cleaning businesses. The system provides both administrative tools for business management and a customer-facing portal for service bookings.

### 📋 Features

#### Admin Portal (http://localhost:8501)
- **Dashboard**: Real-time business metrics and overview
- **Customer Management**: Unified customer database from all sources
- **Job Management**: Service scheduling and assignment
- **Employee Management**: Staff profiles and performance tracking
- **Invoicing**: Automated billing and payment tracking
- **Inventory**: Cleaning supplies and equipment management
- **Reports**: Business analytics and performance metrics

#### Customer Portal (http://localhost:8502)
- **Registration**: Self-service account creation
- **Service Catalog**: Browse available cleaning services
- **Booking System**: Schedule cleaning appointments
- **Account Management**: Profile and booking history
- **Status Tracking**: Real-time booking status updates

### 🚀 Quick Start Guide

#### Prerequisites
- Python 3.8 or higher
- Internet connection for package installation

#### Installation & Demo
```bash
# Make the startup script executable
chmod +x start_production_demo.sh

# Start the demo
./start_production_demo.sh
```

#### Demo Credentials
- **Admin Portal**: username=`admin`, password=`admin123`
- **Customer Portal**: Register a new account or use existing

### 🗄️ Database Schema

The system uses SQLite with the following key tables:

#### Users Table (Admin Access)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT CHECK (role IN ('admin', 'manager', 'employee')),
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Customers Table (Unified Customer Data)
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    registration_source TEXT DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

#### Customer Users Table (Portal Login)
```sql
CREATE TABLE customer_users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Jobs Table
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    employee_id INTEGER,
    service_type TEXT NOT NULL,
    scheduled_date DATE NOT NULL,
    scheduled_time TEXT NOT NULL,
    duration_hours INTEGER DEFAULT 2,
    hourly_rate REAL DEFAULT 25.0,
    total_amount REAL,
    status TEXT DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);
```

### 🔄 Customer Integration Flow

1. **Customer Registration**: 
   - Customer registers via customer portal
   - Account created in both `customer_users` and `customers` tables
   - Registration source marked as 'portal'

2. **Admin Visibility**:
   - Admin can see all customers regardless of registration source
   - Unified customer list shows portal and admin-created customers
   - Customer search works across all registration sources

3. **Booking Process**:
   - Customer books service via portal
   - Booking stored in `customer_bookings` table
   - Admin can view and manage all bookings

### 🎨 Key Design Decisions

#### Security
- Passwords hashed using bcrypt
- Role-based access control
- Session-based authentication

#### Database Design
- Unified customer data across admin and customer portals
- Foreign key relationships for data integrity
- Audit trails with timestamps

#### User Experience
- Responsive design for mobile and desktop
- Intuitive navigation
- Real-time status updates
- Professional styling with custom CSS

### 📊 Demo Scenario

#### For Client Demonstration:

1. **Show Customer Portal** (http://localhost:8502):
   - Register a new customer account
   - Browse available services
   - Book a cleaning service
   - Show booking confirmation

2. **Show Admin Portal** (http://localhost:8501):
   - Login with admin credentials
   - Show customer in Customer Management
   - View booking in Job Management
   - Create invoice for the service
   - Show dashboard metrics

3. **Key Points to Highlight**:
   - Seamless customer self-service
   - Real-time data synchronization
   - Professional business management tools
   - Scalable architecture
   - Mobile-friendly design

### 🔧 Customization Options

#### Branding
- Colors and styling can be customized in CSS sections
- Logo and company name easily replaceable
- Theme consistency across both portals

#### Services
- Service types and pricing configurable
- Add/remove services via admin interface
- Custom service descriptions and features

#### Business Rules
- Hourly rates and pricing structures
- Tax calculations
- Booking availability rules
- Status workflow customization

### 📈 Future Enhancements

#### Potential Additions
- Mobile app development
- SMS/Email notifications
- Payment gateway integration
- Calendar synchronization
- GPS tracking for employees
- Customer feedback system
- Multi-language support
- Advanced reporting and analytics

### 🛠️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite (easily upgradable to PostgreSQL/MySQL)
- **Authentication**: bcrypt for password hashing
- **Data Processing**: Pandas for data manipulation
- **Styling**: Custom CSS for professional appearance

### 📞 Support & Maintenance

#### System Requirements
- Minimal server requirements
- Can run on basic VPS or cloud instance
- Database backup and restoration procedures
- Update and maintenance guidelines

#### Production Deployment
- Environment variable configuration
- SSL certificate setup
- Domain configuration
- Performance optimization

### 💼 Business Value

#### For Cleaning Service Businesses:
- **Efficiency**: Automated booking and scheduling
- **Professionalism**: Modern customer interface
- **Growth**: Scalable customer management
- **Insights**: Business analytics and reporting
- **Cost Savings**: Reduced administrative overhead
- **Customer Satisfaction**: Self-service convenience

#### ROI Indicators:
- Reduced phone-based bookings
- Increased customer retention
- Improved scheduling efficiency
- Better financial tracking
- Enhanced customer experience

---

**Aufraumenbee Development Team**  
Version 1.0 - Production Ready  
June 25, 2025
