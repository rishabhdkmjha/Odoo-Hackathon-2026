import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /assets?search=&category=&status=&department=&location=
export const getAssets = async (params = {}) => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/assets', { params });
  return data;
};

// GET /assets/:id  (includes allocation + maintenance history)
export const getAssetById = async (id) => {
  if (USE_MOCK) return mockResolve(null, 300);
  const { data } = await api.get(`/assets/${id}`);
  return data;
};

// POST /assets
export const createAsset = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset registered.' }, 300);
  const { data } = await api.post('/assets', payload);
  return data;
};

// PUT /assets/:id
export const updateAsset = async (id, payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset updated.' }, 300);
  const { data } = await api.put(`/assets/${id}`, payload);
  return data;
};

// DELETE /assets/:id
export const deleteAsset = async (id) => {
  if (USE_MOCK) return mockResolve({ message: 'Asset removed.' }, 300);
  const { data } = await api.delete(`/assets/${id}`);
  return data;
};
