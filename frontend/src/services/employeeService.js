import api from './api';

// GET /employees?departmentId=&role=
export const getEmployees = async (params = {}) => {
  const { data } = await api.get('/employees', { params });
  return data.data;
};

// POST /employees  (admin directly creates a new employee account)
export const createEmployee = async (payload) => {
  const { data } = await api.post('/employees', payload);
  return data.data;
};

// PUT /employees/:id
// This is the ONLY place role promotion happens (e.g. Employee -> Asset
// Manager / Department Head). Pass { role: 'asset_manager' } etc.
export const updateEmployee = async (id, payload) => {
  const { data } = await api.put(`/employees/${id}`, payload);
  return data.data;
};

// DELETE /employees/:id
export const deleteEmployee = async (id) => {
  const { data } = await api.delete(`/employees/${id}`);
  return data.data;
};