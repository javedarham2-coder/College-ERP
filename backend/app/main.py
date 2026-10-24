from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database_connection
from app.routers.admissions import router as admissions_router
from app.routers.students import router as students_router


app = FastAPI(
    title="College ERP API",
    description="Admission and Student Management System",
    version="0.1.0",
)

app.include_router(admissions_router)
app.include_router(students_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def database_health_check():
    try:
        check_database_connection()
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection unavailable",
        )