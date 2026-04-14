# CivicLens Dataset Scripts

This directory contains the dataset preparation script and the generated JSON dataset used to seed the CivicLens database on every fresh backend start.

---

## Files

| File | Description |
|---|---|
| `prepare_fcc_dataset.py` | Python script that defines all dataset content and generates `fcc_dataset.json` |
| `fcc_dataset.json` | Generated JSON output — also copied to `civiclens-backend/src/main/resources/` for the backend to read |

---

## What the Dataset Contains

The dataset is modeled after real-world U.S. federal regulatory proceedings (FCC, EPA, HHS, DOE, etc.) with curated, realistic comments representing diverse perspectives.

| Entity | Count | Details |
|---|---|---|
| **Users** | 20 | Synthetic personas with distinct viewpoints (e.g., `digital_rights_advocate`, `small_biz_owner`, `rural_internet_user`) |
| **Amendments** | 7 | Real-world legislative topics across 7 categories |
| **Comments** | ~220 total | 23–36 per amendment, each with `body`, `stance` (support/oppose/neutral), and `sentiment` (strongly_positive to strongly_negative) |
| **Votes** | Generated | Upvote/downvote counts per comment, weighted by stance and sentiment intensity |

### The 7 Amendments

| # | Title | Category | Comments |
|---|---|---|---|
| 1 | Restoring Internet Freedom Act — Repeal of Net Neutrality Rules | `DIGITAL_PRIVACY` | 36 |
| 2 | Clean Air and Climate Accountability Act Amendment | `ENVIRONMENT` | 26 |
| 3 | Digital Infrastructure and Rural Broadband Expansion Act | `INFRASTRUCTURE` | 23 |
| 4 | Healthcare Data Privacy and Patient Rights Enhancement Act | `HEALTHCARE` | 23 |
| 5 | Student Digital Privacy and Educational Technology Accountability Act | `EDUCATION` | 22 |
| 6 | Small Business Tax Fairness and Economic Opportunity Act | `TAXATION` | 21 |
| 7 | National Cybersecurity Infrastructure and Critical Defense Systems Act | `DEFENSE` | 23 |

---

## How Seeding Works (End-to-End Pipeline)

```
prepare_fcc_dataset.py           ← You edit this to change dataset content
        │
        ▼
fcc_dataset.json                 ← Generated output (scripts/)
        │
        ▼ (must be copied)
src/main/resources/fcc_dataset.json   ← Backend reads from classpath
        │
        ▼ (on app start)
SampleDataInitializer.java       ← Creates DB records: users → amendments → comments (with vote counts)
        │
        ▼ (after seeding)
AnalyticsBackfillInitializer.java ← Triggers AI analysis for all amendments
```

**Key behaviors:**
- Seeding only runs when the database is empty (`amendmentRepository.count() == 0`)
- All 20 synthetic users get password `civiclens@123` and role `USER`
- Amendments are created by the `admin@gmail.com` admin account
- Vote counts (`upvoteCount`, `downvoteCount`) are stored directly on each `Comment` entity from the JSON — no individual `Vote` records are created for seeded data
- When real users vote via the API, both a `Vote` record (for uniqueness enforcement) and the cached counts on `Comment` are updated

---

## Regenerating the Dataset

If you modify the Python script, regenerate and deploy the JSON:

```bash
cd scripts

# Run the script — outputs fcc_dataset.json in current directory
python prepare_fcc_dataset.py

# Copy to backend resources so it's on the classpath at runtime
copy fcc_dataset.json ..\civiclens-backend\src\main\resources\fcc_dataset.json
```

> **Important:** After updating the JSON, you must either start with a fresh database (empty tables) or manually clear the `amendments` table so the `SampleDataInitializer` runs again.

---

## Extending the Dataset

All data lives inside `prepare_fcc_dataset.py` as Python dictionaries. Follow the patterns below to add content from the same dataset conventions.

### Adding a New Amendment

1. Define a new amendment dictionary following the existing structure:

```python
AMENDMENT_8 = {
    "title": "Amendment title — matches real legislative language",
    "body": (
        "Full text of the amendment, written in formal regulatory language. "
        "Describe what the amendment does, what it changes, and its key provisions."
    ),
    "category": "CATEGORY_NAME",   # Must be a valid category (see below)
    "comments": [
        # Add comments here (see next section)
    ]
}
```

2. Register it in the `main()` function:

```python
def main():
    all_amendments = [AMENDMENT_1, AMENDMENT_2, ..., AMENDMENT_8]  # ← add here
```

**Valid categories:** `HEALTHCARE`, `AGRICULTURE`, `EDUCATION`, `INFRASTRUCTURE`, `DIGITAL_PRIVACY`, `ENVIRONMENT`, `TAXATION`, `DEFENSE`, `OTHER`

### Adding Comments to an Amendment

Each comment follows this structure:

```python
{
    "body": "Full comment text, written from a specific perspective...",
    "stance": "support",           # "support", "oppose", or "neutral"
    "sentiment": "strongly_positive"  # See sentiment values below
}
```

**Sentiment values and their conventions:**

| Sentiment | Used When |
|---|---|
| `strongly_positive` | Passionate support with personal stakes or urgent language |
| `positive` | Clear support with reasoned arguments |
| `neutral` | Mixed views, balanced perspective, or procedural comments |
| `negative` | Clear opposition with specific concerns |
| `strongly_negative` | Strong opposition with alarm, frustration, or dire warnings |

**Dataset conventions used in existing comments:**
- Comments are written from distinct perspectives (professional, personal, technical, economic)
- Each amendment has a realistic distribution: majority on one side, meaningful opposition, and a few neutral
- Comments reference real-world events, statistics, and institutional knowledge
- Opposition comments raise substantive concerns, not strawman arguments
- Neutral comments often suggest amendments or alternative approaches

### Adding New Users

Append to the `USERS` list:

```python
USERS = [
    # ... existing 20 users ...
    {"username": "new_persona_name", "email": "persona@civiclens.com"},
]
```

Comments are assigned to users via round-robin using `user_index` (automatically computed in `main()`).

### Modifying Vote Generation

The `generate_votes()` function (line 358) assigns upvote/downvote counts based on stance and sentiment:

| Stance + Sentiment | Upvote Range | Downvote Range |
|---|---|---|
| support + strongly | 40–110 | 3–15 |
| support + moderate | 22–60 | 5–20 |
| oppose + strongly | 20–55 | 15–50 |
| oppose + moderate | 15–40 | 10–35 |
| neutral | 10–35 | 8–28 |

To change the distribution, modify the ranges in `generate_votes()`. The random seed (`random.seed(42)` on line 22) ensures reproducible results — change the seed for different but deterministic output.

---

## After Extending — Full Workflow

```bash
# 1. Edit prepare_fcc_dataset.py (add amendments, comments, users)

# 2. Regenerate the JSON
cd scripts
python prepare_fcc_dataset.py

# 3. Copy to backend resources
copy fcc_dataset.json ..\civiclens-backend\src\main\resources\fcc_dataset.json

# 4. Clear your database (so the initializer re-runs)
#    If using the live Render deployment, redeploy with a fresh database
#    If running locally, drop and recreate the civiclens database

# 5. Start the backend — data will seed automatically
cd ..\civiclens-backend
mvn spring-boot:run
```

The script prints a summary after generation:

```
=================================================================
CivicLens Dataset Summary
=================================================================
  [DIGITAL_PRIVACY] Restoring Internet Freedom Act — Repeal of Ne...
    Comments: 36  |  Support: 13  Oppose: 19  Neutral: 4
    ...
=================================================================
  TOTALS:
    Amendments:        7
    Total comments:    220
    Total upvotes:     8,XXX
    Total downvotes:   3,XXX
    Users:             20
=================================================================
```
