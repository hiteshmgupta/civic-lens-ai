import api from './axios'

export const vote = (amendmentId, value) =>
  api.post(`/api/amendments/${amendmentId}/vote`, { value })

export const removeVote = (amendmentId) =>
  api.delete(`/api/amendments/${amendmentId}/vote`)
