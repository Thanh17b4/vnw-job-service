from datetime import date

from pydantic import BaseModel


class Job(BaseModel):
    name: str
    company_id: int
    level: str
    salary: str
    type: str
    cv_language: str
    due_at: date

    def job_to_dict(self):
        return vars(self)


def job_result(job) -> dict:
    return {
        "id": job[0],
        "name": job[1],
        "salary": job[2],
        "level": job[3],
        "cv_language": job[4],
        "type": job[5],
        "slug": job[6],
        "company_id": int(job[7]),
        "created_at": job[8],
        "updated_at": job[9],
        "due_at": job[10]
    }


def job_list_result(jobs) -> list:
    return [job_result(job) for job in jobs]
