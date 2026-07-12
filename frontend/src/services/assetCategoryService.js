import api from './api';

// GET /categories  (backend path is /categories, not /asset-categories)
export const getAssetCategories = async () => {
  const { data } = await api.get('/categories');
  return data.data;
};

// POST /categories
export const createAssetCategory = async (payload) => {
  const { data } = await api.post('/categories', payload);
  return data.data;
};