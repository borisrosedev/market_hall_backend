from typing import Annotated
import logging
from pathlib import Path as P
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse 

from fastapi import APIRouter

BASE_DIR = P(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.DEBUG)


api_v1_files = APIRouter(
    tags=["files"]
)



@api_v1_files.post("/upload")
async def upload_file(file: UploadFile):
    return {"file_name": file.filename}

