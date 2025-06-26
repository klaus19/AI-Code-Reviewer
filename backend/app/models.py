from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.relationship import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    language = Column(String, nullable=False)  # python, javascript, kotlin, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="projects")
    analyses = relationship("CodeAnalysis", back_populates="project")

class CodeAnalysis(Base):
    __tablename__ = "code_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_content = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    analysis_results = Column(JSON)  # Store analysis results as JSON
    score = Column(Integer)  # Overall code quality score (0-100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="analyses")
    issues = relationship("CodeIssue", back_populates="analysis")

class CodeIssue(Base):
    __tablename__ = "code_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, nullable=False)
    column_number = Column(Integer)
    severity = Column(String, nullable=False)  # error, warning, info
    category = Column(String, nullable=False)  # style, security, performance, bug
    message = Column(Text, nullable=False)
    rule_name = Column(String)
    suggestion = Column(Text)
    is_fixed = Column(Boolean, default=False)
    analysis_id = Column(Integer, ForeignKey("code_analyses.id"))
    
    analysis = relationship("CodeAnalysis", back_populates="issues")