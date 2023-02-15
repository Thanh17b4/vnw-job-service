CREATE TABLE job_categories
(
    id          SERIAL PRIMARY KEY NOT NULL,
    job_id      INTEGER            NOT NULL,
    category_id INTEGER            NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (job_id) REFERENCES jobs (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT job_id_category_unique UNIQUE (job_id, category_id)
);














