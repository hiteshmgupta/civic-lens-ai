package com.civiclens.analytics;

import com.civiclens.analytics.dto.AnalyticsResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    @GetMapping("/api/amendments/{id}/analytics")
    public ResponseEntity<AnalyticsResponse> getAnalytics(@PathVariable Long id) {
        return ResponseEntity.ok(analyticsService.getAnalytics(id));
    }

    @PostMapping("/api/admin/amendments/{id}/analyze")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<AnalyticsResponse> triggerAnalysis(@PathVariable Long id) {
        return ResponseEntity.ok(analyticsService.triggerAnalysis(id));
    }
}
