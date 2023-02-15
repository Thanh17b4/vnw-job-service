import urllib3
from fastapi import APIRouter, Response
from starlette import status

from db import job_service_db
from model.check_data import is_integer
from schemas.job_category import JobCategory, job_category_list_result, job_category_result
from .jobs import detail_job

job_category_router = APIRouter()


@job_category_router.post('/job-categories', status_code=201)
def create_job_category(request: JobCategory, response: Response):
    job_category = request.job_category_to_dict()
    print(1)
    # Validate data
    is_ok, msg = __validate(job_category)
    if is_ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return msg
    # check job_id valid or not
    ok, result = detail_job(job_category["job_id"], response)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check benefit_id valid or not:
    ok, txt = _check_category_id(job_category["category_id"])
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return txt
    # insert new record in to job_category table
    with job_service_db:
        my_cursor = job_service_db.cursor()
        sql = "INSERT INTO job_categories (job_id, category_id) VALUES (%s, %s)"
        val = (job_category["job_id"], job_category["category_id"])
        my_cursor.execute(sql, val)
        job_service_db.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} job_category has been inserted successfully"


def __validate(req: dict):
    if req.get("job_id") is None or is_integer(req.get("job_id")) is False:
        return False, "job_id cannot be null and must be number"
    if req.get("category_id") is None or is_integer(req.get("category_id")) is False:
        return False, "category_id cannot be null and must be number"
    return req, ""


def _check_category_id(category_id: int):
    # check benefit_id
    http = urllib3.PoolManager()
    r = http.request('GET', f'http://localhost:5003/categories/{category_id}')
    if r.status != 200:
        return False, f"category_id is not exist"
    return True, None


@job_category_router.get('/job-categories/{id}', status_code=200)
def detail_job_category(id: int, response: Response):
    with job_service_db:
        my_cursor = job_service_db.cursor()
        my_cursor.execute("SELECT * FROM job_categories WHERE id = %d" % id)
        job_category = my_cursor.fetchone()
        if job_category is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"id is not correct"
        return True, job_category_result(job_category)


@job_category_router.get('/job-categories', status_code=200)
def all_job_category(page: int, limit: int, response: Response):
    with job_service_db:
        my_cursor = job_service_db.cursor()
        my_cursor.execute("SELECT COUNT(id) FROM job_categories")
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
        my_cursor.execute("SELECT * FROM job_categories LIMIT %s OFFSET %s", (limit, offset))
        job_category = my_cursor.fetchall()
        if job_category is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return job_category_list_result(job_category)


@job_category_router.put('/job-categories/{id}', status_code=200)
async def update_job_category(id: int, req: JobCategory, response: Response):
    job_category = req.job_category_to_dict()
    boolean, result = detail_job_category(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check have some changes or not
    ok, msg = __check_changes(result, job_category)
    response.status_code = status.HTTP_400_BAD_REQUEST
    if ok is False:
        return msg
    # check job_id valid or not:
    ok, result = detail_job(job_category["job_id"], response)
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return result
    # check category_id valid or not:
    ok, txt = _check_category_id(job_category["category_id"])
    if ok is False:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return txt
    with job_service_db:
        my_cursor = job_service_db.cursor()
        sql = "UPDATE job_categories SET job_id = %s, category_id = %s   WHERE id = %s"
        val = (job_category["job_id"], job_category["category_id"], id)
        my_cursor.execute(sql, val)
        response.status_code = status.HTTP_200_OK
        return f"{my_cursor.rowcount} row affected"


def __check_changes(req: dict, new_req: dict):
    if req["job_id"] == new_req["job_id"] and req["category_id"] == new_req["category_id"]:
        return False, "no information have been changed"
    return new_req, ""


@job_category_router.delete('/job-categories/{id}', status_code=204)
async def delete_job_category(id: int, response: Response):
    boolean, result = detail_job_category(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with job_service_db:
        my_cursor = job_service_db.cursor()
        my_cursor.execute("DELETE FROM job_categories WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
