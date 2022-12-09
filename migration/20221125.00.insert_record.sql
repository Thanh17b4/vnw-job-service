INSERT INTO jobs (name, level, cv_language, type, slug, company_id, due_at, salary)
VALUES ('Chuyen vien tin dung', 'Nhân viên', 'Bất kỳ', 'toan thoi gian', 'chuyen-gia-ngan-sach-tai-chinh-va-ke-hoach',
        15, '2022-12-13', 'Thoả thuận');

INSERT INTO job_location(job_id, location_id)
VALUES (1, 1);
INSERT INTO job_category(job_id, category_id)
VALUES (1, 1),
       (1, 2);

INSERT INTO job_benefits(job_id, benefit_id)
VALUES (1, 1);

