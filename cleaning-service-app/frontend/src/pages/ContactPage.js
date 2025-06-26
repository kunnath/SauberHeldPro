import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { FaPhone, FaEnvelope, FaMapMarkerAlt, FaClock, FaComments, FaPaperPlane } from 'react-icons/fa';
import { useLanguage } from '../contexts/LanguageContext';

const ContactContainer = styled.div`
  padding: ${props => props.theme.spacing.xl} 0;
`;

const HeroSection = styled.section`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.xxl} 0;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 2rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.3rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
`;

const ContactContent = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${props => props.theme.spacing.xxl};
  margin: ${props => props.theme.spacing.xxl} 0;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
    gap: ${props => props.theme.spacing.xl};
  }
`;

const ContactInfo = styled.div`
  h2 {
    color: ${props => props.theme.colors.dark};
    margin-bottom: ${props => props.theme.spacing.lg};
    font-size: 2rem;
  }
`;

const ContactItem = styled.div`
  display: flex;
  align-items: flex-start;
  margin-bottom: ${props => props.theme.spacing.lg};
  padding: ${props => props.theme.spacing.lg};
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
`;

const ContactIcon = styled.div`
  font-size: 2rem;
  color: ${props => props.theme.colors.secondary};
  margin-right: ${props => props.theme.spacing.md};
  margin-top: 0.5rem;
`;

const ContactDetails = styled.div`
  h4 {
    color: ${props => props.theme.colors.dark};
    margin-bottom: ${props => props.theme.spacing.xs};
    font-size: 1.2rem;
  }
  
  p {
    color: ${props => props.theme.colors.gray};
    margin-bottom: ${props => props.theme.spacing.xs};
    line-height: 1.6;
  }
  
  a {
    color: ${props => props.theme.colors.secondary};
    text-decoration: none;
    font-weight: 600;
    
    &:hover {
      text-decoration: underline;
    }
  }
`;

const ContactForm = styled(motion.form)`
  background: white;
  padding: ${props => props.theme.spacing.xl};
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  
  h2 {
    color: ${props => props.theme.colors.dark};
    margin-bottom: ${props => props.theme.spacing.lg};
    font-size: 2rem;
  }
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  margin-bottom: ${props => props.theme.spacing.md};
  
  &.full-width {
    grid-column: 1 / -1;
  }
`;

const Label = styled.label`
  display: block;
  margin-bottom: ${props => props.theme.spacing.xs};
  font-weight: 600;
  color: ${props => props.theme.colors.dark};
`;

const Input = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.secondary};
    outline: none;
  }
  
  &.error {
    border-color: ${props => props.theme.colors.danger};
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 8px;
  font-size: 1rem;
  min-height: 120px;
  resize: vertical;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.secondary};
    outline: none;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.secondary};
    outline: none;
  }
`;

const SubmitButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  margin-top: ${props => props.theme.spacing.lg};
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.danger};
  font-size: 0.9rem;
  margin-top: ${props => props.theme.spacing.xs};
  display: block;
`;

const SuccessMessage = styled.div`
  background: ${props => props.theme.colors.success};
  color: white;
  padding: ${props => props.theme.spacing.md};
  border-radius: 8px;
  margin-bottom: ${props => props.theme.spacing.lg};
  text-align: center;
`;

const FAQSection = styled.section`
  background: ${props => props.theme.colors.light};
  padding: ${props => props.theme.spacing.xxl} 0;
  margin-top: ${props => props.theme.spacing.xxl};
`;

const FAQContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const FAQItem = styled.div`
  background: white;
  border-radius: 10px;
  margin-bottom: ${props => props.theme.spacing.md};
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const FAQQuestion = styled.button`
  width: 100%;
  padding: ${props => props.theme.spacing.lg};
  background: none;
  border: none;
  text-align: left;
  font-size: 1.1rem;
  font-weight: 600;
  color: ${props => props.theme.colors.dark};
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  &:hover {
    background: ${props => props.theme.colors.light};
  }
`;

const FAQAnswer = styled.div`
  padding: 0 ${props => props.theme.spacing.lg} ${props => props.theme.spacing.lg};
  color: ${props => props.theme.colors.gray};
  line-height: 1.6;
`;

const ContactPage = () => {
  const { t } = useLanguage();
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [expandedFAQ, setExpandedFAQ] = useState(null);
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm();

  const onSubmit = async (data) => {
    setSubmitting(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      setSubmitted(true);
      reset();
      setTimeout(() => setSubmitted(false), 5000);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const faqs = [
    {
      question: t('faq-1-question'),
      answer: t('faq-1-answer')
    },
    {
      question: t('faq-2-question'),
      answer: t('faq-2-answer')
    },
    {
      question: t('faq-3-question'),
      answer: t('faq-3-answer')
    },
    {
      question: t('faq-4-question'),
      answer: t('faq-4-answer')
    },
    {
      question: t('faq-5-question'),
      answer: t('faq-5-answer')
    },
    {
      question: t('faq-6-question'),
      answer: t('faq-6-answer')
    }
  ];

  const toggleFAQ = (index) => {
    setExpandedFAQ(expandedFAQ === index ? null : index);
  };

  return (
    <ContactContainer>
      <HeroSection>
        <div className="container">
          <Title>{t('contact-us')}</Title>
          <Subtitle>
            {t('contact-page-subtitle')}
          </Subtitle>
        </div>
      </HeroSection>

      <div className="container">
        <ContactContent>
          <ContactInfo>
            <h2>{t('get-in-touch')}</h2>
            
            <ContactItem>
              <ContactIcon><FaPhone /></ContactIcon>
              <ContactDetails>
                <h4>{t('phone-support')}</h4>
                <p>{t('phone-support-desc')}</p>
                <a href="tel:+4915772526898">+49 1577 2526898</a>
                <p>{t('contact-phone-info')}</p>
              </ContactDetails>
            </ContactItem>

            <ContactItem>
              <ContactIcon><FaEnvelope /></ContactIcon>
              <ContactDetails>
                <h4>{t('email-support')}</h4>
                <p>{t('email-support-desc')}</p>
                <a href="mailto:info@cleaningservice.de">info@cleaningservice.de</a>
                <p>{t('email-response-time')}</p>
              </ContactDetails>
            </ContactItem>

            <ContactItem>
              <ContactIcon><FaComments /></ContactIcon>
              <ContactDetails>
                <h4>{t('live-chat')}</h4>
                <p>{t('live-chat-desc')}</p>
                <p>{t('contact-chat-info')}</p>
                <p>{t('chat-instructions')}</p>
              </ContactDetails>
            </ContactItem>

            <ContactItem>
              <ContactIcon><FaMapMarkerAlt /></ContactIcon>
              <ContactDetails>
                <h4>{t('our-address')}</h4>
                <p>GRK Dienstleistungen</p>
                <p>Glockenblumenweg 131A</p>
                <p>12357 Berlin, Deutschland</p>
              </ContactDetails>
            </ContactItem>

            <ContactItem>
              <ContactIcon><FaMapMarkerAlt /></ContactIcon>
              <ContactDetails>
                <h4>{t('service-areas')}</h4>
                <p>{t('service-areas-desc')}</p>
                <a href="/areas">{t('view-all-areas')}</a>
              </ContactDetails>
            </ContactItem>

            <ContactItem>
              <ContactIcon><FaClock /></ContactIcon>
              <ContactDetails>
                <h4>{t('business-hours')}</h4>
                <p>{t('customer-support-hours')}</p>
                <p>{t('cleaning-service-hours')}</p>
                <p>{t('emergency-service')}</p>
              </ContactDetails>
            </ContactItem>
          </ContactInfo>

          <ContactForm
            onSubmit={handleSubmit(onSubmit)}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2>{t('contact-form-title')}</h2>
            
            {submitted && (
              <SuccessMessage>
                {t('message-sent')}
              </SuccessMessage>
            )}

            <FormGrid>
              <FormGroup>
                <Label>{t('first-name')} *</Label>
                <Input
                  {...register('firstName', { required: t('required-field') })}
                  className={errors.firstName ? 'error' : ''}
                />
                {errors.firstName && <ErrorMessage>{errors.firstName.message}</ErrorMessage>}
              </FormGroup>

              <FormGroup>
                <Label>{t('last-name')} *</Label>
                <Input
                  {...register('lastName', { required: t('required-field') })}
                  className={errors.lastName ? 'error' : ''}
                />
                {errors.lastName && <ErrorMessage>{errors.lastName.message}</ErrorMessage>}
              </FormGroup>

              <FormGroup>
                <Label>{t('email')} *</Label>
                <Input
                  type="email"
                  {...register('email', { 
                    required: t('required-field'),
                    pattern: {
                      value: /^\S+@\S+$/i,
                      message: t('invalid-email')
                    }
                  })}
                  className={errors.email ? 'error' : ''}
                />
                {errors.email && <ErrorMessage>{errors.email.message}</ErrorMessage>}
              </FormGroup>

              <FormGroup>
                <Label>{t('phone-number')}</Label>
                <Input
                  type="tel"
                  {...register('phone')}
                />
              </FormGroup>

              <FormGroup className="full-width">
                <Label>{t('inquiry-type')} *</Label>
                <Select
                  {...register('subject', { required: t('required-field') })}
                >
                  <option value="">{t('inquiry-type')}</option>
                  <option value="booking">{t('booking-inquiry')}</option>
                  <option value="general">{t('general-question')}</option>
                  <option value="feedback">{t('service-feedback')}</option>
                  <option value="technical">{t('technical-support')}</option>
                  <option value="partnership">{t('partnership')}</option>
                </Select>
                {errors.subject && <ErrorMessage>{errors.subject.message}</ErrorMessage>}
              </FormGroup>

              <FormGroup className="full-width">
                <Label>{t('message')} *</Label>
                <TextArea
                  {...register('message', { required: t('required-field') })}
                  placeholder={t('message-placeholder')}
                />
                {errors.message && <ErrorMessage>{errors.message.message}</ErrorMessage>}
              </FormGroup>
            </FormGrid>

            <SubmitButton
              type="submit"
              disabled={submitting}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {submitting ? t('sending') : (
                <>
                  <FaPaperPlane />
                  {t('send-message')}
                </>
              )}
            </SubmitButton>
          </ContactForm>
        </ContactContent>
      </div>

      <FAQSection>
        <div className="container">
          <FAQContainer>
            <h2 style={{ textAlign: 'center', marginBottom: '2rem', fontSize: '2.5rem', color: '#333' }}>
              {t('frequently-asked-questions')}
            </h2>
            
            {faqs.map((faq, index) => (
              <FAQItem key={index}>
                <FAQQuestion onClick={() => toggleFAQ(index)}>
                  {faq.question}
                  <span style={{ fontSize: '1.5rem' }}>
                    {expandedFAQ === index ? '−' : '+'}
                  </span>
                </FAQQuestion>
                {expandedFAQ === index && (
                  <FAQAnswer>{faq.answer}</FAQAnswer>
                )}
              </FAQItem>
            ))}
          </FAQContainer>
        </div>
      </FAQSection>
    </ContactContainer>
  );
};

export default ContactPage;
