from test.engine import EngineTestCase


class TestJob(EngineTestCase):
    def setUp(self):
        super(TestJob, self).setUp()
        self.create_job = {
            "name": "Chuyên vien tin dung",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 1,
            "due_at": "2022-12-13"
        }
        self.create_job_1 = {
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 1,
            "due_at": "2022-12-13"
        }

        self.create_job_2 = {
            "name": "Chuyên viên tín dung",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "type": "toàn thời gian",
            "company_id": 1,
            "due_at": "2022-12-13"
        }

        self.create_job_3 = {
            "name": "Chuyên vien tin dung",
            "level": "Nhân viên",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 1,
            "due_at": "2022-12-13"
        }

        self.create_job_4 = {
            "name": "Chuyên vien tin dung",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 1
        }

        self.create_job_5 = {
            "name": "Chuyên vien tin dung",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "due_at": "2022-12-13"
        }

        self.create_job_6 = {
            "name": "Chuyên vien tin dung",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 100,
            "due_at": "2022-12-13"
        }

        self.update_job = {
            "name": "Chuyên Gia Ngân Sách Tài Chính và Kế Hoạch",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 1,
            "due_at": "2022-12-13"
        }

        self.update_job_fail = {
            "name": "Chuyên Gia Ngân Sách Tài Chính và Kế Hoạch",
            "level": "Nhân viên",
            "salary": "Thoả thuận",
            "cv_language": "Bất kỳ",
            "type": "toàn thời gian",
            "company_id": 100,
            "due_at": "2022-12-13"
        }

        self.read_job = {
            "id": 1
        }

        self.delete_job = {
            "id": 96
        }

    def tearDown(self):
        super(TestJob, self).tearDown()

    # Test read job with given ID
    def test_get_job(self):
        response = self.client.get(f"/jobs/{self.read_job['id']}")
        assert response.status_code == 200

    # Test read job with given ID but this id not exist
    def test_get_job_fail(self):
        response = self.client.get(f"/jobs/100")
        assert response.status_code == 400

    # Test create job with given data
    def test_create_jobs(self):
        response = self.client.post("/jobs", json=self.create_job)
        assert response.status_code == 201

    # Test create job with given data but filed name is None
    def test_create_jobs_fail_1(self):
        response = self.client.post("/jobs", json=self.create_job_1)
        assert response.status_code == 422

    # Test create job with given data but filed "cv_language" is None
    def test_create_jobs_fail_2(self):
        response = self.client.post("/jobs", json=self.create_job_2)
        assert response.status_code == 422

    # Test create job with given data but filed "salary" is None
    def test_create_jobs_fail_3(self):
        response = self.client.post("/jobs", json=self.create_job_3)
        assert response.status_code == 422

    # Test create job with given data but filed "due_at" is None
    def test_create_jobs_fail_4(self):
        response = self.client.post("/jobs", json=self.create_job_4)
        assert response.status_code == 422

    # Test create job with given data but filed "company_id" is None
    def test_create_jobs_fail_5(self):
        response = self.client.post("/jobs", json=self.create_job_5)
        assert response.status_code == 422

    # Test create job with given data but filed "company_id" is invalid
    def test_create_jobs_fail_6(self):
        response = self.client.post("/jobs", json=self.create_job_6)
        assert response.status_code == 400

    # Test get all jobs with given data but param "page" is invalid
    def test_get_all_job_fail_1(self):
        response = self.client.get(f"/jobs?page=500&limit=10")
        assert response.status_code == 204

    # Test get all jobs with given data but param "page" is valid
    def test_get_all_job(self):
        response = self.client.get(f"/jobs?page=1&limit=10")
        assert response.status_code == 200

    # Test update medicine with ID
    def test_update_job(self):
        response = self.client.put(f"/jobs/{self.read_job['id']}",
                                   json=self.update_job)
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update medicine with non_existed ID
    def test_update_job_fail(self):
        response = self.client.put(f"/jobs/100",
                                   json=self.update_job)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test update medicine with "company_id" invalid
    def test_update_job_fail(self):
        response = self.client.put(f"/jobs/1",
                                   json=self.update_job_fail)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test delete medicine with ID
    def test_delete_job(self):
        response = self.client.delete(f"/jobs/{self.delete_job['id']}")
        actual_code = response.status_code
        expected_code = 204
        self.assertEqual(expected_code, actual_code)

    #  Test delete medicine with non_existed ID
    def test_delete_job_fail(self):
        response = self.client.delete(f"/jobs/100000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)
