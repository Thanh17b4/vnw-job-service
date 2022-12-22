from pydantic import BaseModel


class JobBenefit(BaseModel):
    job_id: int
    benefit_id: int

    def job_benefit_to_dict(self):
        return vars(self)


def job_benefit_result(job_benefit) -> dict:
    return {
        "id": job_benefit[0],
        "job_id": job_benefit[1],
        "benefit_id": job_benefit[2],

    }


def job_benefit_list_result(job_benefits) -> list:
    return [job_benefit_result(job_benefit) for job_benefit in job_benefits]
