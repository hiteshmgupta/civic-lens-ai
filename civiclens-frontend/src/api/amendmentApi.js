import api from './axios'

export const getAmendments = (params) => api.get('/api/amendments', { params })
export const getAmendment = (id) => api.get(`/api/amendments/${id}`)
export const createAmendment = (data) => api.post('/api/amendments', data)
export const updateAmendment = (id, data) => api.put(`/api/amendments/${id}`, data)
export const deleteAmendment = (id) => api.delete(`/api/admin/amendments/${id}`)
