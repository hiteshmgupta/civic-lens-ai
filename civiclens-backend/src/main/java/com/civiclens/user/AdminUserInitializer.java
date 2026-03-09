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
        // Hardcoded admin user
        String adminEmail = "admin@gmail.com";
        String adminUsername = "admin";
        String adminPassword = "admin@123";

        userRepository.findByEmail(adminEmail).orElseGet(() -> {
            log.info("Creating hardcoded ADMIN user with email={}", adminEmail);
            User admin = User.builder()
                    .username(adminUsername)
                    .email(adminEmail)
                    .passwordHash(passwordEncoder.encode(adminPassword))
                    .role(UserRole.ADMIN)
                    .build();
            return userRepository.save(admin);
        });

        // Hardcoded normal user
        String userEmail = "user@gmail.com";
        String userUsername = "user";
        String userPassword = "user@123";

        userRepository.findByEmail(userEmail).orElseGet(() -> {
            log.info("Creating hardcoded USER with email={}", userEmail);
            User user = User.builder()
                    .username(userUsername)
                    .email(userEmail)
                    .passwordHash(passwordEncoder.encode(userPassword))
                    .role(UserRole.USER)
                    .build();
            return userRepository.save(user);
        });
    }
}

