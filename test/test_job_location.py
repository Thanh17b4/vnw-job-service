from test.engine import EngineTestCase


class TestJobLocation(EngineTestCase):
    def setUp(self):
        super(TestJobLocation, self).setUp()
        self.create_job_location = {
            "job_id": 106,
            "location_id": 1
        }
        self.create_job_location_fail_1 = {
            "location_id": 1
        }

        self.create_job_location_fail_2 = {
            "job_id": 106
        }

        self.create_job_location_fail_3 = {
            "job_id": 1,
            "location_id": 1
        }

        self.create_job_location_fail_4 = {
            "location_id": 1000
        }

        self.update_job_location = {
            "job_id": 106,
            "location_id": 2
        }

        self.update_job_location_fail_1 = {
            "location_id": 1
        }

        self.update_job_location_fail_2 = {
            "job_id": 106
        }

        self.update_job_location_fail_3 = {
            "job_id": 106,
            "location_id": 2
        }

        self.update_job_location_fail_4 = {
            "job_id": 10000,
            "location_id": 1
        }

        self.update_job_location_fail_5 = {
            "job_id": 106,
            "location_id": 100000
        }

        self.read_job_location = {
            "id": 5
        }

        self.delete_job_location = {
            "id": 6
        }

    def tearDown(self):
        super(TestJobLocation, self).tearDown()

    # Test create job with given data
    def test_create_job_locations(self):
        response = self.client.post("/job-locations", json=self.create_job_location)
        actual_code = response.status_code
        expected_code = 201
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed job_id is None
    def test_create_jobs_locations_fail_1(self):
        response = self.client.post("/job-locations", json=self.create_job_location_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job with given data but filed "location_id" is None
    def test_create_job_locations_fail_2(self):
        response = self.client.post("/job-locations", json=self.create_job_location_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job_location with given data but filed "job_id" invalid
    def test_create_job_locations_fail_3(self):
        response = self.client.post("/job-locations", json=self.create_job_location_fail_3)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test create job_location with given data but filed "location_id" invalid
    def test_create_job_locations_fail_4(self):
        response = self.client.post("/job-locations", json=self.create_job_location_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test read job_location with given ID
    def test_get_job_locations(self):
        response = self.client.get(f"/job-locations/{self.read_job_location['id']}")
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test read job_location with given ID but this id not exist
    def test_get_job_locations_fail(self):
        response = self.client.get(f"/job-locations/10000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test get all job_locations with given data but param "page" is invalid
    def test_get_all_job_locations_fail_1(self):
        response = self.client.get(f"/job-locations?page=500&limit=10")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)

    # Test get all job_location with given data but param "page" is valid
    def test_get_all_job_locations(self):
        response = self.client.get(f"/job-locations?page=1&limit=10")
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with ID
    def test_update_job_locations(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location)
        actual_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with non_existed ID
    def test_update_job_locations_fail(self):
        response = self.client.put(f"/job-locations/100", json=self.update_job_location)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with filed 'job_id' is None
    def test_update_job_locations_fail_1(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location_fail_1)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with filed 'location_id' is None
    def test_update_job_locations_fail_2(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location_fail_2)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with no information has been changed
    def test_update_job_locations_fail_3(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location_fail_3)
        actual_code = response.status_code
        expected_code = 204
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with "job_id" invalid
    def test_update_job_locations_fail_4(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location_fail_4)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test update job_location with "location_id" invalid
    def test_update_job_locations_fail_5(self):
        response = self.client.put(f"/job-locations/5", json=self.update_job_location_fail_5)
        actual_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, actual_code)

    # Test delete job_location with ID
    def test_delete_job_locations(self):
        response = self.client.delete(f"/job-locations/{self.delete_job_location['id']}")
        actual_code = response.status_code
        expected_code = 204
        self.assertEqual(expected_code, actual_code)

    #  Test delete job_location with non_existed ID
    def test_delete_job_locations_fail(self):
        response = self.client.delete(f"/job-locations/100000")
        actual_code = response.status_code
        expected_code = 400
        self.assertEqual(expected_code, actual_code)
