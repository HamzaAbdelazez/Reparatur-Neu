import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED
from api.routers.dependencies import db_dependency
from api.models.uploaded_pdf import UploadedPdfOut, UploadedPdfIn
from api.service.uploaded_pdf import UploadedPdfService

router = APIRouter(prefix="/uploadedPdfs", tags=["uploadedPdfs"])


@router.post(
    path="/",
    operation_id="UploadPdf",
    status_code=HTTP_201_CREATED,
    response_model=UploadedPdfOut,
)
async def upload_pdf(
        file: UploadFile = File(...),
        user_id: str = "00000000-0000-0000-0000-000000000000",
        db: AsyncSession = Depends(db_dependency)
):
    # ✅ MIME type validation
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # ✅ Optional filename extension check (extra safeguard)
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must have a .pdf extension.")

    content = await file.read()

    uploaded_pdf_service = UploadedPdfService(db=db)
    return await uploaded_pdf_service.upload_pdf(
        uploaded_pdf_in=UploadedPdfIn(
            user_id=uuid.UUID(user_id),
            title=file.filename,
            content=content,
            file_size=len(content),
        )
    )