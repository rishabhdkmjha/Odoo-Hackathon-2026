import api from './api';

/**
 * GET /dashboard
 * Returns { kpis, overdue, myActiveAllocations } - see backend/README.md.
 */
export const getDashboardSummary = async () => {
  const { data } = await api.get('/dashboard');
  return data.data;
};