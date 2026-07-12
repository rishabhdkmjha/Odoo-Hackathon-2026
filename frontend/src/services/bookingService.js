import api from './api';

// GET /booking?assetId=
export const getBookings = async (params = {}) => {
  const { data } = await api.get('/booking', { params });
  return data.data;
};

// POST /booking  { assetId, startTime, endTime, purpose, departmentId }
// Rejected with 409 if the time window overlaps an existing booking for
// the same asset.
export const createBooking = async (payload) => {
  const { data } = await api.post('/booking', payload);
  return data.data;
};

// PUT /booking/:id  { status: 'cancelled' }
// The backend has no dedicated /cancel route - cancelling is just a status
// update on the booking, same endpoint used for rescheduling (start/end time).
export const cancelBooking = async (id) => {
  const { data } = await api.put(`/booking/${id}`, { status: 'cancelled' });
  return data.data;
};

// PUT /booking/:id  { startTime, endTime }
export const rescheduleBooking = async (id, payload) => {
  const { data } = await api.put(`/booking/${id}`, payload);
  return data.data;
};