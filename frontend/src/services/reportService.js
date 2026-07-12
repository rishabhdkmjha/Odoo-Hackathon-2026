import api from './api';

// GET /reports
// Returns everything at once: { assetUtilization, maintenanceFrequencyByCategory,
// departmentAllocationSummary, bookingHeatmapByHour }. The backend does not
// support a `type` filter param - fetch once and pick the section(s) you need
// on the frontend.
export const getReports = async () => {
  const { data } = await api.get('/reports');
  return data.data;
};