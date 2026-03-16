package com.civiclens.amendment;

import com.civiclens.amendment.dto.*;
import com.civiclens.analytics.*;
import com.civiclens.comment.CommentRepository;
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
class AmendmentServiceTest {

    @Mock
    private AmendmentRepository amendmentRepository;
    @Mock
    private UserRepository userRepository;
    @Mock
    private VoteRepository voteRepository;
    @Mock
    private CommentRepository commentRepository;
    @Mock
    private AnalyticsRepository analyticsRepository;

    @InjectMocks
    private AmendmentService amendmentService;

    private User adminUser;
    private Amendment amendment;

    @BeforeEach
    void setUp() {
        adminUser = User.builder()
                .id(1L).username("admin").email("admin@civiclens.gov")
                .passwordHash("hash").role(UserRole.ADMIN).build();

        amendment = Amendment.builder()
                .id(10L).title("Test Amendment").body("Test body")
                .category(AmendmentCategory.HEALTHCARE)
                .status(AmendmentStatus.ACTIVE)
                .createdAt(LocalDateTime.now())
                .closesAt(LocalDateTime.now().plusDays(7))
                .createdBy(adminUser).build();
    }

    // ---------------------------------------------------------------
    // Create
    // ---------------------------------------------------------------

    @Test
    @DisplayName("Create amendment — success returns response and initializes analytics")
    void create_success() {
        AmendmentRequest request = new AmendmentRequest();
        request.setTitle("New Amendment");
        request.setBody("Amendment body text");
        request.setCategory(AmendmentCategory.EDUCATION);
        request.setClosesAt(LocalDateTime.now().plusDays(14));

        when(userRepository.findByEmail("admin@civiclens.gov")).thenReturn(Optional.of(adminUser));
        when(amendmentRepository.save(any(Amendment.class))).thenAnswer(inv -> {
            Amendment a = inv.getArgument(0);
            a.setId(100L);
            return a;
        });
        when(analyticsRepository.save(any(AmendmentAnalytics.class))).thenAnswer(inv -> inv.getArgument(0));
        when(voteRepository.countUpvotesByAmendmentId(anyLong())).thenReturn(0);
        when(voteRepository.countDownvotesByAmendmentId(anyLong())).thenReturn(0);
        when(commentRepository.countByAmendmentId(anyLong())).thenReturn(0);
        when(analyticsRepository.findByAmendmentId(anyLong())).thenReturn(Optional.empty());

        AmendmentResponse response = amendmentService.create(request, "admin@civiclens.gov");

        assertNotNull(response);
        assertEquals("New Amendment", response.getTitle());
        assertEquals("EDUCATION", response.getCategory());
        verify(analyticsRepository).save(any(AmendmentAnalytics.class));
    }

    @Test
    @DisplayName("Create amendment — user not found throws exception")
    void create_userNotFound_throws() {
        AmendmentRequest request = new AmendmentRequest();
        request.setTitle("Test");
        request.setBody("Body");
        request.setCategory(AmendmentCategory.HEALTHCARE);

        when(userRepository.findByEmail("unknown@test.com")).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> amendmentService.create(request, "unknown@test.com"));
    }

    // ---------------------------------------------------------------
    // Get by ID
    // ---------------------------------------------------------------

    @Test
    @DisplayName("Get by ID — returns amendment response")
    void getById_success() {
        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(amendment));
        when(voteRepository.countUpvotesByAmendmentId(10L)).thenReturn(5);
        when(voteRepository.countDownvotesByAmendmentId(10L)).thenReturn(2);
        when(commentRepository.countByAmendmentId(10L)).thenReturn(8);
        when(analyticsRepository.findByAmendmentId(10L)).thenReturn(Optional.empty());

        AmendmentResponse response = amendmentService.getById(10L);

        assertNotNull(response);
        assertEquals(10L, response.getId());
        assertEquals("Test Amendment", response.getTitle());
        assertEquals(5, response.getUpvotes());
        assertEquals(2, response.getDownvotes());
        assertEquals(8, response.getCommentCount());
    }

    @Test
    @DisplayName("Get by ID — not found throws exception")
    void getById_notFound_throws() {
        when(amendmentRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
                amendmentService.getById(999L));
    }

    // ---------------------------------------------------------------
    // List
    // ---------------------------------------------------------------

    @Test
    @DisplayName("List — returns paginated response with default sort")
    void list_defaultSort() {
        Page<Amendment> page = new PageImpl<>(List.of(amendment), PageRequest.of(0, 10), 1);
        when(amendmentRepository.findAll(any(Pageable.class))).thenReturn(page);
        when(voteRepository.countUpvotesByAmendmentId(anyLong())).thenReturn(0);
        when(voteRepository.countDownvotesByAmendmentId(anyLong())).thenReturn(0);
        when(commentRepository.countByAmendmentId(anyLong())).thenReturn(0);
        when(analyticsRepository.findByAmendmentId(anyLong())).thenReturn(Optional.empty());

        PagedResponse<AmendmentResponse> response = amendmentService.list(null, null, 0, 10);

        assertEquals(1, response.getContent().size());
        assertEquals("Test Amendment", response.getContent().get(0).getTitle());
    }

    @Test
    @DisplayName("List — with category filter")
    void list_withCategoryFilter() {
        Page<Amendment> page = new PageImpl<>(List.of(amendment), PageRequest.of(0, 10), 1);
        when(amendmentRepository.findByCategory(eq(AmendmentCategory.HEALTHCARE), any(Pageable.class)))
                .thenReturn(page);
        when(voteRepository.countUpvotesByAmendmentId(anyLong())).thenReturn(0);
        when(voteRepository.countDownvotesByAmendmentId(anyLong())).thenReturn(0);
        when(commentRepository.countByAmendmentId(anyLong())).thenReturn(0);
        when(analyticsRepository.findByAmendmentId(anyLong())).thenReturn(Optional.empty());

        PagedResponse<AmendmentResponse> response = amendmentService.list("LATEST", "HEALTHCARE", 0, 10);

        assertEquals(1, response.getContent().size());
        verify(amendmentRepository).findByCategory(eq(AmendmentCategory.HEALTHCARE), any(Pageable.class));
    }

    // ---------------------------------------------------------------
    // Update
    // ---------------------------------------------------------------

    @Test
    @DisplayName("Update — success modifies title and body")
    void update_success() {
        AmendmentRequest request = new AmendmentRequest();
        request.setTitle("Updated Title");
        request.setBody("Updated body");
        request.setCategory(AmendmentCategory.HEALTHCARE);

        when(amendmentRepository.findById(10L)).thenReturn(Optional.of(amendment));
        when(amendmentRepository.save(any(Amendment.class))).thenReturn(amendment);
        when(voteRepository.countUpvotesByAmendmentId(10L)).thenReturn(0);
        when(voteRepository.countDownvotesByAmendmentId(10L)).thenReturn(0);
        when(commentRepository.countByAmendmentId(10L)).thenReturn(0);
        when(analyticsRepository.findByAmendmentId(10L)).thenReturn(Optional.empty());

        AmendmentResponse response = amendmentService.update(10L, request);

        assertNotNull(response);
        verify(amendmentRepository).save(any(Amendment.class));
    }
}
