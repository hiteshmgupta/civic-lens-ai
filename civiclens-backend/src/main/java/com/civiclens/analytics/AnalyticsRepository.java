package com.civiclens.analytics;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface AnalyticsRepository extends JpaRepository<AmendmentAnalytics, Long> {
    Optional<AmendmentAnalytics> findByAmendmentId(Long amendmentId);
}
