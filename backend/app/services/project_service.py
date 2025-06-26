from sqlalchemy.orm import Session
from typing import List
from app.models import Project
from app.schemas import ProjectCreate

class ProjectService:
    def create_project(self, db: Session, project: ProjectCreate, user_id: int) -> Project:
        db_project = Project(**project.dict(), owner_id=user_id)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def get_project(self, db: Session, project_id: int) -> Project:
        return db.query(Project).filter(Project.id == project_id).first()
    
    def get_user_projects(self, db: Session, user_id: int) -> List[Project]:
        return db.query(Project).filter(Project.owner_id == user_id).all()