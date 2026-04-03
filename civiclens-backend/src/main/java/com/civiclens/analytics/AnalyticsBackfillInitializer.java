package com.civiclens.analytics;

import com.civiclens.amendment.Amendment;
import com.civiclens.amendment.AmendmentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class AnalyticsBackfillInitializer {

    private final AmendmentRepository amendmentRepository;
    private final AnalyticsSyncService analyticsSyncService;

    @EventListener(ApplicationReadyEvent.class)
    public void queueBackfill() {
        queueBackfillInternal("startup-backfill");
    }

    @Scheduled(fixedDelayString = "${analytics.refresh.interval-ms:180000}", initialDelayString = "${analytics.refresh.initial-delay-ms:45000}")
    public void queuePeriodicBackfill() {
        queueBackfillInternal("periodic-backfill");
    }

    private void queueBackfillInternal(String reason) {
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
    }
}
