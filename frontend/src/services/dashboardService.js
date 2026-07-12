import api from './api';
import { mockResolve } from '../utils/mockAdapter';
import mockDashboard from '../mock/dashboard.json';

const USE_MOCK = true;

/**
 * GET /dashboard
 * Returns KPI snapshot, trend data, overdue/upcoming returns, and recent activity.
 */
export const getDashboardSummary = async () => {
  if (USE_MOCK) {
    return mockResolve(mockDashboard, 450);
  }
  const { data } = await api.get('/dashboard');
  return data;
};
