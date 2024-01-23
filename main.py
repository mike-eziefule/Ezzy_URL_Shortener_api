"""Main FastAPI App."""
from fastapi import FastAPI
from database import engine
from models import Base
from routes import admin, url



app = FastAPI(
    title="Ezzy URL Shortener",
    description="A FastAPI-based URL shortener and redirector.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)


app.include_router(url.router)
app.include_router(admin.router)