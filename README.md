# 🧹 Aufraumenbee - Cleaning Service Management System

A comprehensive cleaning service management application built with Streamlit and Python. This application provides end-to-end management capabilities for cleaning service businesses, from customer bookings to employee scheduling and invoicing.

## 🚀 Features

### Core Management Features
- **Customer Management**: Customer profiles, service history, preferences, ratings
- **Employee Management**: Staff profiles, availability, performance tracking, contract/permanent employees
- **Job Management**: Service booking, approval workflow, employee assignment
- **Booking Requests**: Customer booking interface with manager approval system
- **Scheduling**: Calendar view and job scheduling with drag-and-drop functionality
- **Invoicing**: Automated billing, payment tracking, tax calculations
- **Inventory Management**: Cleaning supplies and equipment tracking with low-stock alerts

### Public Customer Portal Features
- **Customer Registration**: Self-service account creation for customers
- **Service Booking**: Online booking system with real-time slot availability
- **Service Catalog**: Browse available cleaning services with pricing
- **Booking Management**: View and manage personal bookings
- **Slot Management**: Admin can create and manage available time slots
- **Real-time Availability**: Only available slots are shown to customers

### Business Operations
- **Analytics & Reporting**: Revenue reports, job analytics, customer satisfaction trends
- **User Authentication**: Role-based access control (Admin, Manager, Employee, Customer)
- **Real-time Dashboard**: Key metrics and recent activity overview
- **Mobile-Friendly**: Responsive design for mobile and tablet access
- **Portal Management**: Admin interface to manage customer portal settings

### Workflow Features
1. **Customer Registration**: Customers create accounts on public portal
2. **Service Booking**: Select service, date, and available time slots
3. **Admin Approval**: Service managers review and approve/reject bookings
4. **Employee Assignment**: Automatic or manual assignment of available employees
5. **Job Tracking**: Real-time status updates from pending to completed
6. **Automated Invoicing**: Generate invoices for completed jobs
7. **Performance Analytics**: Track business metrics and employee performance

## 🛠️ Technology Stack

- **Frontend**: Streamlit with responsive design
- **Backend**: Python with SQLite database
- **Authentication**: bcrypt for secure password hashing
- **Data Visualization**: Plotly for charts and analytics
- **Database**: SQLite for local data storage with dual portal support
- **UI Components**: Streamlit components with modern styling

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/kunnath/Projects/Aufraumenbee
   ```

2. **The Python virtual environment is already configured**:
   ```bash
   # Virtual environment is located at .venv/
   # Python executable: .venv/bin/python
   ```

3. **Install dependencies** (already installed):
   ```bash
   .venv/bin/python -m pip install -r requirements.txt
   ```

4. **Run the applications**:
   
   **Quick Start (Recommended)**:
   ```bash
   ./start_apps.sh
   ```
   This will start both portals simultaneously.
   
   **Manual Start**:
   
   **Main Admin Portal**:
   ```bash
   .venv/bin/python -m streamlit run app.py
   ```
   
   **Customer Portal** (separate application):
   ```bash
   .venv/bin/python -m streamlit run customer_portal.py --server.port 8502
   ```

5. **Access the applications**:
   - **Admin Portal**: Open your browser and go to `http://localhost:8501`
   - **Customer Portal**: Open your browser and go to `http://localhost:8502`

## 🌐 Application Architecture

### Admin Portal (`app.py`)
- Business management interface
- Employee and customer management
- Job scheduling and assignment
- Analytics and reporting
- Portal management (manage customer portal settings)

### Customer Portal (`customer_portal.py`)
- Public-facing customer registration and login
- Service browsing and booking
- Real-time slot availability
- Personal booking management

Both portals share the same SQLite database (`aufraumenbee.db`) for seamless data integration.

## 🔐 Default Login Credentials

### Admin Portal
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator

### Customer Portal
- Customers register their own accounts
- No default customer credentials (self-registration)

## 📱 User Roles & Permissions

### Administrator
- Full access to all features
- User management and system settings
- Analytics and reporting
- Customer and employee management

### Manager
- Job approval and assignment
- Employee scheduling
- Customer management
- Invoicing and billing

### Employee
- View assigned jobs
- Update job status
- Time tracking
- Customer communication

### Customer (Admin Portal)
- Submit booking requests
- View service history
- Track job status
- Make payments

### Customer (Public Portal)
- Self-registration and account management
- Browse available services with pricing
- Book services with real-time slot availability
- Manage personal bookings
- View booking history and status

## � Customer Booking Workflow

### For Customers:
1. **Registration**: Create account on customer portal (`http://localhost:8502`)
2. **Browse Services**: View available cleaning services with descriptions and pricing
3. **Select Date**: Choose preferred service date (next day onwards)
4. **Choose Time Slot**: Select from available time slots (managed by admin)
5. **Book Service**: Provide service address and special instructions
6. **Confirmation**: Receive booking confirmation with details

### For Administrators:
1. **Manage Services**: Create, edit, and price cleaning services (Portal Management → Services)
2. **Manage Time Slots**: Create available time slots for booking (Portal Management → Time Slots)
3. **Review Bookings**: Monitor customer bookings (Portal Management → Customer Bookings)
4. **Confirm Bookings**: Approve or manage customer booking requests
5. **Assign Employees**: Assign staff to confirmed bookings (Job Management)

## �🗄️ Database Schema

The application uses SQLite with the following main tables:

### Admin Portal Tables:
- **users**: User authentication and roles
- **customers**: Customer information and preferences  
- **employees**: Staff details and availability
- **jobs**: Service bookings and assignments
- **invoices**: Billing and payment tracking

### Customer Portal Tables:
- **customer_users**: Public customer accounts
- **service_types**: Available services with pricing
- **time_slots**: Available booking slots
- **customer_bookings**: Customer service bookings
- **inventory**: Cleaning supplies and equipment

## 🔧 Configuration

### Environment Variables
Create a `.env` file for additional configuration:
```
DB_NAME=aufraumenbee.db
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### Customization
- Modify service types in the booking form
- Adjust pricing models in job management
- Customize invoice templates
- Configure email notifications (future enhancement)

## 📊 Analytics & Reporting

The application provides comprehensive analytics:

- **Revenue Tracking**: Monthly and yearly revenue reports
- **Job Analytics**: Status distribution and completion rates
- **Employee Performance**: Productivity and rating metrics
- **Customer Insights**: Service preferences and satisfaction scores
- **Inventory Reports**: Stock levels and usage patterns

## 🚀 Deployment

### Local Development
```bash
.venv/bin/python -m streamlit run app.py
```

### Production Deployment
For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Implementing proper authentication middleware
- Setting up SSL certificates
- Configuring environment variables
- Using a process manager like PM2 or systemd

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Customer management
- ✅ Employee management
- ✅ Job booking and approval
- ✅ Basic scheduling
- ✅ Invoicing system

### Phase 2 (Planned)
- 📅 Advanced calendar integration
- 📧 Email notifications
- 📱 Mobile app for employees
- 🗺️ GPS tracking and route optimization
- 💳 Payment gateway integration

### Phase 3 (Future)
- 🤖 AI-powered scheduling optimization
- 📊 Advanced analytics and forecasting
- 🔗 Third-party integrations (QuickBooks, etc.)
- 📞 SMS and WhatsApp notifications
- 🎯 Marketing campaign management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- Streamlit community for the excellent framework
- Python ecosystem for robust libraries
- Open source contributors

---

**Aufraumenbee** - Making cleaning service management effortless! 🧹✨
# CleaningServiceManagementSystem
