from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.attachment_repo import AttachmentRepository
from app.schemas.attachment import AttachmentResponse
from app.storage.local_storage import LocalStorage
from app.storage.service import StorageService
from app.core.response import success_response
from app.db.phase1_store import store_create, using_phase1_store
import os

router = APIRouter()
storage = LocalStorage()
_storage_service = StorageService()


@router.get("/investigation/{investigation_id}")
async def list_attachments(investigation_id: int, db: AsyncSession = Depends(get_db)):
    repo = AttachmentRepository(db)
    attachments = await repo.get_by_investigation(investigation_id)
    return success_response(data=[AttachmentResponse.model_validate(a).model_dump() for a in attachments])


@router.post("/upload")
async def upload_attachment(
    investigation_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    contents = await file.read()
    filename = f"inv_{investigation_id}_{file.filename}"

    use_catalyst_files = (os.getenv("STORAGE_PROVIDER") or os.getenv("DB_PROVIDER") or "").lower() == "catalyst"
    file_id = None
    folder_id = None
    if use_catalyst_files or using_phase1_store():
        meta = await _storage_service.upload(filename, contents, folder="attachments")
        path = meta["path"]
        file_id = meta.get("file_id")
        folder_id = meta.get("folder_id")
        if using_phase1_store():
            row = await store_create(
                "attachments",
                {
                    "investigation_id": investigation_id,
                    "filename": file.filename,
                    "file_path": path,
                    "file_id": file_id,
                    "folder_id": folder_id,
                    "file_size": len(contents),
                    "file_type": file.content_type,
                },
            )
            return success_response(data=row, message="Attachment uploaded")
    else:
        path = await storage.upload(filename, contents)

    repo = AttachmentRepository(db)
    payload = {
        "investigation_id": investigation_id,
        "filename": file.filename,
        "file_path": path,
        "file_size": len(contents),
        "file_type": file.content_type,
    }
    attachment = await repo.create(payload)
    data = AttachmentResponse.model_validate(attachment).model_dump()
    if file_id:
        data["file_id"] = file_id
        data["folder_id"] = folder_id
    return success_response(data=data, message="Attachment uploaded")


@router.delete("/{attachment_id}")
async def delete_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    repo = AttachmentRepository(db)
    attachment = await repo.get_by_id(attachment_id)
    if attachment:
        await storage.delete(attachment.filename)
    deleted = await repo.delete(attachment_id)
    return success_response(message="Attachment deleted" if deleted else "Attachment not found")
