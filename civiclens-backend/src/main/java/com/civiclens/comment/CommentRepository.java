package com.civiclens.comment;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CommentRepository extends JpaRepository<Comment, Long> {
    Page<Comment> findByAmendmentId(Long amendmentId, Pageable pageable);
    List<Comment> findByAmendmentId(Long amendmentId);
    int countByAmendmentId(Long amendmentId);

    @Query("SELECT COALESCE(SUM(c.upvoteCount), 0) FROM Comment c WHERE c.amendment.id = :amendmentId")
    int sumUpvotesByAmendmentId(@Param("amendmentId") Long amendmentId);

    @Query("SELECT COALESCE(SUM(c.downvoteCount), 0) FROM Comment c WHERE c.amendment.id = :amendmentId")
    int sumDownvotesByAmendmentId(@Param("amendmentId") Long amendmentId);

    @org.springframework.data.jpa.repository.Modifying
    @Query("DELETE FROM Comment c WHERE c.amendment.id = :amendmentId")
    void deleteByAmendmentId(@Param("amendmentId") Long amendmentId);

    @Query(value = "SELECT TO_CHAR(c.created_at, 'YYYY-MM') AS period, COUNT(*) AS cnt " +
            "FROM comments c GROUP BY period ORDER BY period", nativeQuery = true)
    List<Object[]> countGroupedByMonth();

    @Query("SELECT COALESCE(SUM(c.upvoteCount), 0) FROM Comment c")
    long sumAllUpvotes();

    @Query("SELECT COALESCE(SUM(c.downvoteCount), 0) FROM Comment c")
    long sumAllDownvotes();

    @Query(value = "SELECT TO_CHAR(c.created_at, 'YYYY-MM') AS period, " +
            "COALESCE(SUM(c.upvote_count + c.downvote_count), 0) AS cnt " +
            "FROM comments c GROUP BY period ORDER BY period", nativeQuery = true)
    List<Object[]> sumVotesGroupedByMonth();
}
