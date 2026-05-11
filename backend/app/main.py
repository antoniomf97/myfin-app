from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import engine, Base
from app.routers import transactions

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API", version="1.0.0")

# CORS configuration (allows React frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}
