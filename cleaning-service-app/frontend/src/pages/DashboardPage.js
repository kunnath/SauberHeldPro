import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUser, FaEdit, FaTrash, FaPlus, FaStar, FaSignOutAlt, FaEye } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';

const DashboardContainer = styled.div`
  padding: ${props => props.theme.spacing.xl} 0;
  min-height: 80vh;
`;

const DashboardHeader = styled.div`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.xl} 0;
  margin-bottom: ${props => props.theme.spacing.xl};
  border-radius: 15px;
`;

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.md};
    text-align: center;
  }
`;

const WelcomeText = styled.div`
  h1 {
    font-size: 2.5rem;
    margin-bottom: ${props => props.theme.spacing.xs};
    
    @media (max-width: ${props => props.theme.breakpoints.mobile}) {
      font-size: 2rem;
    }
  }
  
  p {
    font-size: 1.2rem;
    opacity: 0.9;
  }
`;

const HeaderActions = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    width: 100%;
  }
`;

const Button = styled(motion.button)`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border: none;
  border-radius: 8px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  cursor: pointer;
  transition: all 0.3s ease;
  
  &.primary {
    background: white;
    color: ${props => props.theme.colors.secondary};
  }
  
  &.secondary {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
  }
  
  &.danger {
    background: ${props => props.theme.colors.danger};
    color: white;
  }
  
  &:hover {
    transform: translateY(-1px);
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const StatCard = styled(motion.div)`
  background: white;
  padding: ${props => props.theme.spacing.xl};
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
`;

const StatIcon = styled.div`
  font-size: 3rem;
  color: ${props => props.theme.colors.secondary};
  margin-bottom: ${props => props.theme.spacing.md};
`;

const StatNumber = styled.div`
  font-size: 2.5rem;
  font-weight: bold;
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const StatLabel = styled.div`
  color: ${props => props.theme.colors.gray};
  font-size: 1.1rem;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: ${props => props.theme.spacing.xl};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
  }
`;

const SectionCard = styled.div`
  background: white;
  border-radius: 15px;
  padding: ${props => props.theme.spacing.xl};
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const SectionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.lg};
  
  h2 {
    color: ${props => props.theme.colors.dark};
    font-size: 1.8rem;
  }
`;

const BookingCard = styled(motion.div)`
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 10px;
  padding: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.md};
  transition: all 0.3s ease;
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
    transform: translateY(-2px);
  }
  
  &.upcoming {
    border-color: ${props => props.theme.colors.success};
    background: rgba(40, 167, 69, 0.05);
  }
  
  &.completed {
    border-color: ${props => props.theme.colors.gray};
    opacity: 0.8;
  }
`;

const BookingHeader = styled.div`
  display: flex;
  justify-content: between;
  align-items: flex-start;
  margin-bottom: ${props => props.theme.spacing.md};
`;

const BookingInfo = styled.div`
  flex: 1;
`;

const BookingTitle = styled.h3`
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.xs};
  font-size: 1.3rem;
`;

const BookingDetails = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.md};
  
  span {
    display: flex;
    align-items: center;
    gap: ${props => props.theme.spacing.xs};
    color: ${props => props.theme.colors.gray};
    font-size: 0.9rem;
  }
`;

const BookingActions = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.sm};
  margin-left: auto;
`;

const StatusBadge = styled.span`
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  
  &.pending {
    background: rgba(255, 193, 7, 0.2);
    color: #856404;
  }
  
  &.confirmed {
    background: rgba(40, 167, 69, 0.2);
    color: #155724;
  }
  
  &.completed {
    background: rgba(108, 117, 125, 0.2);
    color: #495057;
  }
  
  &.cancelled {
    background: rgba(220, 53, 69, 0.2);
    color: #721c24;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xxl};
  color: ${props => props.theme.colors.gray};
  
  h3 {
    margin-bottom: ${props => props.theme.spacing.md};
    color: ${props => props.theme.colors.dark};
  }
  
  p {
    margin-bottom: ${props => props.theme.spacing.lg};
  }
`;

const ProfileCard = styled.div`
  h3 {
    color: ${props => props.theme.colors.dark};
    margin-bottom: ${props => props.theme.spacing.md};
  }
`;

const ProfileInfo = styled.div`
  margin-bottom: ${props => props.theme.spacing.lg};
  
  p {
    margin-bottom: ${props => props.theme.spacing.xs};
    color: ${props => props.theme.colors.gray};
    
    strong {
      color: ${props => props.theme.colors.dark};
    }
  }
`;

const QuickActions = styled.div`
  display: grid;
  gap: ${props => props.theme.spacing.sm};
`;

const ActionButton = styled(motion.button)`
  background: ${props => props.theme.colors.light};
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 8px;
  padding: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.dark};
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  transition: all 0.3s ease;
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
    background: white;
  }
`;

const DashboardPage = () => {
  const { user, logout, isAuthenticated, isLoading } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [dashboardLoading, setDashboardLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // If user is not authenticated, redirect to login
    if (!isLoading && !isAuthenticated) {
      navigate('/login');
      return;
    }

    // If user is authenticated, load dashboard data
    if (isAuthenticated && user) {
      // Simulate loading bookings data
      setTimeout(() => {
        setBookings([
          {
            id: 1,
            service: 'Deep Cleaning',
            date: '2025-06-28',
            time: '10:00',
            duration: '4 hours',
            address: 'Alexanderplatz 1, Berlin',
            price: 180.00,
            status: 'confirmed',
            cleaner: 'Maria Schmidt'
          },
          {
            id: 2,
            service: 'Basic Cleaning',
            date: '2025-06-15',
            time: '14:00',
            duration: '2 hours',
            address: 'Alexanderplatz 1, Berlin',
            price: 57.80,
            status: 'completed',
            cleaner: 'Anna Mueller',
            rating: 5
          },
          {
            id: 3,
            service: 'Office Cleaning',
            date: '2025-05-30',
            time: '09:00',
            duration: '3 hours',
            address: 'Potsdamer Platz 5, Berlin',
            price: 105.00,
            status: 'completed',
            cleaner: 'Thomas Weber',
            rating: 4
          }
        ]);

        setDashboardLoading(false);
      }, 1000);
    }
  }, [navigate, isAuthenticated, isLoading, user]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleNewBooking = () => {
    navigate('/booking');
  };

  const handleViewCalendar = () => {
    // You can implement calendar view or navigate to a calendar page
    // For now, let's scroll to the bookings section
    const bookingsSection = document.querySelector('[data-section="bookings"]');
    if (bookingsSection) {
      bookingsSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleLeaveReview = () => {
    // Navigate to reviews page or open review modal
    // For now, let's navigate to a reviews page or contact page
    navigate('/contact');
  };

  const upcomingBookings = bookings.filter(booking => booking.status === 'confirmed' || booking.status === 'pending');
  const pastBookings = bookings.filter(booking => booking.status === 'completed');
  const totalSpent = bookings.filter(booking => booking.status === 'completed').reduce((sum, booking) => sum + booking.price, 0);

  // Show loading if auth is loading or dashboard is loading
  if (isLoading || dashboardLoading) {
    return (
      <DashboardContainer>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '4rem 0' }}>
            <h2>Loading your dashboard...</h2>
            <p style={{ color: '#666', marginTop: '1rem' }}>
              {isLoading ? 'Verifying authentication...' : 'Loading your data...'}
            </p>
          </div>
        </div>
      </DashboardContainer>
    );
  }

  // If not authenticated after loading, don't render anything (will redirect)
  if (!isAuthenticated) {
    return null;
  }

  return (
    <DashboardContainer>
      <div className="container">
        <DashboardHeader>
          <div className="container">
            <HeaderContent>
              <WelcomeText>
                <h1>Welcome back, {user?.firstName || 'User'}!</h1>
                <p>Manage your bookings and account settings</p>
              </WelcomeText>
              <HeaderActions>
                <Button
                  className="primary"
                  onClick={handleNewBooking}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaPlus />
                  New Booking
                </Button>
                <Button
                  className="secondary"
                  onClick={handleLogout}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaSignOutAlt />
                  Logout
                </Button>
              </HeaderActions>
            </HeaderContent>
          </div>
        </DashboardHeader>

        <StatsGrid>
          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <StatIcon><FaCalendarAlt /></StatIcon>
            <StatNumber>{bookings.length}</StatNumber>
            <StatLabel>Total Bookings</StatLabel>
          </StatCard>

          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <StatIcon><FaClock /></StatIcon>
            <StatNumber>{upcomingBookings.length}</StatNumber>
            <StatLabel>Upcoming</StatLabel>
          </StatCard>

          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <StatIcon><FaStar /></StatIcon>
            <StatNumber>4.8</StatNumber>
            <StatLabel>Average Rating</StatLabel>
          </StatCard>

          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <StatIcon><FaUser /></StatIcon>
            <StatNumber>€{totalSpent.toFixed(0)}</StatNumber>
            <StatLabel>Total Spent</StatLabel>
          </StatCard>
        </StatsGrid>

        <ContentGrid>
          <SectionCard data-section="bookings">
            <SectionHeader>
              <h2>Your Bookings</h2>
              <Button
                className="primary"
                onClick={handleNewBooking}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FaPlus />
                Book Now
              </Button>
            </SectionHeader>

            {bookings.length === 0 ? (
              <EmptyState>
                <h3>No bookings yet</h3>
                <p>Book your first cleaning service to get started!</p>
                <Button
                  className="primary"
                  onClick={handleNewBooking}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaPlus />
                  Book Your First Cleaning
                </Button>
              </EmptyState>
            ) : (
              <>
                {upcomingBookings.length > 0 && (
                  <>
                    <h3 style={{ color: '#28a745', marginBottom: '1rem' }}>Upcoming Bookings</h3>
                    {upcomingBookings.map(booking => (
                      <BookingCard
                        key={booking.id}
                        className="upcoming"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                      >
                        <BookingHeader>
                          <BookingInfo>
                            <BookingTitle>{booking.service}</BookingTitle>
                            <BookingDetails>
                              <span><FaCalendarAlt /> {new Date(booking.date).toLocaleDateString()}</span>
                              <span><FaClock /> {booking.time}</span>
                              <span><FaMapMarkerAlt /> {booking.address}</span>
                            </BookingDetails>
                            <div style={{ marginBottom: '0.5rem' }}>
                              <StatusBadge className={booking.status}>{booking.status}</StatusBadge>
                            </div>
                            <p style={{ color: '#666', margin: 0 }}>
                              Cleaner: <strong>{booking.cleaner}</strong> • Duration: {booking.duration} • €{booking.price}
                            </p>
                          </BookingInfo>
                          <BookingActions>
                            <Button 
                              className="primary" 
                              whileHover={{ scale: 1.05 }}
                              onClick={() => navigate(`/booking/${booking.id}`)}
                            >
                              <FaEye />
                              View Details
                            </Button>
                            <Button className="secondary" whileHover={{ scale: 1.05 }}>
                              <FaEdit />
                              Edit
                            </Button>
                          </BookingActions>
                        </BookingHeader>
                      </BookingCard>
                    ))}
                  </>
                )}

                {pastBookings.length > 0 && (
                  <>
                    <h3 style={{ color: '#666', marginBottom: '1rem', marginTop: '2rem' }}>Past Bookings</h3>
                    {pastBookings.map(booking => (
                      <BookingCard
                        key={booking.id}
                        className="completed"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                      >
                        <BookingHeader>
                          <BookingInfo>
                            <BookingTitle>{booking.service}</BookingTitle>
                            <BookingDetails>
                              <span><FaCalendarAlt /> {new Date(booking.date).toLocaleDateString()}</span>
                              <span><FaClock /> {booking.time}</span>
                              <span><FaMapMarkerAlt /> {booking.address}</span>
                            </BookingDetails>
                            <div style={{ marginBottom: '0.5rem' }}>
                              <StatusBadge className={booking.status}>{booking.status}</StatusBadge>
                              {booking.rating && (
                                <span style={{ marginLeft: '0.5rem' }}>
                                  {'⭐'.repeat(booking.rating)} ({booking.rating}/5)
                                </span>
                              )}
                            </div>
                            <p style={{ color: '#666', margin: 0 }}>
                              Cleaner: <strong>{booking.cleaner}</strong> • Duration: {booking.duration} • €{booking.price}
                            </p>
                          </BookingInfo>
                          <BookingActions>
                            <Button 
                              className="primary" 
                              whileHover={{ scale: 1.05 }}
                              onClick={() => navigate(`/booking/${booking.id}`)}
                            >
                              <FaEye />
                              View Details
                            </Button>
                            <Button className="secondary" whileHover={{ scale: 1.05 }}>
                              Rebook
                            </Button>
                          </BookingActions>
                        </BookingHeader>
                      </BookingCard>
                    ))}
                  </>
                )}
              </>
            )}
          </SectionCard>

          <div>
            <SectionCard style={{ marginBottom: '1.5rem' }}>
              <ProfileCard>
                <h3>Profile Information</h3>
                <ProfileInfo>
                  <p><strong>Name:</strong> {user?.firstName} {user?.lastName}</p>
                  <p><strong>Email:</strong> {user?.email}</p>
                  <p><strong>Phone:</strong> {user?.phone || 'Not provided'}</p>
                  <p><strong>Address:</strong> {user?.address || 'Not provided'}</p>
                  <p><strong>Member since:</strong> {new Date().toLocaleDateString()}</p>
                </ProfileInfo>
                <Button
                  className="secondary"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaEdit />
                  Edit Profile
                </Button>
              </ProfileCard>
            </SectionCard>

            <SectionCard>
              <h3 style={{ marginBottom: '1rem' }}>Quick Actions</h3>
              <QuickActions>
                <ActionButton
                  onClick={handleNewBooking}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <FaPlus />
                  New Booking
                </ActionButton>
                <ActionButton
                  onClick={handleViewCalendar}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <FaCalendarAlt />
                  View Calendar
                </ActionButton>
                <ActionButton
                  onClick={handleLeaveReview}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <FaStar />
                  Leave Review
                </ActionButton>
              </QuickActions>
            </SectionCard>
          </div>
        </ContentGrid>
      </div>
    </DashboardContainer>
  );
};

export default DashboardPage;
