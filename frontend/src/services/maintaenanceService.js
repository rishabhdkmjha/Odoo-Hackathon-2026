import api from './api';

// GET /maintenance?assetId=&status=
// Note: the backend does not support filtering by priority server-side -
// filter that client-side if needed.
export const getMaintenanceRequests = async (params = {}) => {
  const { data } = await api.get('/maintenance', { params });
  return data.data;
};

// POST /maintenance  { assetId, issueDescription, priority, photoUrl }
// priority must be one of: low | medium | high | critical
export const raiseMaintenanceRequest = async (payload) => {
  const { data } = await api.post('/maintenance', payload);
  return data.data;
};

// PUT /maintenance/:id  { status, technicianName?, resolutionNotes? }
// status must be one of: pending | approved | rejected | technician_assigned
// | in_progress | resolved, and must follow that exact forward order - the
// backend rejects illegal jumps (e.g. pending -> resolved) with a 409.
export const updateMaintenanceStatus = async (id, payload) => {
  const { data } = await api.put(`/maintenance/${id}`, payload);
  return data.data;
};