package com.civiclens.comment;

import com.civiclens.amendment.*;
import com.civiclens.comment.dto.*;
import com.civiclens.common.dto.PagedResponse;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import com.civiclens.vote.VoteRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CommentServiceTest {

    @Mock
    private CommentRepository commentRepository;
    @Mock
    private AmendmentRepository amendmentRepository;
    @Mock
    private UserRepository userRepository;
    @Mock
    private VoteRepository voteRepository;

    @InjectMocks
    private CommentService commentService;

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

    private CommentRequest commentRequest(String body) {
        CommentRequest req = new CommentRequest();
        req.setBody(body);
        return req;
    }

    // Create comment

    @Test
    @DisplayName("Create comment — success on active amendment")
    void create_success() {
        Comment savedComment = Comment.builder()
                .id(1L).user(user).amendment(activeAmendment)
                .body("Great proposal!").createdAt(LocalDateTime.now())
                .build();

        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(activeAmendment));
        when(userRepository.findByEmail("test@example.com")).thenReturn(Optional.of(user));
        when(commentRepository.save(any(Comment.class))).thenReturn(savedComment);

        CommentResponse response = commentService.create(10L, commentRequest("Great proposal!"), "test@example.com");

        assertNotNull(response);
        assertEquals("Great proposal!", response.getBody());
        assertEquals("testuser", response.getUsername());
        verify(commentRepository).save(any(Comment.class));
    }

    @Test
    @DisplayName("Create comment — on closed amendment throws exception")
    void create_closedAmendment_throws() {
        when(amendmentRepository.findById(20L)).thenReturn(Optional.of(closedAmendment));

        assertThrows(IllegalArgumentException.class, () ->
                commentService.create(20L, commentRequest("Too late"), "test@example.com"));
    }

    @Test
    @DisplayName("Create comment — amendment not found throws exception")
    void create_amendmentNotFound_throws() {
        when(amendmentRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                commentService.create(999L, commentRequest("Hello"), "test@example.com"));
    }

    // List comments

    @Test
    @DisplayName("List comments — returns paginated response")
    void list_returnsPaginatedResponse() {
        Comment c1 = Comment.builder().id(1L).user(user).amendment(activeAmendment)
                .body("Comment 1").createdAt(LocalDateTime.now()).build();
        Comment c2 = Comment.builder().id(2L).user(user).amendment(activeAmendment)
                .body("Comment 2").createdAt(LocalDateTime.now()).build();

        Page<Comment> page = new PageImpl<>(List.of(c1, c2), PageRequest.of(0, 10), 2);
        when(commentRepository.findByAmendmentId(eq(10L), any(Pageable.class))).thenReturn(page);

        PagedResponse<CommentResponse> response = commentService.list(10L, 0, 10);

        assertEquals(2, response.getContent().size());
        assertEquals(0, response.getPage());
        assertEquals(2, response.getTotalElements());
    }
}
