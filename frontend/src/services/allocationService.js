import api from './api';

// POST /allocation  { assetId, employeeId | departmentId, expectedReturnDate }
// 409 if the asset already has an active allocation - the response message
// names the current holder; surface that and offer requestTransfer() instead.
export const allocateAsset = async (payload) => {
  const { data } = await api.post('/allocation', payload);
  return data.data;
};

// PUT /allocation/return  { allocationId, conditionCheckinNotes }
// Note: the allocation id goes in the BODY, not the URL.
export const returnAsset = async (allocationId, conditionCheckinNotes) => {
  const { data } = await api.put('/allocation/return', {
    allocationId,
    conditionCheckinNotes,
  });
  return data.data;
};

// GET /allocation/overdue
export const getOverdueAllocations = async () => {
  const { data } = await api.get('/allocation/overdue');
  return data.data;
};

// POST /transfer  { assetId, toEmployeeId, reason }
// (backend route is /transfer, not /allocation/transfer-request)
export const requestTransfer = async (payload) => {
  const { data } = await api.post('/transfer', payload);
  return data.data;
};

// PUT /transfer/decision  { transferId, approve, reason }
// (backend route is /transfer/decision, not /allocation/transfer-request/:id/approve)
export const decideTransfer = async (transferId, approve, reason) => {
  const { data } = await api.put('/transfer/decision', { transferId, approve, reason });
  return data.data;
};

// Convenience wrappers matching the old approve-only naming, in case pages
// already call these:
export const approveTransfer = (transferId) => decideTransfer(transferId, true);
export const rejectTransfer = (transferId, reason) => decideTransfer(transferId, false, reason);