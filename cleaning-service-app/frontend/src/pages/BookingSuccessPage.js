import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { FaCheckCircle, FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUser, FaGift, FaArrowRight, FaHome, FaEnvelope, FaPhone, FaStar } from 'react-icons/fa';

// Animations
const celebration = keyframes`
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1.2) rotate(180deg); opacity: 1; }
  100% { transform: scale(1) rotate(360deg); opacity: 1; }
`;

const confetti = keyframes`
  0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
`;

const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-20px); }
  60% { transform: translateY(-10px); }
`;

const shimmer = keyframes`
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
`;

// Styled Components
const SuccessContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  position: relative;
  overflow: hidden;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const ConfettiPiece = styled.div`
  position: absolute;
  width: 8px;
  height: 8px;
  background: ${props => props.color};
  animation: ${confetti} 3s linear infinite;
  animation-delay: ${props => props.delay}s;
  left: ${props => props.left}%;
  opacity: 0.8;
`;

const SuccessCard = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 10;
`;

const SuccessHeader = styled.div`
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  
  @media (max-width: 768px) {
    padding: 2rem 1rem;
  }
`;

const SuccessIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: ${celebration} 1s ease-out;
  
  @media (max-width: 768px) {
    font-size: 3rem;
  }
`;

const SuccessTitle = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
  animation: ${bounce} 2s ease-in-out infinite;
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const SuccessSubtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
  
  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

const ContentSection = styled.div`
  padding: 2rem;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const BookingDetails = styled.div`
  background: #f8f9fa;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border-left: 4px solid #28a745;
`;

const DetailRow = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 0.75rem;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  svg {
    color: #6c757d;
    font-size: 1.1rem;
  }
  
  span {
    font-weight: 500;
  }
`;

const OfferSection = styled.div`
  background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
  border-radius: 15px;
  padding: 2rem;
  margin: 2rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -200px;
    width: 200px;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.4),
      transparent
    );
    animation: ${shimmer} 2s infinite;
  }
`;

const OfferIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  animation: ${bounce} 2s ease-in-out infinite;
`;

const OfferTitle = styled.h3`
  color: #d63031;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
`;

const OfferText = styled.p`
  color: #2d3436;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  font-weight: 500;
`;

const PromoCode = styled.div`
  background: rgba(255, 255, 255, 0.8);
  border: 2px dashed #d63031;
  border-radius: 10px;
  padding: 1rem;
  margin: 1rem 0;
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  font-weight: bold;
  color: #d63031;
`;

const ActionButtons = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
`;

const ActionButton = styled(motion.button)`
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
  
  &.primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
  }
  
  &.secondary {
    background: #f8f9fa;
    color: #495057;
    border: 2px solid #e9ecef;
    
    &:hover {
      background: #e9ecef;
      transform: translateY(-2px);
    }
  }
  
  &.success {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
    }
  }
`;

const NextSteps = styled.div`
  background: #e3f2fd;
  border-radius: 15px;
  padding: 1.5rem;
  margin: 2rem 0;
`;

const StepList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 1rem 0 0 0;
`;

const StepItem = styled.li`
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 0.75rem;
  
  &::before {
    content: '✓';
    background: #28a745;
    color: white;
    border-radius: 50%;
    width: 1.5rem;
    height: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: bold;
    flex-shrink: 0;
    margin-top: 0.1rem;
  }
`;

const ReferralSection = styled.div`
  background: linear-gradient(135deg, #a8e6cf, #88d8a3);
  border-radius: 15px;
  padding: 2rem;
  margin: 2rem 0;
  text-align: center;
`;

const BookingSuccessPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [confettiPieces, setConfettiPieces] = useState([]);
  
  // Get booking details from URL params or state
  const bookingId = searchParams.get('bookingId') || 'BS' + Date.now();
  const service = searchParams.get('service') || 'Premium Cleaning Service';
  const date = searchParams.get('date') || new Date().toLocaleDateString();
  const time = searchParams.get('time') || '10:00 AM';
  const address = searchParams.get('address') || 'Your specified location';
  
  useEffect(() => {
    // Create confetti pieces
    const pieces = [];
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff'];
    
    for (let i = 0; i < 50; i++) {
      pieces.push({
        id: i,
        color: colors[Math.floor(Math.random() * colors.length)],
        left: Math.random() * 100,
        delay: Math.random() * 3,
      });
    }
    
    setConfettiPieces(pieces);
    
    // Auto-scroll to top
    window.scrollTo(0, 0);
  }, []);

  return (
    <SuccessContainer>
      {/* Confetti Animation */}
      {confettiPieces.map(piece => (
        <ConfettiPiece
          key={piece.id}
          color={piece.color}
          left={piece.left}
          delay={piece.delay}
        />
      ))}

      <SuccessCard
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* Success Header */}
        <SuccessHeader>
          <SuccessIcon>
            <FaCheckCircle />
          </SuccessIcon>
          <SuccessTitle>🎉 Booking Confirmed! 🎉</SuccessTitle>
          <SuccessSubtitle>
            Your cleaning service has been successfully booked!
          </SuccessSubtitle>
        </SuccessHeader>

        <ContentSection>
          {/* Booking Details */}
          <BookingDetails>
            <h3 style={{ margin: '0 0 1rem 0', color: '#495057' }}>
              📋 Your Booking Details
            </h3>
            
            <DetailRow>
              <FaUser />
              <span>Booking ID: <strong>#{bookingId}</strong></span>
            </DetailRow>
            
            <DetailRow>
              <FaCheckCircle />
              <span>Service: <strong>{service}</strong></span>
            </DetailRow>
            
            <DetailRow>
              <FaCalendarAlt />
              <span>Date: <strong>{date}</strong></span>
            </DetailRow>
            
            <DetailRow>
              <FaClock />
              <span>Time: <strong>{time}</strong></span>
            </DetailRow>
            
            <DetailRow>
              <FaMapMarkerAlt />
              <span>Location: <strong>{address}</strong></span>
            </DetailRow>
          </BookingDetails>

          {/* Special Offer */}
          <OfferSection>
            <OfferIcon>
              <FaGift />
            </OfferIcon>
            <OfferTitle>🎁 Exclusive First-Time Bonus!</OfferTitle>
            <OfferText>
              Thank you for choosing our service! As a welcome gift, 
              enjoy <strong>20% OFF</strong> your next booking!
            </OfferText>
            <PromoCode>
              Use Code: <span style={{ color: '#d63031' }}>WELCOME20</span>
            </PromoCode>
            <p style={{ fontSize: '0.9rem', color: '#636e72', margin: 0 }}>
              *Valid for 30 days. Cannot be combined with other offers.
            </p>
          </OfferSection>

          {/* Next Steps */}
          <NextSteps>
            <h3 style={{ margin: '0 0 1rem 0', color: '#1565c0' }}>
              📱 What Happens Next?
            </h3>
            <StepList>
              <StepItem>
                <span>You'll receive a confirmation email within 5 minutes</span>
              </StepItem>
              <StepItem>
                <span>Our team will contact you 24 hours before your appointment</span>
              </StepItem>
              <StepItem>
                <span>Professional cleaners will arrive at your scheduled time</span>
              </StepItem>
              <StepItem>
                <span>Enjoy your sparkling clean space!</span>
              </StepItem>
            </StepList>
          </NextSteps>

          {/* Action Buttons */}
          <ActionButtons>
            <ActionButton
              onClick={() => navigate(`/booking/${bookingId}`)}
              className="primary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FaCalendarAlt />
              View My Booking
            </ActionButton>

            <ActionButton
              as={Link}
              to="/dashboard"
              className="secondary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FaHome />
              View Dashboard
            </ActionButton>
            
            <ActionButton
              onClick={() => navigate('/booking')}
              className="success"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FaArrowRight />
              Book Another Service
            </ActionButton>
            
            <ActionButton
              onClick={() => window.open('mailto:support@cleaningservice.com')}
              className="secondary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FaEnvelope />
              Contact Support
            </ActionButton>
            
            <ActionButton
              onClick={() => window.open('tel:+1234567890')}
              className="secondary"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <FaPhone />
              Call Us: (123) 456-7890
            </ActionButton>
          </ActionButtons>

          {/* Referral Section */}
          <ReferralSection>
            <h3 style={{ margin: '0 0 1rem 0', color: '#00695c' }}>
              💰 Earn $25 for Every Friend You Refer!
            </h3>
            <p style={{ margin: '0 0 1rem 0', color: '#004d40' }}>
              Love our service? Share it with friends and earn rewards!
            </p>
            <ActionButton
              onClick={() => navigate('/referrals')}
              className="success"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              style={{ margin: '0 auto', display: 'inline-flex' }}
            >
              <FaStar />
              Start Referring Friends
            </ActionButton>
          </ReferralSection>

          {/* Emergency Contact */}
          <div style={{ 
            textAlign: 'center', 
            padding: '1rem', 
            backgroundColor: '#fff3cd', 
            borderRadius: '10px',
            border: '1px solid #ffeaa7',
            marginTop: '2rem'
          }}>
            <p style={{ margin: 0, color: '#856404' }}>
              <strong>Need to change your appointment?</strong><br />
              Call us at <strong>(123) 456-7890</strong> or email <strong>support@cleaningservice.com</strong>
            </p>
          </div>
        </ContentSection>
      </SuccessCard>
    </SuccessContainer>
  );
};

export default BookingSuccessPage;
