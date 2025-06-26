from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Project
from app.schemas import ProjectCreate, ProjectResponse
from app.services.auth_service import AuthService
from app.services.project_service import ProjectService

router = APIRouter()
auth_service = AuthService()
project_service = ProjectService()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.create_project(db, project, current_user.id)

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.get_user_projects(db, current_user.id)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    project = project_service.get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project