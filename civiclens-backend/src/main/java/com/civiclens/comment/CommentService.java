package com.civiclens.comment;

import com.civiclens.amendment.*;
import com.civiclens.comment.dto.*;
import com.civiclens.common.dto.PagedResponse;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class CommentService {

    private final CommentRepository commentRepository;
    private final AmendmentRepository amendmentRepository;
    private final UserRepository userRepository;

    @Transactional
    public CommentResponse create(Long amendmentId, CommentRequest request, String userEmail) {
        Amendment amendment = amendmentRepository.findById(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found"));

        if (amendment.getStatus() == AmendmentStatus.CLOSED) {
            throw new IllegalArgumentException("Cannot comment on a closed amendment");
        }

        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Comment comment = Comment.builder()
                .amendment(amendment)
                .user(user)
                .body(request.getBody())
                .build();

        comment = commentRepository.save(comment);
        log.info("Comment added: amendment={}, user={}", amendmentId, user.getId());

        return toResponse(comment);
    }

    public PagedResponse<CommentResponse> list(Long amendmentId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<Comment> comments = commentRepository.findByAmendmentId(amendmentId, pageable);

        List<CommentResponse> content = comments.getContent().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());

        return PagedResponse.<CommentResponse>builder()
                .content(content)
                .page(comments.getNumber())
                .size(comments.getSize())
                .totalElements(comments.getTotalElements())
                .totalPages(comments.getTotalPages())
                .last(comments.isLast())
                .build();
    }

    private CommentResponse toResponse(Comment c) {
        return CommentResponse.builder()
                .id(c.getId())
                .body(c.getBody())
                .username(c.getUser().getUsername())
                .createdAt(c.getCreatedAt())
                .build();
    }
}
