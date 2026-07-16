from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.attachment_repo import AttachmentRepository
from app.schemas.attachment import AttachmentCreate, AttachmentResponse
from app.storage.local_storage import LocalStorage
from app.core.response import success_response

router = APIRouter()
storage = LocalStorage()


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
    path = await storage.upload(filename, contents)

    repo = AttachmentRepository(db)
    attachment = await repo.create({
        "investigation_id": investigation_id,
        "filename": file.filename,
        "file_path": path,
        "file_size": len(contents),
        "file_type": file.content_type,
    })

    return success_response(
        data=AttachmentResponse.model_validate(attachment).model_dump(),
        message="Attachment uploaded"
    )


@router.delete("/{attachment_id}")
async def delete_attachment(attachment_id: int, db: AsyncSession = Depends(get_db)):
    repo = AttachmentRepository(db)
    attachment = await repo.get_by_id(attachment_id)
    if attachment:
        await storage.delete(attachment.filename)
    deleted = await repo.delete(attachment_id)
    return success_response(message="Attachment deleted" if deleted else "Attachment not found")
