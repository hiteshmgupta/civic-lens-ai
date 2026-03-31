package com.civiclens.comment;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface CommentRepository extends JpaRepository<Comment, Long> {
    Page<Comment> findByAmendmentId(Long amendmentId, Pageable pageable);
    List<Comment> findByAmendmentId(Long amendmentId);
    int countByAmendmentId(Long amendmentId);

    @Query(value = "SELECT TO_CHAR(c.created_at, 'YYYY-MM') AS period, COUNT(*) AS cnt " +
            "FROM comments c GROUP BY period ORDER BY period", nativeQuery = true)
    List<Object[]> countGroupedByMonth();
}
