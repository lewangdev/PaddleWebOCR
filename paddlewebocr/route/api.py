from fastapi import APIRouter

from paddlewebocr.route.v1 import ocr

api_router = APIRouter()
api_router.include_router(ocr.router, tags=["ocr"])
