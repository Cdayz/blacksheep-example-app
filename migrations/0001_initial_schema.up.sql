CREATE TABLE IF NOT EXISTS "features" (
    "id" SERIAL PRIMARY KEY,
    "application" VARCHAR(300) NOT NULL,
    "feature_name" VARCHAR(300) NOT NULL,
    "is_enabled" BOOLEAN NOT NULL,
    -- Constraints
    UNIQUE ("application", "feature_name")
);
