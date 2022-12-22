from test.engine import EngineTestCase


class TestJobBenefit(EngineTestCase):
    def setUp(self):
        super(TestJobBenefit, self).setUp()
        self.create_job_benefit = {
            "job_id": 103,
            "benefit_id": 1
        }
        self.create_job_benefit_fail_1 = {
            "job_id": 1,
            "benefit_id": 100
        }

        self.create_job_benefit_fail_2 = {
            "job_id": 1000,
            "benefit_id": 1
        }

        self.create_job_benefit_fail_3 = {
            "benefit_id": 1
        }

        self.create_job_benefit_fail_4 = {
            "job_id": 103
        }

        self.update_job_benefit = {
            "job_id": 103,
            "benefit_id": 2
        }

        self.update_job_benefit_fail_1 = {
            "benefit_id": 1
        }

        self.update_job_benefit_fail_2 = {
            "job_id": 1
        }

        self.update_job_benefit_fail_3 = {
            "job_id": 103,
            "benefit_id": 2
        }

        self.update_job_benefit_fail_4 = {
            "job_id": 103,
            "benefit_id": 1000
        }

        self.update_job_benefit_fail_5 = {
            "job_id": 1,
            "benefit_id": 1
        }

        self.read_job_benefit = {
            "id": 3
        }

        self.delete_job_benefit = {
            "id": 3
        }

    def tearDown(self):
        super(TestJobBenefit, self).tearDown()

    # Test create job with given data
    def test_create_job_benefits(self):
        response = self.client.post("/job-benefits", json=self.create_job_benefit)
        actual_code = response.status_code
        expected_code = 201
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed job_id invalid
    def test_create_jobs_fail_1(self):
        response = self.client.post("/job-benefits", json=self.create_job_benefit_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "benefit_id" invalid
    def test_create_jobs_fail_2(self):
        response = self.client.post("/job-benefits", json=self.create_job_benefit_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "job_id" is None
    def test_create_jobs_fail_3(self):
        response = self.client.post("/job-benefits", json=self.create_job_benefit_fail_3)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "benefit_id" is None
    def test_create_jobs_fail_4(self):
        response = self.client.post("/job-benefits", json=self.create_job_benefit_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test read job with given ID
    def test_get_job_benefit(self):
        response = self.client.get(f"/job-benefits/{self.read_job_benefit['id']}")
        assert response.status_code == 200

    # Test read job with given ID but this id not exist
    def test_get_job_benefit_fail(self):
        response = self.client.get(f"/job-benefits/100")
        assert response.status_code == 400

    # Test get all jobs with given data but param "page" is invalid
    def test_get_all_job_benefit_fail_1(self):
        response = self.client.get(f"/job-benefits?page=500&limit=10")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test get all job_benefits with given data but param "page" is valid
    def test_get_all_job_benefit(self):
        response = self.client.get(f"/job-benefits?page=1&limit=10")
        assert response.status_code == 200

    # Test update job_benefit with ID
    def test_update_job_benefit(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit)
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with non_existed ID
    def test_update_job_benefit_fail(self):
        response = self.client.put(f"/job-benefits/100", json=self.update_job_benefit)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with filed 'job_id' is None
    def test_update_job_benefit_fail_1(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with filed 'benefit' is None
    def test_update_job_benefit_fail_2(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with no information has been changed
    def test_update_job_benefit_fail_3(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit_fail_3)
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with "benefit_id" invalid
    def test_update_job_benefit_fail_4(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_benefit with "job_id" invalid
    def test_update_job_benefit_fail_5(self):
        response = self.client.put(f"/job-benefits/1", json=self.update_job_benefit_fail_5)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test delete job_benefit with ID
    def test_delete_job(self):
        response = self.client.delete(f"/jobs/{self.delete_job_benefit['id']}")
        actual_code = response.status_code
        expected_code = 204
        self.assertEqual(expected_code, actual_code)

    #  Test delete job_benefit with non_existed ID
    def test_delete_job_fail(self):
        response = self.client.delete(f"/jobs/100000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)
