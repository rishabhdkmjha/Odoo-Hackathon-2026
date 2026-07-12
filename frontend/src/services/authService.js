import api from './api';
import { mockResolve, mockReject } from '../utils/mockAdapter';
import mockAuth from '../mock/user.json';

const USE_MOCK = true;

/**
 * POST /auth/login
 * body: { email, password }
 */
export const login = async ({ email, password }) => {
  if (USE_MOCK) {
    if (!email || !password) {
      return mockReject('Email and password are required.');
    }
    return mockResolve(mockAuth, 500);
  }
  const { data } = await api.post('/auth/login', { email, password });
  return data;
};

/**
 * POST /auth/signup
 * Signup ALWAYS creates a plain Employee account. No role field is sent.
 * body: { name, email, password, department }
 */
export const signup = async (payload) => {
  if (USE_MOCK) {
    return mockResolve({ message: 'Employee account created. Please log in.' }, 500);
  }
  const { data } = await api.post('/auth/signup', payload);
  return data;
};

/**
 * POST /auth/forgot-password
 * body: { email }
 */
export const forgotPassword = async (email) => {
  if (USE_MOCK) {
    return mockResolve({ message: 'Password reset link sent if the account exists.' });
  }
  const { data } = await api.post('/auth/forgot-password', { email });
  return data;
};

/**
 * GET /auth/session
 * Validates the current token on app load / refresh.
 */
export const validateSession = async () => {
  if (USE_MOCK) {
    const cached = localStorage.getItem('assetflow_user');
    return mockResolve(cached ? JSON.parse(cached) : null, 150);
  }
  const { data } = await api.get('/auth/session');
  return data;
};

export const logout = () => {
  localStorage.removeItem('assetflow_token');
  localStorage.removeItem('assetflow_user');
};
