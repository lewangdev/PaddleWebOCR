import os
import click
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from paddlewebocr.pkg.config import settings
from paddlewebocr.route.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount("/", StaticFiles(directory=os.path.join(".", "webui", "dist"), html=True), name="static")


@click.command()
@click.option("--bind", default='0.0.0.0', help="service bind address")
@click.option("--port", default=8080, help="service port")
def main(bind, port):
    import uvicorn
    uvicorn.run(app, host=bind, port=port)


if __name__ == "__main__":
    main()
