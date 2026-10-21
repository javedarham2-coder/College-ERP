
from fastapi import FastAPI

app = FastAPI(
    title="College ERP API",
    description="Admission and Student Management System",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
