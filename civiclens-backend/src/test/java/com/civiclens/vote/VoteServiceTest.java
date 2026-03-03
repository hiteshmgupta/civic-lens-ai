package com.civiclens.vote;

import com.civiclens.amendment.*;
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
    private AmendmentRepository amendmentRepository;
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private VoteService voteService;

    private User user;
    private Amendment activeAmendment;
    private Amendment closedAmendment;

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
    }

    private VoteRequest voteRequest(short value) {
        VoteRequest req = new VoteRequest();
        req.setValue(value);
        return req;
    }

    // ---------------------------------------------------------------
    // Cast vote
    // ---------------------------------------------------------------

    @Test
    @DisplayName("Vote — new upvote is saved")
    void vote_newUpvote_saved() {
        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(activeAmendment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndAmendmentId(1L, 10L)).thenReturn(Optional.empty());

        voteService.vote(10L, voteRequest((short) 1), "test@example.com");

        verify(voteRepository).save(any(Vote.class));
    }

    @Test
    @DisplayName("Vote — same vote toggles off (removes)")
    void vote_sameValue_togglesOff() {
        Vote existing = Vote.builder().id(1L).user(user).amendment(activeAmendment).value((short) 1).build();

        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(activeAmendment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndAmendmentId(1L, 10L)).thenReturn(Optional.of(existing));

        voteService.vote(10L, voteRequest((short) 1), "test@example.com");

        verify(voteRepository).delete(existing);
        verify(voteRepository, never()).save(any());
    }

    @Test
    @DisplayName("Vote — different value updates the vote")
    void vote_differentValue_updates() {
        Vote existing = Vote.builder().id(1L).user(user).amendment(activeAmendment).value((short) 1).build();

        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(activeAmendment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndAmendmentId(1L, 10L)).thenReturn(Optional.of(existing));

        voteService.vote(10L, voteRequest((short) -1), "test@example.com");

        assertEquals((short) -1, existing.getValue());
        verify(voteRepository).save(existing);
    }

    @Test
    @DisplayName("Vote — on closed amendment throws exception")
    void vote_closedAmendment_throws() {
        when(amendmentRepository.findById(20L)).thenReturn(Optional.of(closedAmendment));

        assertThrows(IllegalArgumentException.class, () ->
                voteService.vote(20L, voteRequest((short) 1), "test@example.com"));
    }

    @Test
    @DisplayName("Vote — invalid value throws exception")
    void vote_invalidValue_throws() {
        assertThrows(IllegalArgumentException.class,
                () -> voteService.vote(10L, voteRequest((short) 2), "test@example.com"));
    }

    @Test
    @DisplayName("Vote — non-existent amendment throws exception")
    void vote_amendmentNotFound_throws() {
        when(amendmentRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                voteService.vote(999L, voteRequest((short) 1), "test@example.com"));
    }

    // ---------------------------------------------------------------
    // Remove vote
    // ---------------------------------------------------------------

    @Test
    @DisplayName("Remove vote — success deletes vote")
    void removeVote_success() {
        Vote existing = Vote.builder().id(1L).user(user).amendment(activeAmendment).value((short) 1).build();

        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndAmendmentId(1L, 10L)).thenReturn(Optional.of(existing));

        voteService.removeVote(10L, "test@example.com");

        verify(voteRepository).delete(existing);
    }

    @Test
    @DisplayName("Remove vote — non-existent vote throws exception")
    void removeVote_notFound_throws() {
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(voteRepository.findByUserIdAndAmendmentId(1L, 10L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                voteService.removeVote(10L, "test@example.com"));
    }
}
