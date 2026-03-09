package com.civiclens.user;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class AdminUserInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        // Hardcoded admin user (always enforce same password/role)
        String adminEmail = "admin@gmail.com";
        String adminUsername = "admin";
        String adminPassword = "admin@123";

        userRepository.findByEmail(adminEmail).ifPresentOrElse(existing -> {
            existing.setUsername(adminUsername);
            existing.setPasswordHash(passwordEncoder.encode(adminPassword));
            existing.setRole(UserRole.ADMIN);
            userRepository.save(existing);
            log.info("Updated hardcoded ADMIN user with email={}", adminEmail);
        }, () -> {
            log.info("Creating hardcoded ADMIN user with email={}", adminEmail);
            User admin = User.builder()
                    .username(adminUsername)
                    .email(adminEmail)
                    .passwordHash(passwordEncoder.encode(adminPassword))
                    .role(UserRole.ADMIN)
                    .build();
            userRepository.save(admin);
        });

        // Hardcoded normal user (always enforce same password/role)
        String userEmail = "user@gmail.com";
        String userUsername = "user";
        String userPassword = "user@123";

        userRepository.findByEmail(userEmail).ifPresentOrElse(existing -> {
            existing.setUsername(userUsername);
            existing.setPasswordHash(passwordEncoder.encode(userPassword));
            existing.setRole(UserRole.USER);
            userRepository.save(existing);
            log.info("Updated hardcoded USER with email={}", userEmail);
        }, () -> {
            log.info("Creating hardcoded USER with email={}", userEmail);
            User user = User.builder()
                    .username(userUsername)
                    .email(userEmail)
                    .passwordHash(passwordEncoder.encode(userPassword))
                    .role(UserRole.USER)
                    .build();
            userRepository.save(user);
        });
    }
}

