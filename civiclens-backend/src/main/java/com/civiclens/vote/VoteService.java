package com.civiclens.vote;

import com.civiclens.amendment.AmendmentStatus;
import com.civiclens.comment.Comment;
import com.civiclens.comment.CommentRepository;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import com.civiclens.vote.dto.VoteRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class VoteService {

    private final VoteRepository voteRepository;
    private final CommentRepository commentRepository;
    private final UserRepository userRepository;

    @Transactional
    public void vote(Long commentId, VoteRequest request, String userEmail) {
        if (request.getValue() != 1 && request.getValue() != -1) {
            throw new IllegalArgumentException("Vote value must be 1 or -1");
        }

        Comment comment = commentRepository.findById(commentId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment not found"));

        if (comment.getAmendment().getStatus() == AmendmentStatus.CLOSED) {
            throw new IllegalArgumentException("Cannot vote on a comment under a closed amendment");
        }

        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Optional<Vote> existing = voteRepository.findByUserIdAndCommentId(user.getId(), commentId);

        if (existing.isPresent()) {
            Vote vote = existing.get();
            if (vote.getValue() == request.getValue()) {
                // Same vote = toggle off (remove)
                voteRepository.delete(vote);
                log.info("Vote removed: user={}, comment={}", user.getId(), commentId);
            } else {
                // Different vote = update
                vote.setValue(request.getValue());
                voteRepository.save(vote);
                log.info("Vote changed: user={}, comment={}, value={}", user.getId(), commentId,
                        request.getValue());
            }
        } else {
            Vote vote = Vote.builder()
                    .user(user)
                    .comment(comment)
                    .value(request.getValue())
                    .build();
            voteRepository.save(vote);
            log.info("Vote cast: user={}, comment={}, value={}", user.getId(), commentId, request.getValue());
        }
    }

    @Transactional
    public void removeVote(Long commentId, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Vote vote = voteRepository.findByUserIdAndCommentId(user.getId(), commentId)
                .orElseThrow(() -> new ResourceNotFoundException("Vote not found"));

        voteRepository.delete(vote);
        log.info("Vote removed: user={}, comment={}", user.getId(), commentId);
    }
}
