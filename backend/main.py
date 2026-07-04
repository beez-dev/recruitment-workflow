from fastapi import FastAPI

import models  # noqa: F401 — ensures models are registered

app = FastAPI()


@app.get("/health")
def read_health():
    return {"message": "App is running..."}
