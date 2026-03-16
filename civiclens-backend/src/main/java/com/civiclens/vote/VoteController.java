package com.civiclens.vote;

import com.civiclens.vote.dto.VoteRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/comments/{commentId}/vote")
@RequiredArgsConstructor
public class VoteController {

    private final VoteService voteService;

    @PostMapping
    public ResponseEntity<Void> vote(
            @PathVariable Long commentId,
            @Valid @RequestBody VoteRequest request,
            Authentication auth) {
        voteService.vote(commentId, request, auth.getName());
        return ResponseEntity.ok().build();
    }

    @DeleteMapping
    public ResponseEntity<Void> removeVote(
            @PathVariable Long commentId,
            Authentication auth) {
        voteService.removeVote(commentId, auth.getName());
        return ResponseEntity.ok().build();
    }
}
