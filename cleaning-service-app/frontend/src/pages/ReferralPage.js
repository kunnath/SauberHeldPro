import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FaUsers, FaDollarSign, FaGift, FaArrowLeft } from 'react-icons/fa';

const ReferralContainer = styled.div`
  min-height: 80vh;
  padding: ${props => props.theme.spacing.xl} ${props => props.theme.spacing.md};
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
`;

const ReferralCard = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  padding: ${props => props.theme.spacing.xxl};
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const Title = styled.h1`
  font-size: 2.5rem;
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: ${props => props.theme.colors.gray};
`;

const ComingSoon = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl};
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 15px;
  color: white;
  margin: ${props => props.theme.spacing.xl} 0;
`;

const BackButton = styled(Link)`
  display: inline-flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.primary};
  text-decoration: none;
  font-weight: 600;
  margin-bottom: ${props => props.theme.spacing.lg};
  
  &:hover {
    text-decoration: underline;
  }
`;

const ReferralPage = () => {
  return (
    <ReferralContainer>
      <ReferralCard
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <BackButton to="/dashboard">
          <FaArrowLeft />
          Back to Dashboard
        </BackButton>
        
        <Header>
          <Title>
            <FaUsers style={{ marginRight: '1rem', color: '#667eea' }} />
            Referral Program
          </Title>
          <Subtitle>Share the love and earn rewards!</Subtitle>
        </Header>

        <ComingSoon>
          <h2 style={{ margin: '0 0 1rem 0' }}>
            <FaGift style={{ marginRight: '0.5rem' }} />
            Coming Soon!
          </h2>
          <p style={{ fontSize: '1.1rem', margin: 0 }}>
            Our referral program is currently under development. 
            Soon you'll be able to earn <strong>$25</strong> for every friend who books our service!
          </p>
        </ComingSoon>

        <div style={{ 
          textAlign: 'center',
          padding: '2rem',
          backgroundColor: '#f8f9fa',
          borderRadius: '15px',
          marginTop: '2rem'
        }}>
          <h3 style={{ color: '#495057', marginBottom: '1rem' }}>
            Want to be notified when it launches?
          </h3>
          <p style={{ color: '#6c757d', margin: 0 }}>
            Contact us at <strong>support@cleaningservice.com</strong> and we'll let you know!
          </p>
        </div>
      </ReferralCard>
    </ReferralContainer>
  );
};

export default ReferralPage;
