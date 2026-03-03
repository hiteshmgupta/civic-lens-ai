package com.civiclens.comment;

import com.civiclens.comment.dto.*;
import com.civiclens.common.dto.PagedResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/amendments/{amendmentId}/comments")
@RequiredArgsConstructor
public class CommentController {

    private final CommentService commentService;

    @GetMapping
    public ResponseEntity<PagedResponse<CommentResponse>> list(
            @PathVariable Long amendmentId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return ResponseEntity.ok(commentService.list(amendmentId, page, size));
    }

    @PostMapping
    public ResponseEntity<CommentResponse> create(
            @PathVariable Long amendmentId,
            @Valid @RequestBody CommentRequest request,
            Authentication auth) {
        return ResponseEntity.ok(commentService.create(amendmentId, request, auth.getName()));
    }
}
