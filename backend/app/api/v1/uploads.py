from fastapi import APIRouter, UploadFile, File
from app.core.response import success_response
from app.storage.local_storage import LocalStorage
import structlog

router = APIRouter()
logger = structlog.get_logger()
storage = LocalStorage()


@router.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = f"{file.filename}"
    path = await storage.upload(filename, contents)
    logger.info("file_uploaded", filename=filename, size=len(contents))

    return success_response(data={
        "filename": filename,
        "size": len(contents),
        "url": f"/api/v1/uploads/{filename}",
    })


@router.get("/uploads/{filename}")
async def download_file(filename: str):
    from fastapi.responses import Response

    contents = await storage.download(filename)
    if contents is None:
        return success_response(message="File not found")

    return Response(content=contents, media_type="application/octet-stream")
