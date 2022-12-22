from test.engine import EngineTestCase


class TestJobCategory(EngineTestCase):
    def setUp(self):
        super(TestJobCategory, self).setUp()
        self.create_job_category = {
            "job_id": 106,
            "category_id": 2
        }
        self.create_job_category_fail_1 = {
            "category_id": 1
        }

        self.create_job_category_fail_2 = {
            "job_id": 1
        }

        self.create_job_category_fail_3 = {
            "job_id": 1,
            "category_id": 1
        }

        self.create_job_category_fail_4 = {
            "category_id": 103
        }

        self.update_job_category = {
            "job_id": 106,
            "category_id": 2
        }

        self.update_job_category_fail_1 = {
            "category_id": 1
        }

        self.update_job_category_fail_2 = {
            "job_id": 106
        }

        self.update_job_category_fail_3 = {
            "job_id": 106,
            "category_id": 2
        }

        self.update_job_category_fail_4 = {
            "job_id": 10000,
            "category_id": 1
        }

        self.update_job_category_fail_5 = {
            "job_id": 106,
            "category_id": 100000
        }

        self.read_job_category = {
            "id": 1
        }

        self.delete_job_category = {
            "id": 5
        }

    def tearDown(self):
        super(TestJobCategory, self).tearDown()

    # Test create job with given data
    def test_create_job_categories(self):
        response = self.client.post("/job-categories", json=self.create_job_category)
        actual_code = response.status_code
        expected_code = 201
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed job_id is None
    def test_create_jobs_categories_fail_1(self):
        response = self.client.post("/job-categories", json=self.create_job_category_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "category_id" is None
    def test_create_jobs_categories_fail_2(self):
        response = self.client.post("/job-categories", json=self.create_job_category_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "job_id" invalid
    def test_create_jobs_categories_fail_3(self):
        response = self.client.post("/job-categories", json=self.create_job_category_fail_3)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "category_id" invalid
    def test_create_jobs_categories_fail_4(self):
        response = self.client.post("/job-categories", json=self.create_job_category_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test read job with given ID
    def test_get_job_categories(self):
        response = self.client.get(f"/job-categories/{self.read_job_category['id']}")
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test read job with given ID but this id not exist
    def test_get_job_categories_fail(self):
        response = self.client.get(f"/job-categories/10000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test get all jobs with given data but param "page" is invalid
    def test_get_all_job_categories_fail_1(self):
        response = self.client.get(f"/job-categories?page=500&limit=10")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test get all job_benefits with given data but param "page" is valid
    def test_get_all_job_categories(self):
        response = self.client.get(f"/job-categories?page=1&limit=10")
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with ID
    def test_update_job_categories(self):
        response = self.client.put(f"/job-categories/3", json=self.update_job_category)
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with non_existed ID
    def test_update_job_categories_fail(self):
        response = self.client.put(f"/job-categories/100", json=self.update_job_category)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with filed 'job_id' is None
    def test_update_job_categories_fail_1(self):
        response = self.client.put(f"/job-categories/1", json=self.update_job_category_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with filed 'category_id' is None
    def test_update_job_categories_fail_2(self):
        response = self.client.put(f"/job-categories/1", json=self.update_job_category_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with no information has been changed
    def test_update_job_categories_fail_3(self):
        response = self.client.put(f"/job-categories/3", json=self.update_job_category_fail_3)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with "job_id" invalid
    def test_update_job_categories_fail_4(self):
        response = self.client.put(f"/job-categories/3", json=self.update_job_category_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with "category_id" invalid
    def test_update_job_benefit_fail_5(self):
        response = self.client.put(f"/job-categories/1", json=self.update_job_category_fail_5)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test delete job_benefit with ID
    def test_delete_job_categories(self):
        response = self.client.delete(f"/job-categories/{self.delete_job_category['id']}")
        actual_code = response.status_code
        expected_code = 204
        self.assertEqual(expected_code, actual_code)

    #  Test delete job_benefit with non_existed ID
    def test_delete_job_categories_fail(self):
        response = self.client.delete(f"/job-categories/100000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)
