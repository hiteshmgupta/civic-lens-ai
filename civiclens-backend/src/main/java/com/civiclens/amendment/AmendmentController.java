package com.civiclens.amendment;

import com.civiclens.amendment.dto.*;
import com.civiclens.common.dto.PagedResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/amendments")
@RequiredArgsConstructor
public class AmendmentController {

    private final AmendmentService amendmentService;

    @GetMapping
    public ResponseEntity<PagedResponse<AmendmentResponse>> list(
            @RequestParam(required = false) String sort,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return ResponseEntity.ok(amendmentService.list(sort, category, status, page, size));
    }

    @GetMapping("/{id}")
    public ResponseEntity<AmendmentResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(amendmentService.getById(id));
    }

    @PostMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<AmendmentResponse> create(
            @Valid @RequestBody AmendmentRequest request,
            Authentication auth) {
        return ResponseEntity.ok(amendmentService.create(request, auth.getName()));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<AmendmentResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody AmendmentRequest request) {
        return ResponseEntity.ok(amendmentService.update(id, request));
    }
}
