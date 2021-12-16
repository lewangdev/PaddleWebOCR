import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import click

from router import router

app = FastAPI()

app.include_router(router, prefix="/api")
app.mount("/", StaticFiles(directory=os.path.join(".", "webui", "dist"), html=True), name="static")


@click.command()
@click.option("--bind", default='0.0.0.0', help="service bind address")
@click.option("--port", default=8080, help="service port")
def main(bind, port):
    import uvicorn
    uvicorn.run(app, host=bind, port=port)


if __name__ == "__main__":
    main()
