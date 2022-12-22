import urllib3
from fastapi import APIRouter, Response
from starlette import status

from db import mydb
from schemas.job_location import job_location_result, job_location_list_result, JobLocation
from .jobs import detail_job

job_location_router = APIRouter()


@job_location_router.post("/job-locations", status_code=201)
def create_job_location(request: JobLocation, response: Response):
    new_job_location = request.job_location_to_dict()
    # Validate data
    is_ok, msg = __validate(new_job_location)
    if is_ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return msg
    # check job_id is valid or not:
    ok, result = detail_job(new_job_location["job_id"], response)
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    # check location_id is valid or not:
    ok, txt = _check_location_id(new_job_location["location_id"])
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return txt
    # insert new record in to job_location table
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO job_location (job_id, location_id) VALUES (%s, %s)"
        val = (new_job_location["job_id"], new_job_location["location_id"])
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} job_location has been inserted successfully"


def __validate(req: dict):
    if req.get("job_id") is None:
        return False, "job_id cannot be null"
    if req.get("location_id") is None:
        return False, "location_id cannot be null"
    return req, ""


def _check_location_id(location_id: int):
    # check location_id
    http = urllib3.PoolManager()
    r = http.request("GET", f"http://localhost:5001/locations/{location_id}")
    if r.status != 200:
        return False, f"location_id is not exist"
    return True, None


@job_location_router.get("/job-locations/{id}", status_code=200)
def detail_job_location(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM job_location WHERE id = %d" % id)
        job_location = my_cursor.fetchone()
        if job_location is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"job_location_id is not correct"
        return True, job_location_result(job_location)


@job_location_router.get("/job-locations", status_code=200)
def all_job_location(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(id) FROM job_location")
        total_records = my_cursor.fetchone()[0]
        d = total_records % limit
        if d == 0:
            total_page = total_records // limit
        else:
            total_page = total_records // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute(
            "SELECT * FROM job_location LIMIT %s OFFSET %s", (limit, offset)
        )
        job_location = my_cursor.fetchall()
        if job_location is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return job_location_list_result(job_location)


@job_location_router.put("/job-locations/{id}", status_code=200)
async def update_job_location(id: int, req: JobLocation, response: Response):
    # check job_location existed or not in job_location table
    new_job_location = req.job_location_to_dict()
    boolean, old_job_location = detail_job_location(id, response)
    if boolean is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return old_job_location
    # check job_id is valid or not:
    ok, result = detail_job(new_job_location["job_id"], response)
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    # check location_id is valid or not:
    ok, txt = _check_location_id(new_job_location["location_id"])
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return txt
    # check have some changes or not
    ok, msg = __check_change(old_job_location, new_job_location)
    if ok is False:
        response.status_code = status.HTTP_204_NO_CONTENT
        return msg
    # update record
    with mydb:
        my_cursor = mydb.cursor()
        sql = (
            "UPDATE job_location SET job_id = %s, location_id = %s   WHERE id = %s"
        )
        val = (new_job_location["job_id"], new_job_location["location_id"], id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_change(req: dict, new_req: dict):
    if (
            req["job_id"] == new_req["job_id"]
            and req["location_id"] == new_req["location_id"]
    ):
        return False, "no information have been changed"
    return new_req, ""


@job_location_router.delete("/job-locations/{id}", status_code=200)
async def delete_job_location(id: int, response: Response):
    boolean, result = detail_job_location(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM job_location WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
