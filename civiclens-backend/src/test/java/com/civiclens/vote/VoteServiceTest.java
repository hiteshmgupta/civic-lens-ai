package com.civiclens.vote;

import com.civiclens.amendment.*;
import com.civiclens.comment.Comment;
import com.civiclens.comment.CommentRepository;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import com.civiclens.vote.dto.VoteRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class VoteServiceTest {

    @Mock
    private VoteRepository voteRepository;
    @Mock
    private CommentRepository commentRepository;
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private VoteService voteService;

    private User user;
    private Amendment activeAmendment;
    private Amendment closedAmendment;
    private Comment activeComment;
    private Comment closedComment;

    @BeforeEach
    void setUp() {
        user = User.builder().id(1L).email("test@example.com").username("testuser").build();

        activeAmendment = Amendment.builder()
                .id(10L).title("Test").body("Body")
                .category(AmendmentCategory.HEALTHCARE)
                .status(AmendmentStatus.ACTIVE)
                .createdBy(user).build();

        closedAmendment = Amendment.builder()
                .id(20L).title("Closed").body("Body")
                .category(AmendmentCategory.AGRICULTURE)
                .status(AmendmentStatus.CLOSED)
                .createdBy(user).build();

        activeComment = Comment.builder()
                .id(100L).body("Test comment").user(user).amendment(activeAmendment).build();

        closedComment = Comment.builder()
                .id(200L).body("Closed comment").user(user).amendment(closedAmendment).build();
    }

    private VoteRequest voteRequest(short value) {
        VoteRequest req = new VoteRequest();
        req.setValue(value);
        return req;
    }

    // Cast vote

    @Test
    @DisplayName("Vote — new upvote is saved")
    void vote_newUpvote_saved() {
        when(commentRepository.findById(100L)).thenReturn(Optional.of(activeComment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndCommentId(1L, 100L)).thenReturn(Optional.empty());

        voteService.vote(100L, voteRequest((short) 1), "test@example.com");

        verify(voteRepository).save(any(Vote.class));
    }

    @Test
    @DisplayName("Vote — same vote toggles off (removes)")
    void vote_sameValue_togglesOff() {
        Vote existing = Vote.builder().id(1L).user(user).comment(activeComment).value((short) 1).build();

        when(commentRepository.findById(100L)).thenReturn(Optional.of(activeComment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndCommentId(1L, 100L)).thenReturn(Optional.of(existing));

        voteService.vote(100L, voteRequest((short) 1), "test@example.com");

        verify(voteRepository).delete(existing);
        verify(voteRepository, never()).save(any());
    }

    @Test
    @DisplayName("Vote — different value updates the vote")
    void vote_differentValue_updates() {
        Vote existing = Vote.builder().id(1L).user(user).comment(activeComment).value((short) 1).build();

        when(commentRepository.findById(100L)).thenReturn(Optional.of(activeComment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndCommentId(1L, 100L)).thenReturn(Optional.of(existing));

        voteService.vote(100L, voteRequest((short) -1), "test@example.com");

        assertEquals((short) -1, existing.getValue());
        verify(voteRepository).save(existing);
    }

    @Test
    @DisplayName("Vote — on comment under closed amendment throws exception")
    void vote_closedAmendment_throws() {
        when(commentRepository.findById(200L)).thenReturn(Optional.of(closedComment));

        assertThrows(IllegalArgumentException.class, () ->
                voteService.vote(200L, voteRequest((short) 1), "test@example.com"));
    }

    @Test
    @DisplayName("Vote — invalid value throws exception")
    void vote_invalidValue_throws() {
        assertThrows(IllegalArgumentException.class,
                () -> voteService.vote(100L, voteRequest((short) 2), "test@example.com"));
    }

    @Test
    @DisplayName("Vote — non-existent comment throws exception")
    void vote_commentNotFound_throws() {
        when(commentRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                voteService.vote(999L, voteRequest((short) 1), "test@example.com"));
    }

    // Remove vote

    @Test
    @DisplayName("Remove vote — success deletes vote")
    void removeVote_success() {
        Vote existing = Vote.builder().id(1L).user(user).comment(activeComment).value((short) 1).build();

        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndCommentId(1L, 100L)).thenReturn(Optional.of(existing));

        voteService.removeVote(100L, "test@example.com");

        verify(voteRepository).delete(existing);
    }

    @Test
    @DisplayName("Remove vote — non-existent vote throws exception")
    void removeVote_notFound_throws() {
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndCommentId(1L, 100L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                voteService.removeVote(100L, "test@example.com"));
    }
}
