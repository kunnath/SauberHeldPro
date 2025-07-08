import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaPhone, FaEnvelope, FaComments, FaBolt, FaShieldAlt, FaGlobe } from 'react-icons/fa';
import { useLanguage } from '../contexts/LanguageContext';

const Container = styled.div`
  width: 100%;
  overflow: hidden;
`;

const HeroSection = styled.section`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.xxl} 0;
  text-align: center;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><pattern id="grain" width="100" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100" height="20" fill="url(%23grain)"/></svg>');
    pointer-events: none;
  }
`;

const HeroContent = styled.div`
  position: relative;
  z-index: 1;
`;

const HeroTitle = styled(motion.h1)`
  font-size: 3.5rem;
  font-weight: bold;
  margin-bottom: ${props => props.theme.spacing.md};
  line-height: 1.2;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 2.5rem;
  }
`;

const HeroSubtitle = styled(motion.p)`
  font-size: 1.3rem;
  margin-bottom: ${props => props.theme.spacing.xl};
  opacity: 0.9;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 1.1rem;
  }
`;

const PostalSection = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: ${props => props.theme.spacing.xl};
  margin: ${props => props.theme.spacing.xl} auto;
  max-width: 600px;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const PostalTitle = styled.h2`
  font-size: 1.8rem;
  margin-bottom: ${props => props.theme.spacing.md};
  font-weight: 600;
`;

const PostalForm = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.sm};
  margin-top: ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
  }
`;

const PostalInput = styled.input`
  flex: 1;
  padding: ${props => props.theme.spacing.md};
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  
  &::placeholder {
    color: #999;
  }
`;

const BookButton = styled(motion.button)`
  background: ${props => props.theme.colors.success};
  color: white;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  min-width: 150px;
  
  &:hover {
    background: #218838;
  }
`;

const HowItWorksSection = styled.section`
  background: ${props => props.theme.colors.light};
  padding: ${props => props.theme.spacing.xxl} 0;
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: ${props => props.theme.spacing.xl};
  color: ${props => props.theme.colors.dark};
`;

const StepsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-top: ${props => props.theme.spacing.xl};
`;

const StepCard = styled(motion.div)`
  background: white;
  padding: ${props => props.theme.spacing.xl};
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const StepNumber = styled.div`
  background: ${props => props.theme.colors.secondary};
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto ${props => props.theme.spacing.md} auto;
`;

const StepTitle = styled.h3`
  font-size: 1.4rem;
  margin-bottom: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.dark};
`;

const StepDescription = styled.p`
  color: ${props => props.theme.colors.gray};
  line-height: 1.6;
`;

const ServicesSection = styled.section`
  padding: ${props => props.theme.spacing.xxl} 0;
`;

const ServicesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-top: ${props => props.theme.spacing.xl};
`;

const ServiceCard = styled(motion.div)`
  background: white;
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 15px;
  padding: ${props => props.theme.spacing.xl};
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  }
`;

const ServiceTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.dark};
`;

const ServicePrice = styled.div`
  color: ${props => props.theme.colors.secondary};
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: ${props => props.theme.spacing.md};
`;

const ServiceFeatures = styled.ul`
  list-style: none;
  margin-bottom: ${props => props.theme.spacing.lg};
  
  li {
    padding: ${props => props.theme.spacing.xs} 0;
    border-bottom: 1px solid ${props => props.theme.colors.light};
    color: ${props => props.theme.colors.gray};
    position: relative;
    padding-left: 1.5rem;
    
    &::before {
      content: '✓';
      color: ${props => props.theme.colors.success};
      font-weight: bold;
      position: absolute;
      left: 0;
    }
  }
`;

const ContactSection = styled.section`
  background: ${props => props.theme.colors.primary};
  color: white;
  padding: ${props => props.theme.spacing.xxl} 0;
  text-align: center;
`;

const ContactGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-top: ${props => props.theme.spacing.xl};
`;

const ContactItem = styled.div`
  text-align: center;
`;

const ContactIcon = styled.div`
  font-size: 3rem;
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.light};
`;

const ContactTitle = styled.h4`
  font-size: 1.2rem;
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const ContactInfo = styled.div`
  font-size: 1.1rem;
  opacity: 0.9;
`;

const FeaturesSection = styled.section`
  background: ${props => props.theme.colors.light};
  padding: ${props => props.theme.spacing.xxl} 0;
`;

const TestimonialsSection = styled.section`
  padding: ${props => props.theme.spacing.xxl} 0;
`;

const TestimonialsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-top: ${props => props.theme.spacing.xl};
`;

const TestimonialCard = styled(motion.div)`
  background: white;
  padding: ${props => props.theme.spacing.xl};
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
`;

const Stars = styled.div`
  color: ${props => props.theme.colors.warning};
  font-size: 1.2rem;
  margin-bottom: ${props => props.theme.spacing.md};
`;

const TestimonialText = styled.p`
  font-style: italic;
  margin-bottom: ${props => props.theme.spacing.md};
  line-height: 1.6;
  color: ${props => props.theme.colors.gray};
`;

const TestimonialAuthor = styled.div`
  font-weight: 600;
  color: ${props => props.theme.colors.dark};
`;

const HeroBackground = styled.div`
  position: relative;
  z-index: 1;
`;

const HomePage = () => {
  const { t } = useLanguage();
  const [postalCode, setPostalCode] = useState('');
  const navigate = useNavigate();

  const handleBookNow = () => {
    if (postalCode.trim()) {
      navigate('/booking', { state: { postalCode } });
    } else {
      navigate('/booking');
    }
  };

  const steps = [
    {
      number: 1,
      title: t('step-1-title'),
      description: t('step-1-desc')
    },
    {
      number: 2,
      title: t('step-2-title'),
      description: t('step-2-desc')
    },
    {
      number: 3,
      title: t('step-3-title'),
      description: t('step-3-desc')
    }
  ];

  const services = [
    {
      title: t('basic-cleaning'),
      price: t('basic-cleaning-price'),
      description: t('basic-cleaning-desc'),
      features: [
        t('basic-feature-1'),
        t('basic-feature-2'),
        t('basic-feature-3'),
        t('basic-feature-4'),
        t('basic-feature-5')
      ]
    },
    {
      title: t('deep-cleaning'),
      price: t('deep-cleaning-price'),
      description: t('deep-cleaning-desc'),
      features: [
        t('deep-feature-1'),
        t('deep-feature-2'),
        t('deep-feature-3'),
        t('deep-feature-4'),
        t('deep-feature-5')
      ]
    },
    {
      title: t('office-cleaning'),
      price: t('office-cleaning-price'),
      description: t('office-cleaning-desc'),
      features: [
        t('office-feature-1'),
        t('office-feature-2'),
        t('office-feature-3'),
        t('office-feature-4'),
        t('office-feature-5')
      ]
    }
  ];

  const testimonials = [
    {
      text: t('testimonial-1'),
      author: t('testimonial-1-author'),
      rating: 5
    },
    {
      text: t('testimonial-2'),
      author: t('testimonial-2-author'),
      rating: 5
    },
    {
      text: t('testimonial-3'),
      author: t('testimonial-3-author'),
      rating: 5
    }
  ];

  return (
    <Container>
      <HeroSection>
        <HeroBackground>
          <HeroContent>
            <HeroTitle
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              {t('hero-title')}
            </HeroTitle>
            <HeroSubtitle
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              {t('hero-subtitle')}
            </HeroSubtitle>
            
            <PostalSection
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <PostalTitle>{t('postal-code-title')}</PostalTitle>
              <PostalForm>
                <PostalInput
                  type="text"
                  placeholder={t('postal-code-placeholder')}
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                />
                <BookButton
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleBookNow}
                >
                  {t('book-now')}
                </BookButton>
              </PostalForm>
            </PostalSection>
          </HeroContent>
        </HeroBackground>
      </HeroSection>

      <HowItWorksSection>
        <div className="container">
          <SectionTitle>{t('how-it-works')}</SectionTitle>
          <StepsContainer>
            {steps.map((step, index) => (
              <StepCard
                key={step.number}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <StepNumber>{step.number}</StepNumber>
                <StepTitle>{step.title}</StepTitle>
                <StepDescription>{step.description}</StepDescription>
              </StepCard>
            ))}
          </StepsContainer>
        </div>
      </HowItWorksSection>

      <ServicesSection>
        <div className="container">
          <SectionTitle>{t('services-title')}</SectionTitle>
          <ServicesGrid>
            {services.map((service, index) => (
              <ServiceCard
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.02 }}
              >
                <ServiceTitle>{service.title}</ServiceTitle>
                <ServicePrice>{service.price}</ServicePrice>
                <p style={{ color: '#666', marginBottom: '1.5rem' }}>{service.description}</p>
                <ServiceFeatures>
                  {service.features.map((feature, idx) => (
                    <li key={idx}>{feature}</li>
                  ))}
                </ServiceFeatures>
              </ServiceCard>
            ))}
          </ServicesGrid>
        </div>
      </ServicesSection>

      <ContactSection>
        <div className="container">
          <SectionTitle style={{ color: 'white' }}>{t('contact-section-title')}</SectionTitle>
          <h3 style={{ marginBottom: '2rem', fontWeight: 400 }}>{t('contact-section-subtitle')}</h3>
          <ContactGrid>
            <ContactItem>
              <ContactIcon><FaPhone /></ContactIcon>
              <ContactTitle>{t('contact-phone-title')}</ContactTitle>
              <ContactInfo>{t('contact-phone-info')}</ContactInfo>
            </ContactItem>
            <ContactItem>
              <ContactIcon><FaEnvelope /></ContactIcon>
              <ContactTitle>{t('contact-email-title')}</ContactTitle>
              <ContactInfo>{t('contact-email-info')}</ContactInfo>
            </ContactItem>
            <ContactItem>
              <ContactIcon><FaComments /></ContactIcon>
              <ContactTitle>{t('contact-chat-title')}</ContactTitle>
              <ContactInfo>{t('contact-chat-info')}</ContactInfo>
            </ContactItem>
          </ContactGrid>
        </div>
      </ContactSection>

      <FeaturesSection>
        <div className="container">
          <SectionTitle>{t('features-title')}</SectionTitle>
          <StepsContainer>
            <StepCard
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <ContactIcon style={{ color: '#2E86AB' }}><FaBolt /></ContactIcon>
              <StepTitle>{t('easy-booking-title')}</StepTitle>
              <StepDescription>{t('easy-booking-desc')}</StepDescription>
            </StepCard>
            <StepCard
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <ContactIcon style={{ color: '#2E86AB' }}><FaShieldAlt /></ContactIcon>
              <StepTitle>{t('background-checked-title')}</StepTitle>
              <StepDescription>{t('background-checked-desc')}</StepDescription>
            </StepCard>
            <StepCard
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              viewport={{ once: true }}
            >
              <ContactIcon style={{ color: '#2E86AB' }}><FaGlobe /></ContactIcon>
              <StepTitle>{t('english-speaking-title')}</StepTitle>
              <StepDescription>{t('english-speaking-desc')}</StepDescription>
            </StepCard>
          </StepsContainer>
        </div>
      </FeaturesSection>

      <TestimonialsSection>
        <div className="container">
          <SectionTitle>{t('testimonials-title')}</SectionTitle>
          <p style={{ textAlign: 'center', color: '#666', marginBottom: '2rem' }}>{t('testimonials-subtitle')}</p>
          <TestimonialsGrid>
            {testimonials.map((testimonial, index) => (
              <TestimonialCard
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
              >
                <Stars>{'⭐'.repeat(testimonial.rating)}</Stars>
                <TestimonialText>"{testimonial.text}"</TestimonialText>
                <TestimonialAuthor>- {testimonial.author}</TestimonialAuthor>
              </TestimonialCard>
            ))}
          </TestimonialsGrid>
        </div>
      </TestimonialsSection>
    </Container>
  );
};

export default HomePage;
