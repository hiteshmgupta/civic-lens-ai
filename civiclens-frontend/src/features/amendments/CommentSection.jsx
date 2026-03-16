import { useState, useEffect } from 'react'
import { getComments, addComment } from '../../api/commentApi'
import { useAuth } from '../../context/AuthContext'
import { formatDateTime } from '../../utils/constants'
import VoteControls from './VoteControls'

export default function CommentSection({ amendmentId, status }) {
  const { user } = useAuth()
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [body, setBody] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const fetchComments = async () => {
    try {
      const res = await getComments(amendmentId)
      setComments(res.data.content || res.data || [])
    } catch (err) {
      console.error('Failed to load comments:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchComments()
  }, [amendmentId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!body.trim() || submitting) return

    setSubmitting(true)
    setError(null)
    try {
      const res = await addComment(amendmentId, { body: body.trim() })
      setComments(prev => [res.data, ...prev])
      setBody('')
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add comment')
    } finally {
      setSubmitting(false)
    }
  }

  const isClosed = status === 'CLOSED'

  return (
    <div className="space-y-4">
      <h3 className="section-title flex items-center gap-2">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-civic-400">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
        Expert Discussion
        <span className="text-sm font-normal text-dark-500">({comments.length})</span>
      </h3>

      {/* Comment Input */}
      {user && !isClosed ? (
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="relative">
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="Share your analysis or perspective on this amendment..."
              className="input-field min-h-[100px] resize-y"
              maxLength={2000}
            />
            <span className="absolute bottom-3 right-3 text-xs text-dark-600">
              {body.length}/2000
            </span>
          </div>
          {error && (
            <p className="text-sm text-rose-400">{error}</p>
          )}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!body.trim() || submitting}
              className="btn-primary text-sm disabled:opacity-50"
            >
              {submitting ? 'Posting...' : 'Post Comment'}
            </button>
          </div>
        </form>
      ) : isClosed ? (
        <div className="glass-card p-4 text-center text-sm text-dark-400">
          This amendment is closed. Comments are no longer accepted.
        </div>
      ) : (
        <div className="glass-card p-4 text-center text-sm text-dark-400">
          <a href="/login" className="text-civic-400 hover:text-civic-300">Sign in</a> to add your comment.
        </div>
      )}

      {/* Comments List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="glass-card p-4 animate-pulse">
              <div className="h-4 bg-dark-700 rounded w-1/4 mb-3" />
              <div className="h-3 bg-dark-800 rounded w-3/4 mb-2" />
              <div className="h-3 bg-dark-800 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : comments.length === 0 ? (
        <div className="glass-card p-8 text-center">
          <div className="text-3xl mb-2">💬</div>
          <p className="text-sm text-dark-400">No comments yet. Be the first to share your perspective.</p>
        </div>
      ) : (
        <div className="space-y-2">
          {comments.map((comment) => (
            <CommentItem key={comment.id} comment={comment} />
          ))}
        </div>
      )}
    </div>
  )
}

function CommentItem({ comment }) {
  return (
    <div className="glass-card p-4 animate-slide-up">
      <div className="flex gap-3">
        {/* Vote Controls */}
        <div className="flex-shrink-0 pt-0.5">
          <VoteControls
            commentId={comment.id}
            upvotes={comment.upvotes || 0}
            downvotes={comment.downvotes || 0}
            layout="vertical"
          />
        </div>

        {/* Comment Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-7 h-7 bg-dark-700 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-xs font-semibold text-civic-400">
                {comment.username?.charAt(0).toUpperCase() || '?'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-dark-200">{comment.username}</span>
              <span className="text-xs text-dark-500">{formatDateTime(comment.createdAt)}</span>
            </div>
          </div>
          <p className="text-sm text-dark-300 leading-relaxed">{comment.body}</p>
        </div>
      </div>
    </div>
  )
}
