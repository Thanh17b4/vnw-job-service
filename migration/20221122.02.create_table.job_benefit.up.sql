CREATE TABLE job_benefits
(
    id         SERIAL PRIMARY KEY NOT NULL,
    job_id     INTEGER            NOT NULL,
    benefit_id INTEGER            NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (job_id) REFERENCES jobs (id) ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE job_benefits
    ADD CONSTRAINT fk_unique UNIQUE (job_id, benefit_id);










