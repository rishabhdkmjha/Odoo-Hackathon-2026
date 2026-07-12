import api from './api';
import { mockResolve } from '../utils/mockAdapter';

// Live: backend implements /auth/login and /auth/signup.
// Still mocked: /auth/forgot-password and /auth/session don't exist on the
// backend yet - flip these once (if) those endpoints are added.
const USE_MOCK_FORGOT_PASSWORD = true;
const USE_MOCK_SESSION = true;

/**
 * POST /auth/login
 * body: { email, password }
 * Backend envelope: { success, message, data: { accessToken, tokenType, user } }
 * (accessToken/tokenType are camelCase here because api.js auto-converts the
 * backend's snake_case response.)
 */
export const login = async ({ email, password }) => {
  const { data } = await api.post('/auth/login', { email, password });
  return { token: data.data.accessToken, user: data.data.user };
};

/**
 * POST /auth/signup
 * Signup ALWAYS creates a plain Employee account. No role field is sent.
 * body: { name, email, password }
 */
export const signup = async (payload) => {
  const { data } = await api.post('/auth/signup', payload);
  return data.data;
};

/**
 * POST /auth/forgot-password
 * Not implemented on the backend yet - stays mocked so the UI flow doesn't
 * break. Swap to a real call once the endpoint exists.
 */
export const forgotPassword = async (email) => {
  if (USE_MOCK_FORGOT_PASSWORD) {
    return mockResolve({ message: 'Password reset link sent if the account exists.' });
  }
  const { data } = await api.post('/auth/forgot-password', { email });
  return data;
};

/**
 * GET /auth/session
 * Not implemented on the backend yet. For now we just trust the cached user
 * in localStorage (set at login) rather than round-tripping to the server.
 * Swap to a real call once a session-validation endpoint exists.
 */
export const validateSession = async () => {
  if (USE_MOCK_SESSION) {
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