import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /departments
export const getDepartments = async () => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/departments');
  return data;
};

// POST /departments
export const createDepartment = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Department created.' }, 300);
  const { data } = await api.post('/departments', payload);
  return data;
};

// PUT /departments/:id
export const updateDepartment = async (id, payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Department updated.' }, 300);
  const { data } = await api.put(`/departments/${id}`, payload);
  return data;
};
