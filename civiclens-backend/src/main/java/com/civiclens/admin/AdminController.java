package com.civiclens.admin;

import com.civiclens.admin.dto.DashboardResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
@PreAuthorize("hasAuthority('ADMIN')")
public class AdminController {

    private final AdminService adminService;
    private final com.civiclens.amendment.AmendmentService amendmentService;

    @GetMapping("/dashboard")
    public ResponseEntity<DashboardResponse> dashboard() {
        return ResponseEntity.ok(adminService.getDashboard());
    }

    @DeleteMapping("/amendments/{id}")
    public ResponseEntity<Void> deleteAmendment(@PathVariable Long id) {
        amendmentService.deleteAmendment(id);
        return ResponseEntity.noContent().build();
    }
}
