ALTER TABLE job_locations DROP CONSTRAINT fk1;
DELETE
FROM job_locations
WHERE id >= 1;

