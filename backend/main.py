from fastapi import FastAPI

import models  # noqa: F401 — registers all ORM models
from routers import auth, candidates

app = FastAPI()

app.include_router(auth.router)
app.include_router(candidates.router)


@app.get("/health")
def read_health():
    return {"message": "App is running..."}
