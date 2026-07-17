from fastapi import APIRouter, UploadFile, File, HTTPException
from app.storage.service import StorageService
from app.core.response import success_response

router = APIRouter()

storage_service = StorageService()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), folder: str = "uploads"):
    content = await file.read()
    result = await storage_service.upload(file.filename, content, folder)
    return success_response(data=result, message="File uploaded")


@router.get("/download/{path:path}")
async def download_file(path: str):
    try:
        content = await storage_service.download(path)
        from fastapi.responses import Response
        return Response(content=content, media_type="application/octet-stream")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{path:path}")
async def delete_file(path: str):
    deleted = await storage_service.delete(path)
    return success_response(message="Deleted" if deleted else "Not found")


@router.get("/list")
async def list_files(folder: str = "uploads"):
    files = await storage_service.list_files(folder)
    return success_response(data=files)


@router.get("/exists/{path:path}")
async def file_exists(path: str):
    exists = await storage_service.exists(path)
    return success_response(data={"exists": exists})
