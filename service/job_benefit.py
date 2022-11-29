import urllib3
from starlette import status
from jobs.model.check_data import is_integer
from jobs.config import mydb
from jobs.schemas.schemas import JobBenefitResult, JobBenefit, JobBenefitListResult
from fastapi import APIRouter, Response
from .jobs import detail_job
job_benefit_router = APIRouter()


@job_benefit_router.post('/job-benefit/create', status_code=201)
def create_job_benefit(request: JobBenefit, response: Response):
    job_benefit = request.job_benefit_to_dict()
    # Validate data
    is_ok, msg = __validate(job_benefit)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    # check job_id valid or not
    ok, result = detail_job(job_benefit["job_id"], response)
    if ok is False:
        return result
    # check benefit_id valid or not:
    ok, txt = _check_exist(job_benefit["benefit_id"])
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return txt
    # insert new record in to job_benefits table
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO job_benefits (job_id, benefit_id) VALUES (%s, %s)"
        val = (job_benefit["job_id"], job_benefit["benefit_id"])
        my_cursor.execute(sql, val)
        mydb.commit()
        return f"{my_cursor.rowcount} job_benefit has been inserted successfully"


def __validate(req: dict):
    if req.get("job_id") is None or is_integer(req.get("job_id")) is False:
        return False, "job_id cannot be null and must be number"
    if req.get("benefit_id") is None or is_integer(req.get("benefit_id")) is False:
        return False, "benefit_id cannot be null and must be number"
    return req, ""


def _check_exist(benefit_id: int):
    # check benefit_id
    http = urllib3.PoolManager()
    r = http.request('GET', f'http://localhost:5004/benefit/detail/{benefit_id}')
    if r.status != 200:
        return False, f"benefit_id is not exist"
    return True, None


@job_benefit_router.get('/job-benefit/detail/{id}', status_code=200)
def detail_job_benefit(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM job_benefits WHERE id = %d" % id)
        job_benefit = my_cursor.fetchone()
        if job_benefit is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"id is not correct"
        return True, JobBenefitResult(job_benefit)


@job_benefit_router.get('/job-benefit/all/', status_code=200)
def all_job_benefit(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(id) FROM job_benefits")
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
        my_cursor.execute("SELECT * FROM job_benefits LIMIT %s OFFSET %s", (limit, offset))
        job_benefit_list = my_cursor.fetchall()
        if job_benefit_list is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return JobBenefitListResult(job_benefit_list)


@job_benefit_router.put('/job-benefit/update/{id}', status_code=200)
async def update_job_benefit(id: int, req: JobBenefit, response: Response):
    # check id is existed or not
    boolean, result = detail_job_benefit(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    new_job_benefit = req.job_benefit_to_dict()
    # check have some changes or not
    ok, msg = __check_exist(result, new_job_benefit)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    # check job_id valid or not
    ok, result = detail_job(new_job_benefit["job_id"], response)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check benefit_id valid or not:
    ok, txt = _check_exist(new_job_benefit["benefit_id"])
    if ok is False:
        return txt
    # update record
    with mydb:
        my_cursor = mydb.cursor()
        sql = "UPDATE job_benefits SET job_id = %s, benefit_id = %s   WHERE id = %s"
        val = (new_job_benefit["job_id"], new_job_benefit["benefit_id"], id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_exist(old_result: dict, new_req: dict):
    if new_req == old_result.copy().pop('id'):
        return False, "no information have been changed"
    return True, None


@job_benefit_router.delete('/job-benefit/delete/{id}', status_code=200)
async def delete_job_category(id: int, response: Response):
    boolean, result = detail_job_benefit(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM job_benefits WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
