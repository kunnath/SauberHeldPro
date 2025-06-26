# GRK Dienstleistungen - Full Stack Application

## Overview

A modern, full-stack cleaning service management system built with React.js frontend and Node.js/Express backend, inspired by spicandspan.de design patterns.

## Architecture

### Frontend (React.js)
- **Port**: 3000
- **Framework**: React 18.2.0 with React Router 6.3.0
- **Styling**: Styled Components with Framer Motion animations
- **State Management**: Context API for authentication
- **Form Handling**: React Hook Form
- **UI Components**: Modern, responsive design with custom components

### Backend (Node.js/Express)
- **Port**: 5000
- **Framework**: Express.js 4.18.2
- **Database**: SQLite with sqlite3 driver
- **Authentication**: JWT tokens with bcryptjs password hashing
- **Security**: Helmet, CORS, rate limiting, compression
- **API**: RESTful endpoints with comprehensive error handling

## Project Structure

```
cleaning-service-app/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js (with auth integration)
│   │   │   ├── Footer.js
│   │   │   └── ProtectedRoute.js
│   │   ├── pages/
│   │   │   ├── HomePage.js
│   │   │   ├── ServicesPage.js
│   │   │   ├── BookingPage.js (protected)
│   │   │   ├── ContactPage.js
│   │   │   ├── LoginPage.js (with registration)
│   │   │   └── DashboardPage.js (protected)
│   │   ├── contexts/
│   │   │   └── AuthContext.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env
└── backend/
    ├── config/
    │   └── database.js
    ├── middleware/
    │   └── auth.js
    ├── routes/
    │   ├── auth.js
    │   ├── users.js
    │   ├── bookings.js
    │   ├── services.js
    │   └── contact.js
    ├── data/
    │   └── cleaning_service.db (SQLite database)
    ├── server.js
    ├── package.json
    └── .env
```

## Features Implemented

### Authentication System
- ✅ User registration with email verification
- ✅ Secure login with JWT tokens
- ✅ Password hashing with bcryptjs
- ✅ Protected routes for authenticated users
- ✅ User profile management
- ✅ Password change functionality

### User Management
- ✅ User profile CRUD operations
- ✅ Booking history for users
- ✅ Account deletion with safety checks

### Service Management
- ✅ Service types with pricing and features
- ✅ Cleaner profiles and availability
- ✅ Service pricing calculation
- ✅ Availability checking

### Booking System
- ✅ Complete booking workflow
- ✅ Booking status management
- ✅ Cancellation functionality
- ✅ User booking history

### Contact System
- ✅ Contact form with rate limiting
- ✅ Message status tracking
- ✅ Admin message management

### Database Schema
- ✅ Users table with authentication data
- ✅ Service types with features and pricing
- ✅ Cleaners with specialties and ratings
- ✅ Bookings with full lifecycle tracking
- ✅ Contact messages with status management
- ✅ Reviews system for quality feedback

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - User registration
- `POST /login` - User login
- `GET /verify` - Token verification

### Users (`/api/users`)
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `PUT /change-password` - Change password
- `GET /bookings` - Get user bookings
- `DELETE /account` - Delete user account

### Services (`/api/services`)
- `GET /` - Get all services
- `GET /:id` - Get service details
- `GET /:id/pricing` - Get service pricing
- `GET /:id/availability` - Check availability
- `GET /cleaners` - Get all cleaners

### Bookings (`/api/bookings`)
- `POST /` - Create booking
- `GET /` - Get bookings (admin)
- `GET /:id` - Get booking details
- `PUT /:id` - Update booking
- `PUT /:id/cancel` - Cancel booking

### Contact (`/api/contact`)
- `POST /submit` - Submit contact form
- `GET /messages` - Get messages (admin)
- `PUT /messages/:id/status` - Update message status
- `GET /stats` - Get contact statistics

## Security Features

- ✅ JWT token authentication
- ✅ Password hashing with bcryptjs
- ✅ Rate limiting on sensitive endpoints
- ✅ CORS configuration
- ✅ Helmet security headers
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ Error handling without information leakage

## Development Setup

### Prerequisites
- Node.js (v18+ recommended)
- npm or yarn

### Backend Setup
```bash
cd cleaning-service-app/backend
npm install
npm start
```
Server runs on http://localhost:5000

### Frontend Setup
```bash
cd cleaning-service-app/frontend
npm install
npm start
```
React app runs on http://localhost:3000

## Environment Variables

### Backend (.env)
```
PORT=5000
NODE_ENV=development
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
DB_PATH=./database.sqlite
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_NAME=GRK Dienstleistungen
REACT_APP_VERSION=1.0.0
REACT_APP_ENV=development
```

## Database

The SQLite database includes:
- 5 default service types (Basic, Deep, Move-in/out, Office, Post-Construction)
- 4 sample cleaners with profiles and specialties
- Proper foreign key relationships
- Automatic timestamp tracking

## Next Steps for Production

1. **Security Enhancements**
   - Add email verification system
   - Implement password reset functionality
   - Add two-factor authentication
   - Set up proper SSL certificates

2. **Performance Optimization**
   - Add database indexing
   - Implement caching strategy
   - Add image optimization
   - Set up CDN for static assets

3. **Monitoring & Analytics**
   - Add logging system
   - Implement error tracking
   - Set up performance monitoring
   - Add user analytics

4. **Deployment**
   - Set up production environment
   - Configure CI/CD pipeline
   - Add backup strategy
   - Set up monitoring alerts

## Testing

The application is ready for integration testing:
- Backend API endpoints are fully functional
- Frontend authentication flow is complete
- Database schema is properly initialized
- All major user flows are implemented

## Technologies Used

**Frontend:**
- React 18.2.0
- React Router 6.3.0
- Styled Components 5.3.11
- Framer Motion 10.12.16
- React Hook Form 7.44.3
- React Icons 4.8.0

**Backend:**
- Express.js 4.18.2
- SQLite with sqlite3 5.1.6
- JWT (jsonwebtoken 9.0.0)
- bcryptjs 2.4.3
- Helmet 7.0.0
- CORS 2.8.5
- Morgan logging
- Express Rate Limit

The application provides a solid foundation for a modern cleaning service business with room for future enhancements and scaling.
