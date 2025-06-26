from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    language: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int
    
    class Config:
        from_attributes = True

class CodeIssueResponse(BaseModel):
    id: int
    line_number: int
    column_number: Optional[int]
    severity: str
    category: str
    message: str
    rule_name: Optional[str]
    suggestion: Optional[str]
    is_fixed: bool
    
    class Config:
        from_attributes = True

class CodeAnalysisResponse(BaseModel):
    id: int
    filename: str
    language: str
    score: Optional[int]
    created_at: datetime
    issues: List[CodeIssueResponse]
    analysis_results: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class AnalyzeCodeRequest(BaseModel):
    filename: str
    content: str
    language: str
    project_id: Optional[int] = None