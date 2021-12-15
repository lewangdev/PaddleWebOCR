import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from router import router


app = FastAPI()
app.include_router(router, prefix="/api")
app.mount("/", StaticFiles(directory=os.path.join(".", "webui", "dist"), html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
