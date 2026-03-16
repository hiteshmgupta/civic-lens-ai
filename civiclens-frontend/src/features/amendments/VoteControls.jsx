import { useState } from 'react'
import { vote as voteApi, removeVote } from '../../api/voteApi'
import { useAuth } from '../../context/AuthContext'

export default function VoteControls({ commentId, upvotes: initUp, downvotes: initDown, userVote: initVote, layout = 'horizontal' }) {
  const { user } = useAuth()
  const [upvotes, setUpvotes] = useState(initUp || 0)
  const [downvotes, setDownvotes] = useState(initDown || 0)
  const [userVote, setUserVote] = useState(initVote || 0) // 1, -1, or 0
  const [loading, setLoading] = useState(false)

  const handleVote = async (value) => {
    if (!user) return
    if (loading) return

    setLoading(true)
    try {
      if (userVote === value) {
        // Remove vote
        await removeVote(commentId)
        if (value === 1) setUpvotes(prev => prev - 1)
        else setDownvotes(prev => prev - 1)
        setUserVote(0)
      } else {
        if (userVote === 1) setUpvotes(prev => prev - 1)
        else if (userVote === -1) setDownvotes(prev => prev - 1)

        await voteApi(commentId, value)
        if (value === 1) setUpvotes(prev => prev + 1)
        else setDownvotes(prev => prev + 1)
        setUserVote(value)
      }
    } catch (err) {
      console.error('Vote failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const net = upvotes - downvotes
  const isVertical = layout === 'vertical'

  return (
    <div className={`flex items-center gap-1 ${isVertical ? 'flex-col' : 'flex-row'}`}>
      {/* Upvote */}
      <button
        onClick={() => handleVote(1)}
        disabled={!user || loading}
        className={`group p-1.5 rounded-lg transition-all duration-200 ${
          userVote === 1
            ? 'bg-civic-400/20 text-civic-400'
            : 'text-dark-500 hover:text-civic-400 hover:bg-civic-400/10'
        } disabled:opacity-40 disabled:cursor-not-allowed`}
        title={user ? 'Upvote' : 'Login to vote'}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="transition-transform duration-200 group-active:scale-90">
          <path d="M12 19V5M5 12l7-7 7 7" />
        </svg>
      </button>

      {/* Score */}
      <span className={`text-xs font-bold font-mono min-w-[2ch] text-center ${
        net > 0 ? 'text-civic-400' : net < 0 ? 'text-rose-400' : 'text-dark-400'
      }`}>
        {net > 0 ? `+${net}` : net}
      </span>

      {/* Downvote */}
      <button
        onClick={() => handleVote(-1)}
        disabled={!user || loading}
        className={`group p-1.5 rounded-lg transition-all duration-200 ${
          userVote === -1
            ? 'bg-rose-400/20 text-rose-400'
            : 'text-dark-500 hover:text-rose-400 hover:bg-rose-400/10'
        } disabled:opacity-40 disabled:cursor-not-allowed`}
        title={user ? 'Downvote' : 'Login to vote'}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="transition-transform duration-200 group-active:scale-90">
          <path d="M12 5v14M19 12l-7 7-7-7" />
        </svg>
      </button>
    </div>
  )
}
