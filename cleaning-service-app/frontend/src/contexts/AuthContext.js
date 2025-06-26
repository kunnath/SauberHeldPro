import React, { createContext, useContext, useReducer, useEffect } from 'react';
import apiService from '../services/api';

const AuthContext = createContext();

const initialState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
    case 'REGISTER_START':
    case 'VERIFY_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    
    case 'LOGIN_SUCCESS':
    case 'REGISTER_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    
    case 'VERIFY_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    
    case 'LOGIN_FAILURE':
    case 'REGISTER_FAILURE':
    case 'VERIFY_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload },
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Verify token on app load
  useEffect(() => {
    const verifyToken = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken && !state.isAuthenticated) {
        try {
          dispatch({ type: 'VERIFY_START' });
          const response = await apiService.verifyToken();
          dispatch({ 
            type: 'VERIFY_SUCCESS', 
            payload: { user: response.user } 
          });
        } catch (error) {
          console.error('Token verification failed:', error);
          localStorage.removeItem('token');
          dispatch({ 
            type: 'VERIFY_FAILURE', 
            payload: error.message 
          });
        }
      } else if (!storedToken) {
        dispatch({ 
          type: 'VERIFY_FAILURE', 
          payload: null 
        });
      }
    };

    verifyToken();
  }, []); // Only run once on mount

  const login = async (credentials) => {
    try {
      dispatch({ type: 'LOGIN_START' });
      const response = await apiService.login(credentials);
      console.log('🔑 Login API response:', response);
      dispatch({ 
        type: 'LOGIN_SUCCESS', 
        payload: { 
          user: response.user, 
          token: response.token 
        } 
      });
      console.log('✅ Login dispatch successful, authentication state should be true');
      return response;
    } catch (error) {
      console.error('❌ Login failed:', error);
      dispatch({ 
        type: 'LOGIN_FAILURE', 
        payload: error.message 
      });
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      dispatch({ type: 'REGISTER_START' });
      const response = await apiService.register(userData);
      dispatch({ 
        type: 'REGISTER_SUCCESS', 
        payload: { 
          user: response.user, 
          token: response.token 
        } 
      });
      return response;
    } catch (error) {
      dispatch({ 
        type: 'REGISTER_FAILURE', 
        payload: error.message 
      });
      throw error;
    }
  };

  const logout = () => {
    apiService.logout();
    dispatch({ type: 'LOGOUT' });
  };

  const updateUser = (userData) => {
    dispatch({ 
      type: 'UPDATE_USER', 
      payload: userData 
    });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
