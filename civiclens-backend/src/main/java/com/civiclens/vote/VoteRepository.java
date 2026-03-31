package com.civiclens.vote;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface VoteRepository extends JpaRepository<Vote, Long> {

    // Per-comment vote lookup (for casting / removing a vote)
    Optional<Vote> findByUserIdAndCommentId(Long userId, Long commentId);
    boolean existsByUserIdAndCommentId(Long userId, Long commentId);

    @org.springframework.data.jpa.repository.Modifying
    @Query("DELETE FROM Vote v WHERE v.comment.id IN (SELECT c.id FROM Comment c WHERE c.amendment.id = :amendmentId)")
    void deleteByAmendmentId(@Param("amendmentId") Long amendmentId);

    // Per-comment vote counts
    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = 1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.comment.id = :commentId")
    int countUpvotesByCommentId(@Param("commentId") Long commentId);

    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = -1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.comment.id = :commentId")
    int countDownvotesByCommentId(@Param("commentId") Long commentId);

    // Per-amendment vote counts (aggregated through comments)
    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = 1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.comment.amendment.id = :amendmentId")
    int countUpvotesByAmendmentId(@Param("amendmentId") Long amendmentId);

    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = -1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.comment.amendment.id = :amendmentId")
    int countDownvotesByAmendmentId(@Param("amendmentId") Long amendmentId);

    @Query(value = "SELECT TO_CHAR(cv.created_at, 'YYYY-MM') AS period, COUNT(*) AS cnt " +
            "FROM comment_votes cv GROUP BY period ORDER BY period", nativeQuery = true)
    List<Object[]> countGroupedByMonth();
}
