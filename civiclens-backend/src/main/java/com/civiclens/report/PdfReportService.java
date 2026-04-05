package com.civiclens.report;

import com.civiclens.analytics.*;
import com.civiclens.amendment.*;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.openhtmltopdf.pdfboxout.PdfRendererBuilder;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class PdfReportService {

    private final AnalyticsRepository analyticsRepository;
    private final AmendmentRepository amendmentRepository;

    public byte[] generateReport(Long amendmentId) {
        Amendment amendment = amendmentRepository.findById(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found"));

        AmendmentAnalytics analytics = analyticsRepository.findByAmendmentId(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Analytics not found for amendment"));

        String html = buildReportHtml(amendment, analytics);

        try (ByteArrayOutputStream os = new ByteArrayOutputStream()) {
            PdfRendererBuilder builder = new PdfRendererBuilder();
            builder.useFastMode();
            builder.withHtmlContent(html, null);
            builder.toStream(os);
            builder.run();
            log.info("PDF report generated for amendment {}", amendmentId);
            return os.toByteArray();
        } catch (Exception e) {
            log.error("Failed to generate PDF for amendment {}", amendmentId, e);
            throw new RuntimeException("PDF generation failed", e);
        }
    }

    private String buildReportHtml(Amendment amendment, AmendmentAnalytics a) {
        String date = LocalDateTime.now().format(DateTimeFormatter.ofPattern("MMMM dd, yyyy"));
        String computedDate = a.getLastComputedAt() != null
                ? a.getLastComputedAt().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"))
                : "N/A";

        StringBuilder sb = new StringBuilder();
        sb.append("<!DOCTYPE html><html><head><style>");
        sb.append(getReportCss());
        sb.append("</style></head><body>");

        // Cover Page
        sb.append("<div class='cover'>");
        sb.append("<div class='gov-header'>LEGISLATIVE CONSULTATION INTELLIGENCE REPORT</div>");
        sb.append("<div class='gov-seal'>&#9878; CivicLens Intelligence Platform</div>");
        sb.append("<h1 class='title'>").append(esc(amendment.getTitle())).append("</h1>");
        sb.append("<div class='meta'>Category: ").append(amendment.getCategory()).append("</div>");
        sb.append("<div class='meta'>Report Date: ").append(date).append("</div>");
        sb.append("<div class='meta'>Analysis Computed: ").append(computedDate).append("</div>");
        sb.append("<div class='meta'>Document Classification: OFFICIAL — FOR DECISION SUPPORT</div>");
        sb.append("<div class='classification'>UNCLASSIFIED // CIVIC INTELLIGENCE</div>");
        sb.append("</div>");

        sb.append("<div class='page-break'></div>");

        // Executive Summary
        sb.append("<h2>1. Executive Summary</h2>");
        sb.append("<div class='section'>");
        if (a.getPolicyBrief() != null) {
            sb.append("<p>").append(esc(a.getPolicyBrief())).append("</p>");
        } else {
            sb.append("<p>No policy brief available.</p>");
        }
        sb.append("</div>");

        // Engagement Metrics
        sb.append("<h2>2. Engagement Metrics</h2>");
        sb.append("<table><tr><th>Metric</th><th>Value</th></tr>");
        sb.append("<tr><td>Total Comments</td><td>").append(a.getTotalComments()).append("</td></tr>");
        sb.append("<tr><td>Total Votes</td><td>").append(a.getTotalVotes()).append("</td></tr>");
        sb.append("<tr><td>Upvotes</td><td>").append(a.getUpvotes()).append("</td></tr>");
        sb.append("<tr><td>Downvotes</td><td>").append(a.getDownvotes()).append("</td></tr>");
        sb.append("<tr><td>Engagement Score</td><td>").append(fmt(a.getEngagementScore())).append("</td></tr>");
        sb.append("</table>");

        // Sentiment Breakdown
        sb.append("<h2>3. Sentiment Analysis</h2>");
        sb.append("<table><tr><th>Metric</th><th>Value</th></tr>");
        sb.append("<tr><td>Mean Sentiment</td><td>").append(fmt(a.getSentimentMean())).append("</td></tr>");
        sb.append("<tr><td>Sentiment Variance (S)</td><td>").append(fmt(a.getSentimentVariance())).append("</td></tr>");
        sb.append("</table>");
        if (a.getSentimentDistribution() != null) {
            sb.append("<h3>Distribution</h3><table><tr><th>Sentiment</th><th>Count</th></tr>");
            a.getSentimentDistribution().forEach(
                    (k, v) -> sb.append("<tr><td>").append(esc(k)).append("</td><td>").append(v).append("</td></tr>"));
            sb.append("</table>");
        }

        // Controversy Index
        sb.append("<h2>4. Controversy Index</h2>");
        sb.append("<div class='highlight'>Score: ").append(fmt(a.getControversyScore()))
                .append(" — ").append(esc(a.getControversyLabel())).append("</div>");
        sb.append("<table><tr><th>Component</th><th>Value</th><th>Description</th></tr>");
        sb.append("<tr><td>S (Sentiment Variance)</td><td>").append(fmt(a.getSentimentVariance()))
                .append("</td><td>Emotional dispersion</td></tr>");
        sb.append("<tr><td>P (Vote Polarity)</td><td>").append(fmt(a.getVotePolarity()))
                .append("</td><td>Balance of opposition</td></tr>");
        sb.append("<tr><td>D (Stance Entropy)</td><td>").append(fmt(a.getStanceEntropy()))
                .append("</td><td>Diversity of disagreement</td></tr>");
        sb.append("<tr><td>E (Engagement)</td><td>").append(fmt(a.getEngagementScore()))
                .append("</td><td>Participation intensity</td></tr>");
        sb.append("</table>");
        sb.append("<p><em>Formula: C(a) = S · P · D · √E ∈ [0,1]</em></p>");

        // Topic Ranking
        sb.append("<h2>5. Topic Clusters</h2>");
        if (a.getTopicClusters() != null && !a.getTopicClusters().isEmpty()) {
            sb.append("<table><tr><th>#</th><th>Topic</th><th>Size</th></tr>");
            int i = 1;
            for (Map<String, Object> cluster : a.getTopicClusters()) {
                sb.append("<tr><td>").append(i++).append("</td>");
                sb.append("<td>").append(esc(String.valueOf(cluster.getOrDefault("topic", "N/A")))).append("</td>");
                sb.append("<td>").append(cluster.getOrDefault("size", "—")).append("</td></tr>");
            }
            sb.append("</table>");
        }

        // Arguments
        sb.append("<h2>6. Structured Arguments</h2>");
        sb.append("<h3>Top Supporting Arguments</h3><ol>");
        if (a.getTopSupporting() != null) {
            a.getTopSupporting().forEach(arg -> sb.append("<li>").append(esc(arg)).append("</li>"));
        }
        sb.append("</ol>");
        sb.append("<h3>Top Opposing Arguments</h3><ol>");
        if (a.getTopOpposing() != null) {
            a.getTopOpposing().forEach(arg -> sb.append("<li>").append(esc(arg)).append("</li>"));
        }
        sb.append("</ol>");

        // Risk Assessment
        sb.append("<h2>7. Risk Assessment</h2>");
        sb.append("<div class='section'>");
        double c = a.getControversyScore() != null ? a.getControversyScore() : 0;
        if (c > 0.75) {
            sb.append(
                    "<p class='risk-high'>HIGH RISK — Extreme public controversy detected. Recommend further stakeholder consultation before proceeding.</p>");
        } else if (c > 0.50) {
            sb.append(
                    "<p class='risk-med'>MODERATE–HIGH RISK — Significant disagreement exists. Policy revision may be needed.</p>");
        } else if (c > 0.25) {
            sb.append(
                    "<p class='risk-low'>LOW–MODERATE RISK — Some disagreement, but manageable through communication.</p>");
        } else {
            sb.append("<p class='risk-min'>LOW RISK — Broad consensus observed.</p>");
        }
        sb.append("</div>");

        // Appendix
        sb.append("<h2>8. Appendix — Metadata</h2>");
        sb.append("<table><tr><th>Field</th><th>Value</th></tr>");
        sb.append("<tr><td>Amendment ID</td><td>").append(a.getAmendment().getId()).append("</td></tr>");
        sb.append("<tr><td>Status</td><td>").append(a.getAmendment().getStatus()).append("</td></tr>");
        sb.append("<tr><td>Created</td><td>").append(a.getAmendment().getCreatedAt()).append("</td></tr>");
        sb.append("<tr><td>Closes At</td><td>")
                .append(a.getAmendment().getClosesAt() != null ? a.getAmendment().getClosesAt() : "No expiry")
                .append("</td></tr>");
        sb.append("<tr><td>Last Analysis</td><td>").append(computedDate).append("</td></tr>");
        sb.append("</table>");

        sb.append("<div class='footer'>Generated by CivicLens Intelligence Platform — ").append(date).append("</div>");
        sb.append("</body></html>");
        return sb.toString();
    }

    private String getReportCss() {
        return """
                body { font-family: 'Times New Roman', serif; color: #1a1a2e; margin: 40px; line-height: 1.6; }
                .cover { text-align: center; padding: 80px 20px; }
                .gov-header { font-size: 14px; letter-spacing: 4px; color: #16213e; text-transform: uppercase; margin-bottom: 40px; border-top: 3px solid #0f3460; border-bottom: 3px solid #0f3460; padding: 10px; }
                .gov-seal { font-size: 24px; margin: 30px 0; color: #0f3460; }
                .title { font-size: 28px; color: #0f3460; margin: 30px 0; }
                .meta { font-size: 13px; color: #555; margin: 5px 0; }
                .classification { margin-top: 40px; font-size: 11px; letter-spacing: 3px; color: #888; }
                h2 { color: #0f3460; border-bottom: 2px solid #e94560; padding-bottom: 5px; margin-top: 30px; }
                h3 { color: #16213e; }
                table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px; }
                th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
                th { background-color: #0f3460; color: white; }
                tr:nth-child(even) { background: #f4f4f8; }
                .highlight { background: #fff3cd; padding: 15px; border-left: 4px solid #e94560; font-size: 18px; font-weight: bold; margin: 15px 0; }
                .section { margin: 10px 0; }
                .risk-high { color: #dc3545; font-weight: bold; }
                .risk-med { color: #fd7e14; font-weight: bold; }
                .risk-low { color: #ffc107; }
                .risk-min { color: #28a745; }
                .footer { text-align: center; font-size: 11px; color: #888; margin-top: 50px; border-top: 1px solid #ccc; padding-top: 10px; }
                .page-break { page-break-after: always; }
                ol { margin: 10px 0 10px 20px; }
                li { margin: 5px 0; }
                """;
    }

    private String fmt(Double val) {
        return val != null ? String.format("%.4f", val) : "N/A";
    }

    private String esc(String s) {
        if (s == null)
            return "";
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }
}
