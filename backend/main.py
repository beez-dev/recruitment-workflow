from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def read_health():
    return {"message": "App is running..."}
