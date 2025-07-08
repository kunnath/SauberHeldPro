import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { FaUser, FaLock, FaEye, FaEyeSlash, FaUserPlus, FaEnvelope, FaPhone } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

const LoginContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${props => props.theme.spacing.md};
  background: linear-gradient(135deg, ${props => props.theme.colors.light} 0%, rgba(46, 134, 171, 0.1) 100%);
  
  @media (max-width: 768px) {
    padding: ${props => props.theme.spacing.sm};
    min-height: 100vh;
  }
  
  @media (max-width: 480px) {
    padding: ${props => props.theme.spacing.xs};
  }
`;

const LoginCard = styled(motion.div)`
  background: white;
  border-radius: 20px;
  padding: ${props => props.theme.spacing.xxl};
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  
  @media (max-width: 768px) {
    padding: ${props => props.theme.spacing.xl};
    border-radius: 15px;
    margin: ${props => props.theme.spacing.sm};
  }
  
  @media (max-width: 480px) {
    padding: ${props => props.theme.spacing.lg};
    border-radius: 12px;
    margin: ${props => props.theme.spacing.xs};
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }
`;

const LoginHeader = styled.div`
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.xl};
  
  @media (max-width: 480px) {
    margin-bottom: ${props => props.theme.spacing.lg};
  }
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.dark};
  font-size: 2.5rem;
  margin-bottom: ${props => props.theme.spacing.sm};
  
  @media (max-width: 768px) {
    font-size: 2.2rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.8rem;
  }
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 1.1rem;
  
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

const TabContainer = styled.div`
  display: flex;
  margin-bottom: ${props => props.theme.spacing.xl};
  border-radius: 10px;
  background: ${props => props.theme.colors.light};
  padding: 4px;
  
  @media (max-width: 480px) {
    margin-bottom: ${props => props.theme.spacing.lg};
    border-radius: 8px;
  }
`;

const Tab = styled.button`
  flex: 1;
  padding: ${props => props.theme.spacing.sm};
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  background: ${props => props.active ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.active ? 'white' : props.theme.colors.gray};
  font-size: 1rem;
  
  @media (max-width: 480px) {
    padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
    font-size: 0.9rem;
  }
  
  &:hover {
    background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.lightGray};
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: 480px) {
    gap: ${props => props.theme.spacing.sm};
  }
`;

const InputGroup = styled.div`
  position: relative;
  width: 100%;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 16px 12px 48px;
  border: 2px solid ${props => props.className === 'error' ? props.theme.colors.danger : '#e9ecef'};
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
  background: white;
  
  @media (max-width: 480px) {
    padding: 10px 12px 10px 40px;
    font-size: 16px; /* Prevents zoom on iOS */
    border-radius: 8px;
  }
  
  &:focus {
    outline: none;
    border-color: ${props => props.className === 'error' ? props.theme.colors.danger : props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => 
      props.className === 'error' 
        ? 'rgba(220, 53, 69, 0.1)' 
        : 'rgba(46, 134, 171, 0.1)'
    };
  }
  
  &::placeholder {
    color: #666;
  }
`;

const InputIcon = styled.div`
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
  z-index: 1;
  
  @media (max-width: 480px) {
    left: 12px;
  }
`;

const PasswordToggle = styled.button`
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: ${props => props.theme.colors.gray};
  cursor: pointer;
  padding: 0.5rem;
  z-index: 3;
  pointer-events: auto;
  
  &:hover {
    color: ${props => props.theme.colors.primary};
  }
`;

const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.danger};
  font-size: 0.85rem;
  margin-top: 0.25rem;
`;

const SubmitButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.primary} 0%, ${props => props.theme.colors.secondary} 100%);
  color: white;
  padding: ${props => props.theme.spacing.sm};
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: ${props => props.theme.spacing.md};
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 50px;
  width: 100%;
  cursor: pointer;
  
  @media (max-width: 480px) {
    padding: ${props => props.theme.spacing.xs};
    font-size: 1rem;
    min-height: 45px;
    border-radius: 8px;
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  &:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  &:not(:disabled):active {
    transform: translateY(0);
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ErrorAlert = styled(motion.div)`
  background: ${props => props.theme.colors.danger};
  color: white;
  padding: ${props => props.theme.spacing.sm};
  border-radius: 10px;
  margin-bottom: ${props => props.theme.spacing.md};
  text-align: center;
  font-weight: 500;
  font-size: 0.95rem;
  width: 100%;
`;

const SuccessAlert = styled(motion.div)`
  background: ${props => props.theme.colors.success};
  color: white;
  padding: ${props => props.theme.spacing.sm};
  border-radius: 10px;
  margin-bottom: ${props => props.theme.spacing.md};
  text-align: center;
  font-weight: 500;
  font-size: 0.95rem;
  width: 100%;
`;

const LoginPage = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const { login, register: authRegister, isAuthenticated, isLoading, error, clearError, user } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Separate form instances for login and register
  const loginForm = useForm({
    mode: 'onChange'
  });
  
  const registerForm = useForm({
    mode: 'onChange'
  });

  const from = location.state?.from?.pathname || '/dashboard';

  useEffect(() => {
    console.log('🔍 Auth state changed:', { isAuthenticated, user: !!user });
    if (isAuthenticated) {
      console.log('✅ User is authenticated, redirecting to:', from);
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from, user]);

  useEffect(() => {
    clearError();
    // Reset both forms when switching tabs
    if (activeTab === 'login') {
      registerForm.reset();
    } else {
      loginForm.reset();
    }
  }, [activeTab, clearError]);

  const onLoginSubmit = async (data) => {
    console.log('🚀 Login form submitted with:', data);
    try {
      const result = await login(data);
      console.log('✅ Login result:', result);
    } catch (err) {
      console.error('❌ Login error:', err);
      // Error is handled by the auth context
    }
  };

  const onRegisterSubmit = async (data) => {
    clearError();
    try {
      const result = await authRegister(data);
      console.log('✅ Registration successful:', result);
      // Show success message and optionally switch to login tab
      setTimeout(() => {
        setActiveTab('login');
        loginForm.setValue('email', data.email);
      }, 1000);
    } catch (err) {
      console.error('❌ Registration error:', err);
      // Set form-level error
      registerForm.setError('root.serverError', {
        type: 'server',
        message: err.message
      });

      // If we have validation details, set field-specific errors
      if (err.details) {
        err.details.forEach(detail => {
          const field = detail.param;
          if (field) {
            registerForm.setError(field, {
              type: 'server',
              message: detail.msg
            });
          }
        });
      }
    }
  };

  const password = registerForm.watch('password');

  return (
    <LoginContainer>
      <LoginCard
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <LoginHeader>
          <Title>{t('welcome-back')}</Title>
          <Subtitle>
            {activeTab === 'login' 
              ? t('sign-in-account') 
              : t('create-account')
            }
          </Subtitle>
        </LoginHeader>

        <TabContainer>
          <Tab 
            active={activeTab === 'login'} 
            onClick={() => setActiveTab('login')}
            type="button"
          >
            {t('sign-in')}
          </Tab>
          <Tab 
            active={activeTab === 'register'} 
            onClick={() => setActiveTab('register')}
            type="button"
          >
            {t('register')}
          </Tab>
        </TabContainer>

        {error && (
          <ErrorAlert
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {error}
          </ErrorAlert>
        )}

        {activeTab === 'login' ? (
          <Form onSubmit={loginForm.handleSubmit(onLoginSubmit)}>
            <InputGroup>
              <InputIcon>
                <FaEnvelope />
              </InputIcon>
              <Input
                type="email"
                placeholder={t('email-address')}
                autoComplete="email"
                {...loginForm.register('email', {
                  required: t('required-field'),
                  pattern: {
                    value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: t('invalid-email')
                  }
                })}
              />
              {loginForm.formState.errors.email && <ErrorMessage>{loginForm.formState.errors.email.message}</ErrorMessage>}
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaLock />
              </InputIcon>
              <Input
                type={showPassword ? 'text' : 'password'}
                placeholder={t('password')}
                autoComplete="current-password"
                {...loginForm.register('password', {
                  required: t('required-field'),
                  minLength: {
                    value: 6,
                    message: t('password-min-length')
                  }
                })}
              />
              <PasswordToggle
                type="button"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </PasswordToggle>
              {loginForm.formState.errors.password && <ErrorMessage>{loginForm.formState.errors.password.message}</ErrorMessage>}
            </InputGroup>

            <SubmitButton
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {isLoading ? (
                <>
                  <LoadingSpinner />
                  {t('signing-in')}
                </>
              ) : (
                <>
                  <FaUser />
                  {t('sign-in')}
                </>
              )}
            </SubmitButton>
          </Form>
        ) : (
          <Form onSubmit={registerForm.handleSubmit(onRegisterSubmit)}>
            {/* Show form-level errors */}
            {(error || registerForm.formState.errors.root?.serverError) && (
              <ErrorAlert
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {error || registerForm.formState.errors.root?.serverError.message}
              </ErrorAlert>
            )}

            <InputGroup>
              <InputIcon>
                <FaUser />
              </InputIcon>
              <Input
                type="text"
                placeholder={t('first-name')}
                autoComplete="given-name"
                {...registerForm.register('firstName', {
                  required: t('required-field'),
                  minLength: {
                    value: 2,
                    message: t('name-min-length')
                  }
                })}
                className={registerForm.formState.errors.firstName ? 'error' : ''}
              />
              {registerForm.formState.errors.firstName && (
                <ErrorMessage>
                  {registerForm.formState.errors.firstName.message}
                </ErrorMessage>
              )}
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaUser />
              </InputIcon>
              <Input
                type="text"
                placeholder={t('last-name')}
                autoComplete="family-name"
                id="lastName"
                name="lastName"
                {...registerForm.register('lastName', {
                  required: t('required-field')
                })}
              />
              {registerForm.formState.errors.lastName && <ErrorMessage>{registerForm.formState.errors.lastName.message}</ErrorMessage>}
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaEnvelope />
              </InputIcon>
              <Input
                type="email"
                placeholder={t('email-address')}
                autoComplete="email"
                id="registerEmail"
                name="email"
                {...registerForm.register('email', {
                  required: t('required-field'),
                  pattern: {
                    value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: t('invalid-email')
                  }
                })}
              />
              {registerForm.formState.errors.email && <ErrorMessage>{registerForm.formState.errors.email.message}</ErrorMessage>}
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaPhone />
              </InputIcon>
              <Input
                type="tel"
                placeholder={t('phone-optional')}
                autoComplete="tel"
                {...registerForm.register('phone')}
              />
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaUser />
              </InputIcon>
              <Input
                type="text"
                placeholder={t('address-optional')}
                autoComplete="street-address"
                {...registerForm.register('address')}
              />
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaLock />
              </InputIcon>
              <Input
                type={showPassword ? 'text' : 'password'}
                placeholder={t('password')}
                autoComplete="new-password"
                {...registerForm.register('password', {
                  required: t('required-field'),
                  minLength: {
                    value: 6,
                    message: t('password-min-length')
                  }
                })}
              />
              <PasswordToggle
                type="button"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </PasswordToggle>
              {registerForm.formState.errors.password && <ErrorMessage>{registerForm.formState.errors.password.message}</ErrorMessage>}
            </InputGroup>

            <InputGroup>
              <InputIcon>
                <FaLock />
              </InputIcon>
              <Input
                type={showConfirmPassword ? 'text' : 'password'}
                placeholder={t('confirm-password')}
                autoComplete="new-password"
                {...registerForm.register('confirmPassword', {
                  required: t('confirm-password-required'),
                  validate: value => value === password || t('passwords-do-not-match')
                })}
              />
              <PasswordToggle
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
              </PasswordToggle>
              {registerForm.formState.errors.confirmPassword && <ErrorMessage>{registerForm.formState.errors.confirmPassword.message}</ErrorMessage>}
            </InputGroup>

            <SubmitButton
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {isLoading ? (
                <>
                  <LoadingSpinner />
                  {t('creating-account')}
                </>
              ) : (
                <>
                  <FaUserPlus />
                  {t('create-account')}
                </>
              )}
            </SubmitButton>
          </Form>
        )}
      </LoginCard>
    </LoginContainer>
  );
};

export default LoginPage;
