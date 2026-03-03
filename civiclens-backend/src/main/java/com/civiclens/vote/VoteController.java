package com.civiclens.vote;

import com.civiclens.vote.dto.VoteRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/amendments/{amendmentId}/vote")
@RequiredArgsConstructor
public class VoteController {

    private final VoteService voteService;

    @PostMapping
    public ResponseEntity<Void> vote(
            @PathVariable Long amendmentId,
            @Valid @RequestBody VoteRequest request,
            Authentication auth) {
        voteService.vote(amendmentId, request, auth.getName());
        return ResponseEntity.ok().build();
    }

    @DeleteMapping
    public ResponseEntity<Void> removeVote(
            @PathVariable Long amendmentId,
            Authentication auth) {
        voteService.removeVote(amendmentId, auth.getName());
        return ResponseEntity.ok().build();
    }
}
