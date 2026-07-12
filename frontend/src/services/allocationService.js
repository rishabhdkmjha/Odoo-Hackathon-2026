import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// POST /allocation  { assetId, employeeId | departmentId, expectedReturnDate }
export const allocateAsset = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset allocated.' }, 300);
  const { data } = await api.post('/allocation', payload);
  return data;
};

// POST /allocation/transfer-request
export const requestTransfer = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Transfer requested.' }, 300);
  const { data } = await api.post('/allocation/transfer-request', payload);
  return data;
};

// PUT /allocation/transfer-request/:id/approve
export const approveTransfer = async (id) => {
  if (USE_MOCK) return mockResolve({ message: 'Transfer approved.' }, 300);
  const { data } = await api.put(`/allocation/transfer-request/${id}/approve`);
  return data;
};

// PUT /allocation/:id/return
export const returnAsset = async (id, payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset marked returned.' }, 300);
  const { data } = await api.put(`/allocation/${id}/return`, payload);
  return data;
};
