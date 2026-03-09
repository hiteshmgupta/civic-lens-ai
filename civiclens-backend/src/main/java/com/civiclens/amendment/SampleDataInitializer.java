package com.civiclens.amendment;

import com.civiclens.comment.Comment;
import com.civiclens.comment.CommentRepository;
import com.civiclens.user.User;
import com.civiclens.user.UserRepository;
import com.civiclens.user.UserRole;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
@Slf4j
public class SampleDataInitializer implements CommandLineRunner {

    private final AmendmentRepository amendmentRepository;
    private final CommentRepository commentRepository;
    private final UserRepository userRepository;

    @Override
    public void run(String... args) {
        if (amendmentRepository.count() > 0) {
            // Don't add sample data if there are already amendments in the DB
            return;
        }

        // Use the hardcoded admin and user created by AdminUserInitializer
        User admin = userRepository.findByEmail("admin@gmail.com")
                .orElseThrow(() -> new IllegalStateException("Expected hardcoded admin user to exist"));

        User user = userRepository.findByEmail("user@gmail.com")
                .orElseThrow(() -> new IllegalStateException("Expected hardcoded user to exist"));

        // Amendment 1 – Digital Privacy
        Amendment privacy = Amendment.builder()
                .title("Data Protection and Digital Privacy Amendment")
                .body("""
This amendment proposes stricter limits on how government agencies and private platforms
can collect and store citizens' personal data. It introduces:
- mandatory deletion of inactive user data after 2 years,
- clear opt-in consent for data sharing with third parties,
- a right for citizens to request a full export of their stored data.
""")
                .category(AmendmentCategory.DIGITAL_PRIVACY)
                .status(AmendmentStatus.ACTIVE)
                .createdAt(LocalDateTime.now().minusDays(5))
                .closesAt(LocalDateTime.now().plusDays(10))
                .createdBy(admin)
                .build();
        privacy = amendmentRepository.save(privacy);

        commentRepository.save(Comment.builder()
                .user(user)
                .amendment(privacy)
                .body("I support this. Citizens should have clear control over how long platforms keep their data.")
                .build());

        commentRepository.save(Comment.builder()
                .user(admin)
                .amendment(privacy)
                .body("Please clarify how this will impact small startups that rely on analytics data.")
                .build());

        // Amendment 2 – Public Transport & Air Quality
        Amendment transport = Amendment.builder()
                .title("Urban Public Transport and Air Quality Improvement Amendment")
                .body("""
This amendment funds the expansion of electric bus fleets and dedicated bus lanes
in major cities. It also introduces low-emission zones where highly polluting
vehicles will be restricted during peak hours.
""")
                .category(AmendmentCategory.INFRASTRUCTURE)
                .status(AmendmentStatus.ACTIVE)
                .createdAt(LocalDateTime.now().minusDays(3))
                .closesAt(LocalDateTime.now().plusDays(7))
                .createdBy(admin)
                .build();
        transport = amendmentRepository.save(transport);

        commentRepository.save(Comment.builder()
                .user(user)
                .amendment(transport)
                .body("This is good for air quality, but please include subsidies for low-income commuters.")
                .build());

        commentRepository.save(Comment.builder()
                .user(user)
                .amendment(transport)
                .body("Will there be enough charging infrastructure for the new electric buses?")
                .build());

        // Amendment 3 – Education & Digital Skills
        Amendment education = Amendment.builder()
                .title("Digital Skills Curriculum in Public Schools Amendment")
                .body("""
This amendment requires all public secondary schools to introduce a basic digital skills
curriculum. Topics include online safety, critical evaluation of information sources,
and introductory programming.
""")
                .category(AmendmentCategory.EDUCATION)
                .status(AmendmentStatus.ACTIVE)
                .createdAt(LocalDateTime.now().minusDays(1))
                .closesAt(LocalDateTime.now().plusDays(14))
                .createdBy(admin)
                .build();
        education = amendmentRepository.save(education);

        commentRepository.save(Comment.builder()
                .user(user)
                .amendment(education)
                .body("Great idea. Please ensure the curriculum also covers misinformation and deepfakes.")
                .build());

        log.info("Sample amendments and comments created for demo purposes.");
    }
}

