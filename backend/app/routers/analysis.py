from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import AnalyzeCodeRequest, CodeAnalysisResponse
from app.services.auth_service import AuthService
from app.services.analysis_service import AnalysisService

router = APIRouter()
auth_service = AuthService()
analysis_service = AnalysisService()

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: AnalyzeCodeRequest,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return await analysis_service.analyze_code(db, request, current_user.id)

@router.post("/upload", response_model=CodeAnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    project_id: int = None,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type not in ["text/plain", "application/x-python-code"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    content = await file.read()
    content_str = content.decode("utf-8")
    
    # Detect language from file extension
    language = analysis_service.detect_language(file.filename)
    
    request = AnalyzeCodeRequest(
        filename=file.filename,
        content=content_str,
        language=language,
        project_id=project_id
    )
    
    return await analysis_service.analyze_code(db, request, current_user.id)

@router.get("/{analysis_id}", response_model=CodeAnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    analysis = analysis_service.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Check if user owns the project
    if analysis.project and analysis.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return analysis