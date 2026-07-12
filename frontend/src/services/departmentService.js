import api from './api';
import { mockResolve } from '../utils/mockAdapter';

// GET /departments
export const getDepartments = async () => {
  const { data } = await api.get('/departments');
  return data.data;
};

// POST /departments
export const createDepartment = async (payload) => {
  const { data } = await api.post('/departments', payload);
  return data.data;
};

// PUT /departments/:id
// NOT IMPLEMENTED on the backend yet (only GET + POST exist for departments).
// Kept mocked so the UI doesn't 404 - ask backend to add this endpoint,
// then swap this to a real api.put('/departments/${id}', payload) call.
export const updateDepartment = async (id, payload) => {
  return mockResolve({ id, ...payload, message: 'Department updated (mock - backend endpoint pending).' }, 300);
};