package com.civiclens.analytics;

import com.civiclens.amendment.Amendment;
import com.civiclens.amendment.AmendmentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
@ConditionalOnProperty(
    name = "analytics.backfill.enabled",
    havingValue = "true",
    matchIfMissing = false  // Disabled by default
)
public class AnalyticsBackfillInitializer {

    private final AmendmentRepository amendmentRepository;
    private final AnalyticsSyncService analyticsSyncService;

    @Scheduled(fixedDelayString = "${analytics.refresh.interval-ms:180000}", initialDelayString = "${analytics.refresh.initial-delay-ms:45000}")
    public void queuePeriodicBackfill() {
        try {
            queueBackfillInternal("periodic-backfill");
        } catch (Exception e) {
            log.warn("Failed to queue periodic backfill: {}", e.getMessage(), e);
        }
    }

    private void queueBackfillInternal(String reason) {
        try {
            List<Amendment> amendments = amendmentRepository.findAll();
            int queued = 0;

            for (Amendment amendment : amendments) {
                Long amendmentId = amendment.getId();
                if (analyticsSyncService.isRefreshNeeded(amendmentId)) {
                    analyticsSyncService.requestRefresh(amendmentId, false, reason);
                    queued++;
                }
            }

            if (queued > 0) {
                log.info("Queued {} analytics refresh job(s) out of {} amendments ({})", queued, amendments.size(), reason);
            } else {
                log.debug("No stale analytics found during {}", reason);
            }
        } catch (Exception e) {
            log.error("Error during analytics backfill ({}): {}", reason, e.getMessage(), e);
        }
    }
}
