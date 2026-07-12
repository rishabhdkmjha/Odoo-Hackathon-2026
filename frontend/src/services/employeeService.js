import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /employees?search=&department=&role=&status=
export const getEmployees = async (params = {}) => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/employees', { params });
  return data;
};

// POST /employees  (admin promotes/creates Department Head or Asset Manager here)
export const createOrUpdateEmployeeRole = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Employee updated.' }, 300);
  const { data } = await api.post('/employees', payload);
  return data;
};
