CREATE TABLE jobs
(
    id          SERIAL PRIMARY KEY NOT NULL,
    name        TEXT               NOT NULL,
    level       TEXT               NOT NULL,
    salary      TEXT               NOT NULL,
    CV_language TEXT               NOT NULL,
    type        TEXT               NOT NULL,
    slug        TEXT               NOT NULL,
    company_id  TEXT               NOT NULL,
    created_at  TIMESTAMP(6)       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP(6)       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_at      TIMESTAMP(6)       NOT NULL
);










