package com.civiclens.analytics;

import com.civiclens.analytics.dto.AiAnalysisRequest;
import com.civiclens.analytics.dto.AiAnalysisResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
@Slf4j
public class AiServiceClient {

    private final WebClient webClient;

    public AiServiceClient(@Value("${app.ai.service-url}") String aiServiceUrl) {
        this.webClient = WebClient.builder()
                .baseUrl(aiServiceUrl)
                .build();
    }

    public AiAnalysisResponse analyze(AiAnalysisRequest request) {
        log.info("Calling AI service for amendment {}", request.getAmendmentId());
        try {
            AiAnalysisResponse response = webClient.post()
                    .uri("/ai/analyze")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(AiAnalysisResponse.class)
                    .block();
            log.info("AI analysis completed for amendment {}", request.getAmendmentId());
            return response;
        } catch (Exception e) {
            log.error("AI service call failed for amendment {}: {}", request.getAmendmentId(), e.getMessage());
            throw new RuntimeException("AI service unavailable: " + e.getMessage(), e);
        }
    }

    public boolean isHealthy() {
        try {
            webClient.get()
                    .uri("/ai/health")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
