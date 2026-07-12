import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /audits
export const getAuditCycles = async () => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/audits');
  return data;
};

// POST /audits  { scopeDepartment, scopeLocation, startDate, endDate, auditorIds }
export const createAuditCycle = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Audit cycle created.' }, 300);
  const { data } = await api.post('/audits', payload);
  return data;
};

// PUT /audits/:id/asset/:assetId  { verdict: 'Verified' | 'Missing' | 'Damaged' }
export const markAuditAsset = async (auditId, assetId, payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset marked.' }, 300);
  const { data } = await api.put(`/audits/${auditId}/asset/${assetId}`, payload);
  return data;
};

// PUT /audits/:id/close
export const closeAuditCycle = async (id) => {
  if (USE_MOCK) return mockResolve({ message: 'Audit cycle closed.' }, 300);
  const { data } = await api.put(`/audits/${id}/close`);
  return data;
};
