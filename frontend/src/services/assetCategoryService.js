import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /asset-categories
export const getAssetCategories = async () => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/asset-categories');
  return data;
};

// POST /asset-categories
export const createAssetCategory = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Category created.' }, 300);
  const { data } = await api.post('/asset-categories', payload);
  return data;
};
