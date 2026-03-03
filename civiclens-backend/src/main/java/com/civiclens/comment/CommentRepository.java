package com.civiclens.comment;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CommentRepository extends JpaRepository<Comment, Long> {
    Page<Comment> findByAmendmentId(Long amendmentId, Pageable pageable);
    List<Comment> findByAmendmentId(Long amendmentId);
    int countByAmendmentId(Long amendmentId);
}
