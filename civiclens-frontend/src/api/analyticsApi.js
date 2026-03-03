import api from './axios'

export const getAnalytics = (amendmentId) =>
  api.get(`/api/amendments/${amendmentId}/analytics`)

export const triggerAnalysis = (amendmentId) =>
  api.post(`/api/admin/amendments/${amendmentId}/analyze`)

export const getAdminDashboard = () =>
  api.get('/api/admin/dashboard')

export const downloadReport = (amendmentId) =>
  api.get(`/api/amendments/${amendmentId}/report/pdf`, { responseType: 'blob' })
