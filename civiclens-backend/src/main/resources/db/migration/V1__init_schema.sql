-- CivicLens — PostgreSQL Schema Initialization
-- V1: Core tables for users, amendments, votes, comments, analytics


-- 1. USERS

CREATE TABLE IF NOT EXISTS users (
    id             BIGSERIAL PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    role           VARCHAR(10)  NOT NULL DEFAULT 'USER',
    created_at     TIMESTAMP    NOT NULL DEFAULT NOW()
);


-- 2. AMENDMENTS

CREATE TABLE IF NOT EXISTS amendments (
    id          BIGSERIAL    PRIMARY KEY,
    title       VARCHAR(500) NOT NULL,
    body        TEXT         NOT NULL,
    category    VARCHAR(50)  NOT NULL,
    status      VARCHAR(10)  NOT NULL DEFAULT 'ACTIVE',
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    closes_at   TIMESTAMP,
    created_by  BIGINT       NOT NULL REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_amendments_status ON amendments(status);
CREATE INDEX IF NOT EXISTS idx_amendments_category ON amendments(category);


-- 3. VOTES (unique constraint: one vote per user per amendment)

CREATE TABLE IF NOT EXISTS votes (
    id            BIGSERIAL PRIMARY KEY,
    user_id       BIGINT    NOT NULL REFERENCES users(id),
    amendment_id  BIGINT    NOT NULL REFERENCES amendments(id),
    value         SMALLINT  NOT NULL CHECK (value IN (-1, 1)),
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, amendment_id)
);


-- 4. COMMENTS

CREATE TABLE IF NOT EXISTS comments (
    id            BIGSERIAL PRIMARY KEY,
    user_id       BIGINT    NOT NULL REFERENCES users(id),
    amendment_id  BIGINT    NOT NULL REFERENCES amendments(id),
    body          TEXT      NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comments_amendment_id ON comments(amendment_id);


-- 5. AMENDMENT ANALYTICS (one row per amendment)

CREATE TABLE IF NOT EXISTS amendment_analytics (
    id                     BIGSERIAL        PRIMARY KEY,
    amendment_id           BIGINT           NOT NULL UNIQUE REFERENCES amendments(id),
    sentiment_mean         DOUBLE PRECISION DEFAULT 0,
    sentiment_variance     DOUBLE PRECISION DEFAULT 0,
    sentiment_distribution JSONB            DEFAULT '{}',
    sentiment_timeline     JSONB            DEFAULT '[]',
    topic_clusters         JSONB            DEFAULT '[]',
    top_supporting         JSONB            DEFAULT '[]',
    top_opposing           JSONB            DEFAULT '[]',
    total_comments         INT              DEFAULT 0,
    total_votes            INT              DEFAULT 0,
    upvotes                INT              DEFAULT 0,
    downvotes              INT              DEFAULT 0,
    vote_polarity          DOUBLE PRECISION DEFAULT 0,
    stance_entropy         DOUBLE PRECISION DEFAULT 0,
    engagement_score       DOUBLE PRECISION DEFAULT 0,
    controversy_score      DOUBLE PRECISION DEFAULT 0,
    controversy_label      VARCHAR(20)      DEFAULT 'Low',
    policy_brief           TEXT,
    last_computed_at       TIMESTAMP        DEFAULT NOW()
);


-- 6. SEED DATA (development only)

-- Admin user (password: admin123 — BCrypt hash)
INSERT INTO users (username, email, password_hash, role) VALUES
    ('admin', 'admin@civiclens.gov', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'ADMIN'),
    ('alice', 'alice@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'USER'),
    ('bob',   'bob@example.com',   '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'USER')
ON CONFLICT DO NOTHING;

-- Sample amendments
INSERT INTO amendments (title, body, category, status, closes_at, created_by) VALUES
    (
        'Universal Healthcare Access Act',
        'Proposed amendment to expand healthcare coverage to all citizens regardless of employment status. This includes mental health services, preventive care, and emergency services at reduced copayment rates.',
        'HEALTHCARE',
        'ACTIVE',
        NOW() + INTERVAL '30 days',
        1
    ),
    (
        'Agricultural Subsidy Reform',
        'Amendment proposing restructured subsidies for small-scale organic farmers. Introduces graduated support tiers based on farm size and sustainable practices adoption.',
        'AGRICULTURE',
        'ACTIVE',
        NOW() + INTERVAL '14 days',
        1
    ),
    (
        'Digital Education Infrastructure Act',
        'Proposal for nationwide broadband infrastructure investment in rural school districts. Mandates minimum internet speed standards for educational institutions.',
        'EDUCATION',
        'ACTIVE',
        NOW() + INTERVAL '21 days',
        1
    )
ON CONFLICT DO NOTHING;

-- Initialize analytics rows for seeded amendments
INSERT INTO amendment_analytics (amendment_id) VALUES (1), (2), (3)
ON CONFLICT DO NOTHING;
