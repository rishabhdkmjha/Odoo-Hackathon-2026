import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /maintenance?status=&priority=&assetId=
export const getMaintenanceRequests = async (params = {}) => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/maintenance', { params });
  return data;
};

// POST /maintenance  { assetId, issue, priority, photo }
export const raiseMaintenanceRequest = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Maintenance request raised.' }, 300);
  const { data } = await api.post('/maintenance', payload);
  return data;
};

// PUT /maintenance/:id/status  { status: 'Approved' | 'Rejected' | 'In Progress' | 'Resolved', technicianId? }
export const updateMaintenanceStatus = async (id, payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Maintenance status updated.' }, 300);
  const { data } = await api.put(`/maintenance/${id}/status`, payload);
  return data;
};
