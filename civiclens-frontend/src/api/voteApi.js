import api from './axios'

export const vote = (commentId, value) =>
  api.post(`/api/comments/${commentId}/vote`, { value })

export const removeVote = (commentId) =>
  api.delete(`/api/comments/${commentId}/vote`)
