package com.civiclens.amendment;

import com.civiclens.comment.Comment;
import com.civiclens.comment.CommentRepository;
import com.civiclens.user.User;
import com.civiclens.user.UserRepository;
import com.civiclens.user.UserRole;
import com.civiclens.vote.Vote;
import com.civiclens.vote.VoteRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.time.LocalDateTime;
import java.util.*;

@Component
@RequiredArgsConstructor
@Slf4j
public class SampleDataInitializer implements CommandLineRunner {

    private final AmendmentRepository amendmentRepository;
    private final CommentRepository commentRepository;
    private final UserRepository userRepository;
    private final VoteRepository voteRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (amendmentRepository.count() > 0) {
            log.info("Database already has amendments — skipping data seeding.");
            return;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            InputStream is = new ClassPathResource("fcc_dataset.json").getInputStream();
            Map<String, Object> dataset = mapper.readValue(is, new TypeReference<>() {});

            // 1. Create synthetic users
            @SuppressWarnings("unchecked")
            List<Map<String, String>> usersData = (List<Map<String, String>>) dataset.get("users");
            List<User> users = new ArrayList<>();
            for (Map<String, String> u : usersData) {
                String email = u.get("email");
                User user = userRepository.findByEmail(email).orElseGet(() -> {
                    User newUser = User.builder()
                            .username(u.get("username"))
                            .email(email)
                            .passwordHash(passwordEncoder.encode("civiclens@123"))
                            .role(UserRole.USER)
                            .build();
                    return userRepository.save(newUser);
                });
                users.add(user);
            }
            log.info("Created/loaded {} synthetic users", users.size());

            // 2. Get admin user for creating amendments
            User admin = userRepository.findByEmail("admin@gmail.com")
                    .orElseThrow(() -> new IllegalStateException("Expected admin user to exist"));

            // 3. Process each amendment
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> amendments = (List<Map<String, Object>>) dataset.get("amendments");

            int totalComments = 0;
            int totalVotes = 0;

            for (int aIdx = 0; aIdx < amendments.size(); aIdx++) {
                Map<String, Object> amd = amendments.get(aIdx);

                Amendment amendment = Amendment.builder()
                        .title((String) amd.get("title"))
                        .body((String) amd.get("body"))
                        .category(AmendmentCategory.valueOf((String) amd.get("category")))
                        .status(AmendmentStatus.valueOf((String) amd.get("status")))
                        .createdAt(LocalDateTime.now().minusDays(14 - aIdx * 2))
                        .closesAt(LocalDateTime.now().plusDays(30 + aIdx * 5))
                        .createdBy(admin)
                        .build();
                amendment = amendmentRepository.save(amendment);

                // 4. Process comments for this amendment
                @SuppressWarnings("unchecked")
                List<Map<String, Object>> comments = (List<Map<String, Object>>) amd.get("comments");

                for (Map<String, Object> c : comments) {
                    int userIndex = ((Number) c.get("user_index")).intValue();
                    User commentUser = users.get(userIndex % users.size());

                    Comment comment = Comment.builder()
                            .amendment(amendment)
                            .user(commentUser)
                            .body((String) c.get("body"))
                            .build();
                    comment = commentRepository.save(comment);
                    totalComments++;

                    // 5. Generate vote entities for this comment
                    int upvotes = ((Number) c.get("upvotes")).intValue();
                    int downvotes = ((Number) c.get("downvotes")).intValue();

                    // Distribute upvotes across users (round-robin, skip comment author)
                    int voteUserIdx = 0;
                    for (int v = 0; v < upvotes && v < users.size() - 1; v++) {
                        User voter = users.get(voteUserIdx % users.size());
                        if (voter.getId().equals(commentUser.getId())) {
                            voteUserIdx++;
                            voter = users.get(voteUserIdx % users.size());
                        }
                        if (!voteRepository.existsByUserIdAndCommentId(voter.getId(), comment.getId())) {
                            Vote vote = Vote.builder()
                                    .user(voter)
                                    .comment(comment)
                                    .value((short) 1)
                                    .build();
                            voteRepository.save(vote);
                            totalVotes++;
                        }
                        voteUserIdx++;
                    }

                    // Distribute downvotes across remaining users
                    for (int v = 0; v < downvotes && voteUserIdx < users.size(); v++) {
                        User voter = users.get(voteUserIdx % users.size());
                        if (voter.getId().equals(commentUser.getId())) {
                            voteUserIdx++;
                            if (voteUserIdx >= users.size()) break;
                            voter = users.get(voteUserIdx % users.size());
                        }
                        if (!voteRepository.existsByUserIdAndCommentId(voter.getId(), comment.getId())) {
                            Vote vote = Vote.builder()
                                    .user(voter)
                                    .comment(comment)
                                    .value((short) -1)
                                    .build();
                            voteRepository.save(vote);
                            totalVotes++;
                        }
                        voteUserIdx++;
                    }
                }

                log.info("Seeded amendment '{}' with {} comments",
                        amendment.getTitle().substring(0, Math.min(50, amendment.getTitle().length())),
                        comments.size());
            }

            log.info("Dataset seeding complete: {} amendments, {} comments, {} votes",
                    amendments.size(), totalComments, totalVotes);

        } catch (Exception e) {
            log.error("Failed to seed dataset from fcc_dataset.json: {}", e.getMessage(), e);
        }
    }
}
