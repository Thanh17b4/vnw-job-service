CREATE TABLE job_locations
(
    job_id        INTEGER NOT NULL,
    location_name TEXT    NOT NULL,
    CONSTRAINT fk1 FOREIGN KEY (job_id) REFERENCES jobs (id) ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE job_locations
    ADD id SERIAL PRIMARY KEY NOT NULL;

ALTER TABLE job_locations
    ADD CONSTRAINT job_id_location_unique UNIQUE (job_id, location_name);

ALTER TABLE job_locations
    RENAME COLUMN location_name to location_id;










