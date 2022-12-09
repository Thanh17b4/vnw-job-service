import urllib3
from fastapi import APIRouter, Response
from slugify import slugify
from starlette import status

from db import mydb
from model.check_data import is_blank, is_integer
from schemas.schemas import Job, JobResult, JobListResult

job_router = APIRouter()


@job_router.post('/jobs', status_code=201)
def create_job(request: Job, response: Response):
    job = request.job_to_dict()
    # Validate data
    is_ok, msg = __validate(job)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    # check company_id is existed or not
    ok, result = _check_account_exist(job["company_id"])
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # create job
    slug = slugify(job["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO jobs (name, cv_language, type, slug, company_id, level, due_at, salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (job["name"], job["cv_language"], job["type"], slug, job["company_id"], job["level"], job["due_at"],
               job["salary"])
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} job has been inserted successfully"


def __validate(req: dict):
    if req.get("name") is None or is_blank(req.get("name")) is True:
        return False, "name cannot be null"
    if req.get("cv_language") is None or is_blank(req.get("cv_language")) is True:
        return False, "cv_language cannot be null"
    if req.get("level") is None or is_blank(req.get("level")) is True:
        return False, "level cannot be null"
    if req.get("salary") is None or is_blank(req.get("salary")) is True:
        return False, "salary cannot be null"
    if req.get("company_id") is None or is_integer(req.get("company_id")) is False:
        return False, "company_id cannot be null"
    if req.get("due_at") is None:
        return False, "due_at cannot be null"
    return req, ""


def _check_account_exist(id: int):
    http = urllib3.PoolManager()
    r = http.request('GET', f'http://localhost:5002/company/{id}')
    if r.status != 200:
        return False, f"company_id is not exist"
    return True, None


@job_router.get('/jobs/{id}', status_code=200)
def detail_job(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM jobs WHERE id = %d" % id)
        job = my_cursor.fetchone()
        if job is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"job_id is not correct"
        return True, JobResult(job)


@job_router.get('/jobs', status_code=200)
def all_job(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(id) FROM jobs")
        total_jobs = my_cursor.fetchone()[0]
        d = total_jobs % limit
        if d == 0:
            total_page = total_jobs // limit
        else:
            total_page = total_jobs // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute("SELECT * FROM jobs ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        jobs = my_cursor.fetchall()
        if jobs is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return JobListResult(jobs)


@job_router.put('/jobs/{id}', status_code=200)
async def update_job(id: int, req: Job, response: Response):
    job = req.job_to_dict()
    boolean, result = detail_job(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    ok, result = _check_account_exist(job["company_id"])
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        slug = slugify(job["name"])
        sql = "UPDATE jobs SET name = %s, level = %s, cv_language = %s, type = %s, company_id = %s, due_at = %s, slug = %s   WHERE id = %s"
        val = (job["name"], job["level"], job["cv_language"], job["type"], job["company_id"], job["due_at"], slug, id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


@job_router.delete('/jobs/{id}', status_code=200)
async def delete_job(id: int, response: Response):
    boolean, result = detail_job(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM jobs WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
