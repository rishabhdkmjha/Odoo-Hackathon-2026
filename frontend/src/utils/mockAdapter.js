// Simulates a network round-trip so loading states are visible during dev.
// Swap USE_MOCK to false inside a service file once its endpoint is live.
export const mockResolve = (data, delay = 350) =>
  new Promise((resolve) => setTimeout(() => resolve(data), delay));

export const mockReject = (message = 'Request failed', delay = 350) =>
  new Promise((_, reject) =>
    setTimeout(() => reject({ response: { data: { message } } }), delay)
  );
