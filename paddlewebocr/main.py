from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from route import router

app = FastAPI()
app.mount("/", StaticFiles(directory=os.path.join(".", "webui", "dist"), html=True), name="static")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
