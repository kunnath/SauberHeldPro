import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FaCheck, FaArrowLeft, FaArrowRight, FaCalendarAlt, FaClock, FaMapMarkerAlt, FaUser, FaEnvelope, FaPhone } from 'react-icons/fa';
import { useLanguage } from '../contexts/LanguageContext';
import axios from 'axios';

const BookingContainer = styled.div`
  padding: ${props => props.theme.spacing.xl} 0;
  min-height: 80vh;
`;

const BookingHeader = styled.div`
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

const ProgressBar = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const ProgressStep = styled.div`
  display: flex;
  align-items: center;
  margin: 0 ${props => props.theme.spacing.sm};
`;

const StepCircle = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${props => props.active ? props.theme.colors.secondary : props.theme.colors.lightGray};
  color: ${props => props.active ? 'white' : props.theme.colors.gray};
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: ${props => props.theme.spacing.xs};
`;

const StepLabel = styled.span`
  color: ${props => props.active ? props.theme.colors.dark : props.theme.colors.gray};
  font-weight: ${props => props.active ? 600 : 400};
`;

const BookingForm = styled.div`
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const StepContent = styled(motion.div)`
  padding: ${props => props.theme.spacing.xl};
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${props => props.theme.spacing.xl};
`;

const FormSection = styled.div`
  h3 {
    color: ${props => props.theme.colors.dark};
    margin-bottom: ${props => props.theme.spacing.md};
    font-size: 1.3rem;
  }
`;

const ServiceGrid = styled.div`
  display: grid;
  gap: ${props => props.theme.spacing.md};
`;

const ServiceOption = styled.div`
  border: 2px solid ${props => props.selected ? props.theme.colors.secondary : props.theme.colors.lightGray};
  border-radius: 10px;
  padding: ${props => props.theme.spacing.md};
  cursor: pointer;
  transition: all 0.3s ease;
  background: ${props => props.selected ? 'rgba(102, 126, 234, 0.1)' : 'white'};
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
  }
`;

const ServiceTitle = styled.h4`
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const ServicePrice = styled.div`
  color: ${props => props.theme.colors.secondary};
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const ServiceDescription = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 0.9rem;
`;

const FormGroup = styled.div`
  margin-bottom: ${props => props.theme.spacing.md};
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
  min-height: 100px;
  resize: vertical;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.secondary};
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
  }
`;

const TimeSlotGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: ${props => props.theme.spacing.sm};
  margin-top: ${props => props.theme.spacing.md};
`;

const TimeSlot = styled.button`
  padding: ${props => props.theme.spacing.sm};
  border: 2px solid ${props => props.selected ? props.theme.colors.secondary : props.theme.colors.lightGray};
  border-radius: 8px;
  background: ${props => props.selected ? props.theme.colors.secondary : 'white'};
  color: ${props => props.selected ? 'white' : props.theme.colors.dark};
  font-weight: 600;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) {
    border-color: ${props => props.theme.colors.secondary};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: ${props => props.theme.spacing.xl};
  padding-top: ${props => props.theme.spacing.lg};
  border-top: 1px solid ${props => props.theme.colors.lightGray};
`;

const Button = styled(motion.button)`
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  
  &.primary {
    background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
    color: white;
  }
  
  &.secondary {
    background: ${props => props.theme.colors.lightGray};
    color: ${props => props.theme.colors.dark};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const SummaryCard = styled.div`
  background: ${props => props.theme.colors.light};
  border-radius: 10px;
  padding: ${props => props.theme.spacing.lg};
  margin-top: ${props => props.theme.spacing.lg};
`;

const SummaryTitle = styled.h4`
  color: ${props => props.theme.colors.dark};
  margin-bottom: ${props => props.theme.spacing.md};
`;

const SummaryItem = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: ${props => props.theme.spacing.xs};
  
  strong {
    color: ${props => props.theme.colors.secondary};
  }
`;

const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.danger};
  font-size: 0.9rem;
  margin-top: ${props => props.theme.spacing.xs};
  display: block;
`;

const BookingPage = () => {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm();
  
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedService, setSelectedService] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTime, setSelectedTime] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [postalCode, setPostalCode] = useState(location.state?.postalCode || '');

  const services = [
    {
      id: 1,
      name: t('basic-cleaning-booking'),
      price: 28.90,
      duration: 2,
      description: t('basic-cleaning-booking-desc')
    },
    {
      id: 2,
      name: t('deep-cleaning-booking'),
      price: 45.00,
      duration: 4,
      description: t('deep-cleaning-booking-desc')
    },
    {
      id: 3,
      name: t('office-cleaning-booking'),
      price: 35.00,
      duration: 3,
      description: t('office-cleaning-booking-desc')
    }
  ];

  const timeSlots = [
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00'
  ];

  useEffect(() => {
    if (selectedDate) {
      // Simulate API call to get available slots
      const slots = timeSlots.map(time => ({
        time,
        available: Math.random() > 0.3 // 70% chance of being available
      }));
      setAvailableSlots(slots);
    }
  }, [selectedDate]);

  const handleServiceSelect = (service) => {
    setSelectedService(service);
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const bookingData = {
        ...data,
        service: selectedService,
        date: selectedDate,
        time: selectedTime,
        postalCode,
        totalPrice: selectedService?.price * selectedService?.duration
      };
      
      // Simulate API call (replace with actual API call)
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Generate booking ID
      const bookingId = 'BS' + Date.now();
      
      // Create success page URL with booking details
      const successUrl = new URLSearchParams({
        bookingId: bookingId,
        service: selectedService?.name || 'Cleaning Service',
        date: selectedDate?.toLocaleDateString() || new Date().toLocaleDateString(),
        time: selectedTime || '10:00 AM',
        address: data.address || 'Your specified location'
      });
      
      // Redirect to success page with booking details
      navigate(`/booking/success?${successUrl.toString()}`);
    } catch (error) {
      console.error('Booking failed:', error);
      // You can add error handling here
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <StepContent
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.3 }}
    >
      <FormGrid>
        <FormSection>
          <h3>{t('choose-service-type')}</h3>
          <ServiceGrid>
            {services.map(service => (
              <ServiceOption
                key={service.id}
                selected={selectedService?.id === service.id}
                onClick={() => handleServiceSelect(service)}
              >
                <ServiceTitle>{service.name}</ServiceTitle>
                <ServicePrice>€{service.price}{t('per-hour')}</ServicePrice>
                <ServiceDescription>{service.description}</ServiceDescription>
              </ServiceOption>
            ))}
          </ServiceGrid>
        </FormSection>
        
        <FormSection>
          <h3>{t('contact-details')}</h3>
          <FormGroup>
            <Label>{t('postal-code')}</Label>
            <Input
              type="text"
              value={postalCode}
              onChange={(e) => setPostalCode(e.target.value)}
              placeholder={t('postal-code-placeholder')}
            />
          </FormGroup>
          
          <FormGroup>
            <Label>{t('duration')}</Label>
            <Select>
              <option value="2">2 {t('hours')}</option>
              <option value="3">3 {t('hours')}</option>
              <option value="4">4 {t('hours')}</option>
              <option value="5">5 {t('hours')}</option>
              <option value="6">6+ {t('hours')}</option>
            </Select>
          </FormGroup>
          
          {selectedService && (
            <SummaryCard>
              <SummaryTitle>{t('booking-summary-title')}</SummaryTitle>
              <SummaryItem>
                <span>{t('service')}:</span>
                <span>{selectedService.name}</span>
              </SummaryItem>
              <SummaryItem>
                <span>Price per hour:</span>
                <span>€{selectedService.price}</span>
              </SummaryItem>
              <SummaryItem>
                <span>Estimated duration:</span>
                <span>{selectedService.duration} hours</span>
              </SummaryItem>
              <SummaryItem>
                <span><strong>Total estimate:</strong></span>
                <strong>€{(selectedService.price * selectedService.duration).toFixed(2)}</strong>
              </SummaryItem>
            </SummaryCard>
          )}
        </FormSection>
      </FormGrid>
    </StepContent>
  );

  const renderStep2 = () => (
    <StepContent
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.3 }}
    >
      <FormGrid>
        <FormSection>
          <h3><FaCalendarAlt /> {t('select-date-time')}</h3>
          
          <FormGroup>
            <Label>{t('preferred-date')}</Label>
            <DatePicker
              selected={selectedDate}
              onChange={setSelectedDate}
              minDate={new Date()}
              inline
              calendarClassName="custom-datepicker"
            />
          </FormGroup>
        </FormSection>
        
        <FormSection>
          <h3><FaClock /> {t('available-time-slots')}</h3>
          
          {selectedDate ? (
            <TimeSlotGrid>
              {availableSlots.map(slot => (
                <TimeSlot
                  key={slot.time}
                  selected={selectedTime === slot.time}
                  disabled={!slot.available}
                  onClick={() => slot.available && setSelectedTime(slot.time)}
                >
                  {slot.time}
                </TimeSlot>
              ))}
            </TimeSlotGrid>
          ) : (
            <p style={{ color: '#666', marginTop: '1rem' }}>
              {t('select-date-to-view-slots')}
            </p>
          )}
          
          {selectedDate && selectedTime && (
            <SummaryCard>
              <SummaryTitle>{t('selected-schedule')}</SummaryTitle>
              <SummaryItem>
                <span>{t('date')}:</span>
                <span>{selectedDate.toLocaleDateString()}</span>
              </SummaryItem>
              <SummaryItem>
                <span>{t('time')}:</span>
                <span>{selectedTime}</span>
              </SummaryItem>
              <SummaryItem>
                <span>{t('duration')}:</span>
                <span>{selectedService?.duration} hours</span>
              </SummaryItem>
            </SummaryCard>
          )}
        </FormSection>
      </FormGrid>
    </StepContent>
  );

  const renderStep3 = () => (
    <StepContent
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.3 }}
    >
      <form onSubmit={handleSubmit(onSubmit)}>
        <FormGrid>
          <FormSection>
            <h3><FaUser /> {t('contact-information')}</h3>
            
            <FormGroup>
              <Label>{t('first-name')} *</Label>
              <Input
                {...register('firstName', { required: 'First name is required' })}
                className={errors.firstName ? 'error' : ''}
              />
              {errors.firstName && <ErrorMessage>{errors.firstName.message}</ErrorMessage>}
            </FormGroup>
            
            <FormGroup>
              <Label>{t('last-name')} *</Label>
              <Input
                {...register('lastName', { required: 'Last name is required' })}
                className={errors.lastName ? 'error' : ''}
              />
              {errors.lastName && <ErrorMessage>{errors.lastName.message}</ErrorMessage>}
            </FormGroup>
            
            <FormGroup>
              <Label>{t('email')} *</Label>
              <Input
                type="email"
                {...register('email', { 
                  required: 'Email is required',
                  pattern: {
                    value: /^\S+@\S+$/i,
                    message: 'Invalid email address'
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
          </FormSection>
          
          <FormSection>
            <h3><FaMapMarkerAlt /> {t('address-details')}</h3>
            
            <FormGroup>
              <Label>{t('full-address')} *</Label>
              <TextArea
                {...register('address', { required: 'Address is required' })}
                placeholder={t('address-placeholder')}
                className={errors.address ? 'error' : ''}
              />
              {errors.address && <ErrorMessage>{errors.address.message}</ErrorMessage>}
            </FormGroup>
            
            <FormGroup>
              <Label>{t('special-instructions')}</Label>
              <TextArea
                {...register('specialInstructions')}
                placeholder={t('special-instructions-placeholder')}
              />
            </FormGroup>
            
            <SummaryCard>
              <SummaryTitle>{t('booking-summary')}</SummaryTitle>
              <SummaryItem>
                <span>{t('service')}:</span>
                <span>{selectedService?.name}</span>
              </SummaryItem>
              <SummaryItem>
                <span>{t('date-time')}:</span>
                <span>{selectedDate?.toLocaleDateString()} at {selectedTime}</span>
              </SummaryItem>
              <SummaryItem>
                <span>{t('duration')}:</span>
                <span>{selectedService?.duration} hours</span>
              </SummaryItem>
              <SummaryItem>
                <span>{t('location')}:</span>
                <span>{postalCode}</span>
              </SummaryItem>
              <SummaryItem>
                <span><strong>{t('total-price')}:</strong></span>
                <strong>€{selectedService ? (selectedService.price * selectedService.duration).toFixed(2) : '0.00'}</strong>
              </SummaryItem>
              <SummaryItem>
                <span><strong>{t('deposit-required')}:</strong></span>
                <strong>€{selectedService?.price.toFixed(2) || '0.00'}</strong>
              </SummaryItem>
            </SummaryCard>
          </FormSection>
        </FormGrid>
      </form>
    </StepContent>
  );

  const steps = [
    { number: 1, label: t('step-1') },
    { number: 2, label: t('step-2') },
    { number: 3, label: t('step-3') },
  ];

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return selectedService && postalCode;
      case 2:
        return selectedDate && selectedTime;
      case 3:
        return true;
      default:
        return false;
    }
  };

  return (
    <BookingContainer>
      <div className="container">
        <BookingHeader>
          <Title>{t('booking-title')}</Title>
          <Subtitle>{t('booking-subtitle')}</Subtitle>
        </BookingHeader>
        
        <ProgressBar>
          {steps.map((step) => (
            <ProgressStep key={step.number}>
              <StepCircle active={currentStep >= step.number}>
                {currentStep > step.number ? <FaCheck /> : step.number}
              </StepCircle>
              <StepLabel active={currentStep >= step.number}>
                {step.label}
              </StepLabel>
            </ProgressStep>
          ))}
        </ProgressBar>
        
        <BookingForm>
          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}
          
          <ButtonGroup>
            <Button
              type="button"
              className="secondary"
              onClick={handlePrevious}
              disabled={currentStep === 1}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaArrowLeft />
              {t('go-back')}
            </Button>
            
            {currentStep < 3 ? (
              <Button
                type="button"
                className="primary"
                onClick={handleNext}
                disabled={!canProceed()}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {t('continue')}
                <FaArrowRight />
              </Button>
            ) : (
              <Button
                type="submit"
                className="primary"
                onClick={handleSubmit(onSubmit)}
                disabled={loading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {loading ? t('processing') : t('book-service-now')}
              </Button>
            )}
          </ButtonGroup>
        </BookingForm>
      </div>
    </BookingContainer>
  );
};

export default BookingPage;
