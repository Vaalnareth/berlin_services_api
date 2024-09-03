from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routes import router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Service API!"}
