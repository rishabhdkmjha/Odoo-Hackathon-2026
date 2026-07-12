import axios from 'axios';

// The ONLY place BASE_URL is defined. Backend dev swaps this via .env.
export const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// The backend (FastAPI/Pydantic) speaks snake_case. The frontend speaks
// camelCase. Rather than rewriting every service call by hand, we convert
// automatically at the HTTP boundary: outgoing bodies -> snake_case,
// incoming responses -> camelCase. Query params are left alone since they're
// attached per-call with axios `params` and are simple key/value pairs.
const toSnake = (str) => str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
const toCamel = (str) => str.replace(/_([a-z0-9])/g, (_, letter) => letter.toUpperCase());

const transformKeys = (value, fn) => {
  if (Array.isArray(value)) {
    return value.map((item) => transformKeys(item, fn));
  }
  if (value !== null && typeof value === 'object' && !(value instanceof Date) && !(value instanceof File)) {
    return Object.fromEntries(
      Object.entries(value).map(([key, val]) => [fn(key), transformKeys(val, fn)])
    );
  }
  return value;
};

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT + convert outgoing bodies to snake_case for the backend.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('assetflow_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (config.data && typeof config.data === 'object') {
    config.data = transformKeys(config.data, toSnake);
  }
  return config;
});

// Convert incoming responses to camelCase + central 401 handling.
api.interceptors.response.use(
  (response) => {
    if (response.data && typeof response.data === 'object') {
      response.data = transformKeys(response.data, toCamel);
    }
    return response;
  },
  (error) => {
    if (error.response?.data && typeof error.response.data === 'object') {
      error.response.data = transformKeys(error.response.data, toCamel);
    }
    if (error.response?.status === 401) {
      localStorage.removeItem('assetflow_token');
      localStorage.removeItem('assetflow_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;