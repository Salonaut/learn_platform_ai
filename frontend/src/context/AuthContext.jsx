/**
 * @file AuthContext.jsx
 * @brief Authentication context provider for the application.
 * 
 * @details Manages user authentication state, login, registration, and logout
 * functionality using React Context API and localStorage for persistence.
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api';

const AuthContext = createContext(null);

/**
 * @brief Custom hook to access authentication context.
 * 
 * @return {Object} Authentication context value
 * @throws {Error} If used outside of AuthProvider
 * 
 * @example
 * const { user, login, logout } = useAuth();
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

/**
 * @brief Authentication provider component.
 * 
 * @details Wraps the application to provide authentication context to all children.
 * Manages user state, authentication tokens, and provides login/logout functionality.
 * 
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * 
 * @example
 * <AuthProvider>
 *   <App />
 * </AuthProvider>
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Перевірка чи є користувач в localStorage при завантаженні
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('access_token');
    
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  /**
   * @brief Authenticate user with email and password.
   * 
   * @param {string} email - User's email address
   * @param {string} password - User's password
   * 
   * @return {Promise<Object>} Object with success status and optional error message
   */
  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      const { user, access, refresh } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setUser(user);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed',
      };
    }
  };

  /**
   * @brief Register a new user account.
   * 
   * @param {Object} data - Registration data including email, password, username
   * 
   * @return {Promise<Object>} Object with success status and optional error message
   */
  const register = async (data) => {
    try {
      const response = await authAPI.register(data);
      const { user, access, refresh } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setUser(user);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Registration failed',
      };
    }
  };

  /**
   * @brief Log out the current user.
   * 
   * @details Clears authentication tokens from localStorage and resets user state.
   * Calls the logout API endpoint to invalidate the refresh token.
   */
  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await authAPI.logout(refreshToken);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      setUser(null);
    }
  };

  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
