package com.civiclens.vote;

import com.civiclens.amendment.*;
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
    private final AmendmentRepository amendmentRepository;
    private final UserRepository userRepository;

    @Transactional
    public void vote(Long amendmentId, VoteRequest request, String userEmail) {
        if (request.getValue() != 1 && request.getValue() != -1) {
            throw new IllegalArgumentException("Vote value must be 1 or -1");
        }

        Amendment amendment = amendmentRepository.findById(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found"));

        if (amendment.getStatus() == AmendmentStatus.CLOSED) {
            throw new IllegalArgumentException("Cannot vote on a closed amendment");
        }

        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Optional<Vote> existing = voteRepository.findByUserIdAndAmendmentId(user.getId(), amendmentId);

        if (existing.isPresent()) {
            Vote vote = existing.get();
            if (vote.getValue() == request.getValue()) {
                // Same vote = toggle off (remove)
                voteRepository.delete(vote);
                log.info("Vote removed: user={}, amendment={}", user.getId(), amendmentId);
            } else {
                // Different vote = update
                vote.setValue(request.getValue());
                voteRepository.save(vote);
                log.info("Vote changed: user={}, amendment={}, value={}", user.getId(), amendmentId,
                        request.getValue());
            }
        } else {
            Vote vote = Vote.builder()
                    .user(user)
                    .amendment(amendment)
                    .value(request.getValue())
                    .build();
            voteRepository.save(vote);
            log.info("Vote cast: user={}, amendment={}, value={}", user.getId(), amendmentId, request.getValue());
        }
    }

    @Transactional
    public void removeVote(Long amendmentId, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Vote vote = voteRepository.findByUserIdAndAmendmentId(user.getId(), amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Vote not found"));

        voteRepository.delete(vote);
        log.info("Vote removed: user={}, amendment={}", user.getId(), amendmentId);
    }
}
