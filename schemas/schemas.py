from datetime import datetime, date

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


class JobLocation(BaseModel):
    job_id: int
    location_id: int
    created_at: datetime or None = None
    updated_at: datetime or None = None

    def job_location_to_dict(self):
        return vars(self)


class JobBenefit(BaseModel):
    job_id: int
    benefit_id: int

    def job_benefit_to_dict(self):
        return vars(self)


class JobCategory(BaseModel):
    job_id: int
    category_id: int
    created_at: datetime or None = None
    updated_at: datetime or None = None

    def job_category_to_dict(self):
        return vars(self)


def JobResult(job) -> dict:
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


def JobListResult(jobs) -> list:
    return [JobResult(job) for job in jobs]


def JobLocationResult(job_location) -> dict:
    return {
        "id": job_location[2],
        "job_id": job_location[0],
        "location_id": int(job_location[1])

    }


def JobLocationListResult(job_locations) -> list:
    return [JobLocationResult(job_location) for job_location in job_locations]


def JobCategoryResult(job_category) -> dict:
    return {
        "id": job_category[0],
        "job_id": job_category[1],
        "category_id": job_category[2],

    }


def JobCategoryListResult(job_categories) -> list:
    return [JobCategoryResult(job_category) for job_category in job_categories]


def JobBenefitResult(job_benefit) -> dict:
    return {
        "id": job_benefit[0],
        "job_id": job_benefit[1],
        "benefit_id": job_benefit[2],

    }


def JobBenefitListResult(job_benefits) -> list:
    return [JobBenefitResult(job_benefit) for job_benefit in job_benefits]
