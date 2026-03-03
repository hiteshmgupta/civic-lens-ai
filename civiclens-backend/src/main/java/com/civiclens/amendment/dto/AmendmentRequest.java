package com.civiclens.amendment.dto;

import com.civiclens.amendment.AmendmentCategory;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDateTime;

@Data
public class AmendmentRequest {
    @NotBlank
    private String title;

    @NotBlank
    private String body;

    @NotNull
    private AmendmentCategory category;

    private LocalDateTime closesAt;
}
