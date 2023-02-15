ALTER TABLE job_categories DROP CONSTRAINT fk1;
DELETE
FROM job_categories
WHERE id >= 1;

