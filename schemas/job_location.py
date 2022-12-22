from datetime import datetime

from pydantic import BaseModel


class JobLocation(BaseModel):
    job_id: int
    location_id: int
    created_at: datetime or None = None
    updated_at: datetime or None = None

    def job_location_to_dict(self):
        return vars(self)


def job_location_result(job_location) -> dict:
    return {
        "id": job_location[2],
        "job_id": job_location[0],
        "location_id": int(job_location[1])
    }


def job_location_list_result(job_locations) -> list:
    return [job_location_result(job_location) for job_location in job_locations]
