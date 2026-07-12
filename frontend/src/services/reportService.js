import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /reports?type=utilization|maintenance|allocation|booking-heatmap
export const getReport = async (type, params = {}) => {
  if (USE_MOCK) return mockResolve({ type, data: [] }, 300);
  const { data } = await api.get('/reports', { params: { type, ...params } });
  return data;
};
