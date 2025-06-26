import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { FaUser, FaLock, FaEye, FaEyeSlash, FaUserPlus, FaEnvelope } from 'react-icons/fa';
import { useAuth } from '../contexts/AuthContext';

const LoginContainer = styled.div`
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${props => props.theme.spacing.xl} 0;
  background: linear-gradient(135deg, ${props => props.theme.colors.light} 0%, rgba(102, 126, 234, 0.1) 100%);
`;

const LoginCard = styled(motion.div)`
  background: white;
  border-radius: 20px;
  padding: ${props => props.theme.spacing.xxl};
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  margin: 0 ${props => props.theme.spacing.md};
`;

const LoginHeader = styled.div`
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.dark};
  font-size: 2.5rem;
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 1.1rem;
`;

const TabContainer = styled.div`
  display: flex;
  margin-bottom: ${props => props.theme.spacing.xl};
  border-radius: 10px;
  background: ${props => props.theme.colors.light};
  padding: 4px;
`;

const Tab = styled.button`
  flex: 1;
  padding: ${props => props.theme.spacing.sm};
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  background: ${props => props.active ? 'white' : 'transparent'};
  color: ${props => props.active ? props.theme.colors.secondary : props.theme.colors.gray};
  box-shadow: ${props => props.active ? '0 2px 4px rgba(0,0,0,0.1)' : 'none'};
`;

const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const FormGroup = styled.div`
  position: relative;
`;

const Label = styled.label`
  display: block;
  margin-bottom: ${props => props.theme.spacing.xs};
  font-weight: 600;
  color: ${props => props.theme.colors.dark};
`;

const InputContainer = styled.div`
  position: relative;
`;

const Input = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.md};
  padding-left: 3rem;
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.secondary};
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    outline: none;
  }
  
  &.error {
    border-color: ${props => props.theme.colors.danger};
  }
`;

const InputIcon = styled.div`
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: ${props => props.theme.colors.gray};
  font-size: 1.2rem;
`;

const PasswordToggle = styled.button`
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: ${props => props.theme.colors.gray};
  font-size: 1.2rem;
  cursor: pointer;
  
  &:hover {
    color: ${props => props.theme.colors.secondary};
  }
`;

const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.danger};
  font-size: 0.9rem;
  margin-top: ${props => props.theme.spacing.xs};
  display: block;
`;

const SubmitButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.secondary} 0%, ${props => props.theme.colors.accent} 100%);
  color: white;
  padding: ${props => props.theme.spacing.md};
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: ${props => props.theme.spacing.md};
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

const ForgotPassword = styled.a`
  text-align: center;
  color: ${props => props.theme.colors.secondary};
  font-size: 0.9rem;
  margin-top: ${props => props.theme.spacing.sm};
  cursor: pointer;
  
  &:hover {
    text-decoration: underline;
  }
`;

const Divider = styled.div`
  display: flex;
  align-items: center;
  margin: ${props => props.theme.spacing.lg} 0;
  
  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: ${props => props.theme.colors.lightGray};
  }
  
  span {
    padding: 0 ${props => props.theme.spacing.md};
    color: ${props => props.theme.colors.gray};
    font-size: 0.9rem;
  }
`;

const SocialButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: ${props => props.theme.spacing.sm};
  width: 100%;
  padding: ${props => props.theme.spacing.md};
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 10px;
  background: white;
  color: ${props => props.theme.colors.dark};
  font-weight: 600;
  transition: all 0.3s ease;
  margin-bottom: ${props => props.theme.spacing.sm};
  
  &:hover {
    border-color: ${props => props.theme.colors.secondary};
    transform: translateY(-1px);
  }
`;

const SuccessMessage = styled.div`
  background: ${props => props.theme.colors.success};
  color: white;
  padding: ${props => props.theme.spacing.md};
  border-radius: 10px;
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const LoginPage = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [registered, setRegistered] = useState(false);
  
  const navigate = useNavigate();
  
  const { register: loginRegister, handleSubmit: handleLoginSubmit, formState: { errors: loginErrors }, reset: resetLogin } = useForm();
  const { register: signupRegister, handleSubmit: handleSignupSubmit, formState: { errors: signupErrors }, watch, reset: resetSignup } = useForm();
  
  const password = watch('password');

  const onLoginSubmit = async (data) => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate successful login
      localStorage.setItem('userToken', 'demo_token');
      localStorage.setItem('userEmail', data.email);
      
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const onSignupSubmit = async (data) => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setRegistered(true);
      resetSignup();
      
      setTimeout(() => {
        setRegistered(false);
        setActiveTab('login');
      }, 3000);
    } catch (error) {
      console.error('Registration failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <LoginContainer>
      <LoginCard
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <LoginHeader>
          <Title>Welcome Back</Title>
          <Subtitle>Sign in to your account or create a new one</Subtitle>
        </LoginHeader>

        <TabContainer>
          <Tab
            active={activeTab === 'login'}
            onClick={() => setActiveTab('login')}
            type="button"
          >
            Sign In
          </Tab>
          <Tab
            active={activeTab === 'signup'}
            onClick={() => setActiveTab('signup')}
            type="button"
          >
            Sign Up
          </Tab>
        </TabContainer>

        {registered && (
          <SuccessMessage>
            Account created successfully! Please sign in with your credentials.
          </SuccessMessage>
        )}

        {activeTab === 'login' ? (
          <FormContainer onSubmit={handleLoginSubmit(onLoginSubmit)}>
            <FormGroup>
              <Label>Email Address</Label>
              <InputContainer>
                <InputIcon><FaUser /></InputIcon>
                <Input
                  type="email"
                  {...loginRegister('email', { 
                    required: 'Email is required',
                    pattern: {
                      value: /^\S+@\S+$/i,
                      message: 'Invalid email address'
                    }
                  })}
                  className={loginErrors.email ? 'error' : ''}
                  placeholder="Enter your email"
                />
              </InputContainer>
              {loginErrors.email && <ErrorMessage>{loginErrors.email.message}</ErrorMessage>}
            </FormGroup>

            <FormGroup>
              <Label>Password</Label>
              <InputContainer>
                <InputIcon><FaLock /></InputIcon>
                <Input
                  type={showPassword ? 'text' : 'password'}
                  {...loginRegister('password', { required: 'Password is required' })}
                  className={loginErrors.password ? 'error' : ''}
                  placeholder="Enter your password"
                />
                <PasswordToggle type="button" onClick={togglePasswordVisibility}>
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </PasswordToggle>
              </InputContainer>
              {loginErrors.password && <ErrorMessage>{loginErrors.password.message}</ErrorMessage>}
            </FormGroup>

            <SubmitButton
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </SubmitButton>

            <ForgotPassword>Forgot your password?</ForgotPassword>
          </FormContainer>
        ) : (
          <FormContainer onSubmit={handleSignupSubmit(onSignupSubmit)}>
            <FormGroup>
              <Label>First Name</Label>
              <InputContainer>
                <InputIcon><FaUser /></InputIcon>
                <Input
                  {...signupRegister('firstName', { required: 'First name is required' })}
                  className={signupErrors.firstName ? 'error' : ''}
                  placeholder="Enter your first name"
                />
              </InputContainer>
              {signupErrors.firstName && <ErrorMessage>{signupErrors.firstName.message}</ErrorMessage>}
            </FormGroup>

            <FormGroup>
              <Label>Last Name</Label>
              <InputContainer>
                <InputIcon><FaUser /></InputIcon>
                <Input
                  {...signupRegister('lastName', { required: 'Last name is required' })}
                  className={signupErrors.lastName ? 'error' : ''}
                  placeholder="Enter your last name"
                />
              </InputContainer>
              {signupErrors.lastName && <ErrorMessage>{signupErrors.lastName.message}</ErrorMessage>}
            </FormGroup>

            <FormGroup>
              <Label>Email Address</Label>
              <InputContainer>
                <InputIcon><FaUser /></InputIcon>
                <Input
                  type="email"
                  {...signupRegister('email', { 
                    required: 'Email is required',
                    pattern: {
                      value: /^\S+@\S+$/i,
                      message: 'Invalid email address'
                    }
                  })}
                  className={signupErrors.email ? 'error' : ''}
                  placeholder="Enter your email"
                />
              </InputContainer>
              {signupErrors.email && <ErrorMessage>{signupErrors.email.message}</ErrorMessage>}
            </FormGroup>

            <FormGroup>
              <Label>Password</Label>
              <InputContainer>
                <InputIcon><FaLock /></InputIcon>
                <Input
                  type={showPassword ? 'text' : 'password'}
                  {...signupRegister('password', { 
                    required: 'Password is required',
                    minLength: {
                      value: 6,
                      message: 'Password must be at least 6 characters'
                    }
                  })}
                  className={signupErrors.password ? 'error' : ''}
                  placeholder="Create a password"
                />
                <PasswordToggle type="button" onClick={togglePasswordVisibility}>
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </PasswordToggle>
              </InputContainer>
              {signupErrors.password && <ErrorMessage>{signupErrors.password.message}</ErrorMessage>}
            </FormGroup>

            <FormGroup>
              <Label>Confirm Password</Label>
              <InputContainer>
                <InputIcon><FaLock /></InputIcon>
                <Input
                  type={showConfirmPassword ? 'text' : 'password'}
                  {...signupRegister('confirmPassword', { 
                    required: 'Please confirm your password',
                    validate: value => value === password || 'Passwords do not match'
                  })}
                  className={signupErrors.confirmPassword ? 'error' : ''}
                  placeholder="Confirm your password"
                />
                <PasswordToggle type="button" onClick={toggleConfirmPasswordVisibility}>
                  {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                </PasswordToggle>
              </InputContainer>
              {signupErrors.confirmPassword && <ErrorMessage>{signupErrors.confirmPassword.message}</ErrorMessage>}
            </FormGroup>

            <SubmitButton
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </SubmitButton>
          </FormContainer>
        )}

        <Divider>
          <span>or continue with</span>
        </Divider>

        <SocialButton type="button">
          <span style={{ color: '#4285f4' }}>G</span>
          Continue with Google
        </SocialButton>

        <SocialButton type="button">
          <span style={{ color: '#1877f2' }}>f</span>
          Continue with Facebook
        </SocialButton>
      </LoginCard>
    </LoginContainer>
  );
};

export default LoginPage;
