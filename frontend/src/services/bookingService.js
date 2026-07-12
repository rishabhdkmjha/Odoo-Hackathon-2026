import api from './api';
import { mockResolve } from '../utils/mockAdapter';

const USE_MOCK = true;

// GET /booking?resourceId=&date=
export const getBookings = async (params = {}) => {
  if (USE_MOCK) return mockResolve([], 300);
  const { data } = await api.get('/booking', { params });
  return data;
};

// POST /booking  { resourceId, startTime, endTime, bookedFor }
export const createBooking = async (payload) => {
  if (USE_MOCK) return mockResolve({ message: 'Resource booked.' }, 300);
  const { data } = await api.post('/booking', payload);
  return data;
};

// PUT /booking/:id/cancel
export const cancelBooking = async (id) => {
  if (USE_MOCK) return mockResolve({ message: 'Booking cancelled.' }, 300);
  const { data } = await api.put(`/booking/${id}/cancel`);
  return data;
};
