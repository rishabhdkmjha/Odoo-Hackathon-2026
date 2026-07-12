import api from './api';
import { mockResolve } from '../utils/mockAdapter';

// GET /notifications?unreadOnly=true
export const getNotifications = async (unreadOnly = false) => {
  const { data } = await api.get('/notifications', { params: { unreadOnly } });
  return data.data;
};

// NOT IMPLEMENTED on the backend yet (no mark-as-read endpoint exists).
// Kept mocked so the UI doesn't 404 - ask backend to add PUT
// /notifications/:id/read, then wire this for real.
export const markNotificationRead = async (id) => {
  return mockResolve({ id, isRead: true, message: 'Marked as read (mock - backend endpoint pending).' }, 200);
};