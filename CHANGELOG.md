# Changelog

## 2026-04-02

### Backend: Java, Maven, and runtime stability
- Fixed Maven wrapper startup failure on Windows PowerShell in `civiclens-backend/mvnw.cmd` (safe `.m2` target handling).
- Updated backend build target to Java 21 in `civiclens-backend/pom.xml`.
- Kept Spring Boot parent at `4.0.0` and added explicit `maven-compiler-plugin` configuration.
- Normalized Lombok dependency management in `pom.xml`:
  - added explicit `lombok.version`
  - removed duplicate Lombok dependency entry
- Removed incompatible Jackson setting from `civiclens-backend/src/main/resources/application.yml` that broke startup.

### AI analytics quality and fallback behavior
- Improved sentiment parsing in `civiclens-ai/models/sentiment.py`:
  - supports both explicit labels (`positive/negative`) and numeric labels (`LABEL_2/LABEL_0`)
  - adds heuristic fallback scoring when HuggingFace calls fail
- Improved stance classification fallback in `civiclens-ai/models/classifier.py`:
  - replaces all-neutral fallback with heuristic support/oppose/suggestion detection
- Improved policy brief generation in `civiclens-ai/models/summarizer.py`:
  - avoids persisting `"Summary generation failed."`
  - generates a local heuristic summary when API output is invalid or unavailable

### Backend analytics orchestration (core functional fix)
- Added `civiclens-backend/src/main/java/com/civiclens/analytics/AnalyticsSyncService.java`:
  - async refresh orchestration
  - in-flight deduplication per amendment
  - stale-data detection via comment/vote counts and failure markers
- Added `civiclens-backend/src/main/java/com/civiclens/analytics/AnalyticsBackfillInitializer.java`:
  - startup backfill for stale/missing analytics
  - periodic scheduled retry to self-heal when AI service was unavailable during startup
- Enabled async support in `civiclens-backend/src/main/java/com/civiclens/config/WebConfig.java` via `@EnableAsync`.
- Added automatic refresh triggers after domain changes:
  - `AmendmentService` on create/update and stale list reads
  - `CommentService` after comment creation
  - `VoteService` after vote add/change/remove
- Registered refresh requests after transaction commit to avoid race conditions with newly persisted data.

### Frontend local environment consistency
- Updated local frontend env defaults to use local backend (`http://localhost:8080`) in:
  - `civiclens-frontend/.env.local`
  - `civiclens-frontend/.env.development`

### Validation performed
- Backend tests pass after changes:
  - `.\mvnw.cmd test -q`
- Verified amendment analytics endpoint returns populated values after re-analysis.
- Confirmed previous zero/empty values were caused by stale persisted analytics and AI unavailability during refresh windows.

### Notes
- This changelog reflects local workspace changes currently in progress.
- `run-logs/` contains runtime/debug artifacts and is not part of source changes.
