from pydantic import BaseModel


class JobCategory(BaseModel):
    job_id: int
    category_id: int

    def job_category_to_dict(self):
        return vars(self)


def job_category_result(job_category) -> dict:
    return {
        "id": job_category[0],
        "job_id": job_category[1],
        "category_id": job_category[2],

    }


def job_category_list_result(job_categories) -> list:
    return [job_category_result(job_category) for job_category in job_categories]
