import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /notifications
export const getNotifications = async () => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/notifications');
  return data;
};

// PUT /notifications/:id/read
export const markNotificationRead = async (id) => {
  if (USE_MOCK) return mockResolve({ message: 'Marked as read.' }, 200);
  const { data } = await api.put(`/notifications/${id}/read`);
  return data;
};
