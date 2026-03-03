package com.civiclens.vote;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface VoteRepository extends JpaRepository<Vote, Long> {

    Optional<Vote> findByUserIdAndAmendmentId(Long userId, Long amendmentId);

    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = 1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.amendment.id = :amendmentId")
    int countUpvotes(@Param("amendmentId") Long amendmentId);

    @Query("SELECT COALESCE(SUM(CASE WHEN v.value = -1 THEN 1 ELSE 0 END), 0) FROM Vote v WHERE v.amendment.id = :amendmentId")
    int countDownvotes(@Param("amendmentId") Long amendmentId);

    boolean existsByUserIdAndAmendmentId(Long userId, Long amendmentId);
}
