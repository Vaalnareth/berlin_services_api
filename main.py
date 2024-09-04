from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.routes import router
import uvicorn

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Service API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)