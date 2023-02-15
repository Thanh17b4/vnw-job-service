ALTER TABLE job_benefits DROP CONSTRAINT fk1;
DELETE
FROM job_benefits
WHERE id >= 1;

