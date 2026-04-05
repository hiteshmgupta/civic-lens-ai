import api from './axios'

export const getComments = (amendmentId, params) =>
  api.get(`/api/amendments/${amendmentId}/comments`, { params })

export const addComment = (amendmentId, data) =>
  api.post(`/api/amendments/${amendmentId}/comments`, data)

export const deleteComment = (commentId) =>
  api.delete(`/api/admin/comments/${commentId}`)
