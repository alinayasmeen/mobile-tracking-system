import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  signup: (data: any) => api.post('/auth/signup', data),
  login: (data: any) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Citizen API
export const citizenAPI = {
  registerPhone: (data: any) => api.post('/citizen/phones', data),
  getPhones: () => api.get('/citizen/phones'),
  createReport: (data: any) => api.post('/citizen/reports', data),
  getReports: () => api.get('/citizen/reports'),
  createTransferRequest: (data: any) => api.post('/citizen/transfer-request', data),
  getTransferRequests: () => api.get('/citizen/transfer-requests'),
};

// Retailer API
export const retailerAPI = {
  registerPurchase: (data: any) => api.post('/retailer/purchases', data),
  getPurchases: () => api.get('/retailer/purchases'),
  submitReceivedPhone: (data: any) => api.post('/retailer/received-phone', data),
};

// Admin API
export const adminAPI = {
  getUsers: () => api.get('/admin/users'),
  getPhones: () => api.get('/admin/phones'),
  getReports: () => api.get('/admin/reports'),
  getPurchases: () => api.get('/admin/purchases'),
  getTransferRequests: () => api.get('/admin/transfer-requests'),
  updateReportStatus: (id: number, status: string) =>
    api.put(`/admin/reports/${id}`, { status }),
  updateTransferStatus: (id: number, data: any) =>
    api.put(`/admin/transfer-requests/${id}`, data),
  getStats: () => api.get('/admin/stats'),
  getMatches: () => api.get('/admin/matches'),
};
