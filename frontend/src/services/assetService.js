import api from './api';

// GET /assets?search=&categoryId=&status=&departmentId=&location=
export const getAssets = async (params = {}) => {
  const { data } = await api.get('/assets', { params });
  return data.data;
};

// GET /assets/:id/history  (allocation + maintenance history for one asset)
// Note: the backend has no single-asset GET /assets/:id. If you need the
// asset's own fields (not just history), filter the result of getAssets().
export const getAssetHistory = async (id) => {
  const { data } = await api.get(`/assets/${id}/history`);
  return data.data;
};

// POST /assets
export const createAsset = async (payload) => {
  const { data } = await api.post('/assets', payload);
  return data.data;
};

// PUT /assets/:id
export const updateAsset = async (id, payload) => {
  const { data } = await api.put(`/assets/${id}`, payload);
  return data.data;
};

// DELETE /assets/:id
export const deleteAsset = async (id) => {
  const { data } = await api.delete(`/assets/${id}`);
  return data.data;
};