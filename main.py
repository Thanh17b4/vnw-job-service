import uvicorn
from fastapi import FastAPI

from service.job_benefit import job_benefit_router
from service.job_category import job_category_router
from service.job_location import job_location_router
from service.jobs import job_router

app = FastAPI(docs_url='/')
app.include_router(job_router)
app.include_router(job_location_router)
app.include_router(job_category_router)
app.include_router(job_benefit_router)

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
