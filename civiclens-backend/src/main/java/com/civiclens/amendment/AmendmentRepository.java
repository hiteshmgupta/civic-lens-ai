package com.civiclens.amendment;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface AmendmentRepository extends JpaRepository<Amendment, Long> {

    Page<Amendment> findByStatus(AmendmentStatus status, Pageable pageable);

    Page<Amendment> findByCategory(AmendmentCategory category, Pageable pageable);

    Page<Amendment> findByStatusAndCategory(AmendmentStatus status, AmendmentCategory category, Pageable pageable);

    @Query("SELECT a FROM Amendment a WHERE a.status = 'ACTIVE' AND a.closesAt IS NOT NULL AND a.closesAt <= CURRENT_TIMESTAMP")
    List<Amendment> findExpiredAmendments();

    long countByStatus(AmendmentStatus status);
}
