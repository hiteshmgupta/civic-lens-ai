package com.civiclens.analytics;

import com.civiclens.analytics.dto.AiAnalysisRequest;
import com.civiclens.analytics.dto.AiAnalysisResponse;
import io.netty.channel.ChannelOption;
import io.netty.handler.timeout.ReadTimeoutHandler;
import io.netty.handler.timeout.WriteTimeoutHandler;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

@Component
@Slf4j
public class AiServiceClient {

    private final WebClient webClient;

    public AiServiceClient(@Value("${app.ai.service-url}") String aiServiceUrl) {
        // Configure HttpClient with long timeouts for Render's cold starts
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 60000) // 60s connection timeout
                .responseTimeout(Duration.ofSeconds(60))            // 60s total response timeout
                .doOnConnected(conn -> conn
                        .addHandlerLast(new ReadTimeoutHandler(60, TimeUnit.SECONDS))
                        .addHandlerLast(new WriteTimeoutHandler(60, TimeUnit.SECONDS)));

        this.webClient = WebClient.builder()
                .baseUrl(aiServiceUrl)
                .clientConnector(new ReactorClientHttpConnector(httpClient))
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
                    .block(); // Blocks until 60s timeout is reached
            
            log.info("AI analysis completed for amendment {}", request.getAmendmentId());
            return response;
        } catch (Exception e) {
            log.error("AI service call failed for amendment {}: {}", request.getAmendmentId(), e.getMessage());
            throw new RuntimeException("AI service unavailable or timed out: " + e.getMessage(), e);
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
            log.warn("AI Health check failed: {}", e.getMessage());
            return false;
        }
    }
}