import os
import tempfile
import subprocess
import json
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.models import CodeAnalysis, CodeIssue, Project
from app.schemas import AnalyzeCodeRequest
from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.javascript_analyzer import JavaScriptAnalyzer

class AnalysisService:
    def __init__(self):
        self.analyzers = {
            "python": PythonAnalyzer(),
            "javascript": JavaScriptAnalyzer(),
            "typescript": JavaScriptAnalyzer(),
        }
    
    def detect_language(self, filename: str) -> str:
        extension = filename.split('.')[-1].lower()
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript',
            'kt': 'kotlin',
            'java': 'java'
        }
        return language_map.get(extension, 'text')
    
    async def analyze_code(self, db: Session, request: AnalyzeCodeRequest, user_id: int) -> CodeAnalysis:
        analyzer = self.analyzers.get(request.language)
        if not analyzer:
            raise ValueError(f"Unsupported language: {request.language}")
        
        # Run analysis
        issues = await analyzer.analyze(request.content, request.filename)
        analysis_results = analyzer.get_metrics(request.content)
        
        # Calculate overall score
        score = self.calculate_score(issues, analysis_results)
        
        # Save to database
        db_analysis = CodeAnalysis(
            filename=request.filename,
            file_content=request.content,
            language=request.language,
            analysis_results=analysis_results,
            score=score,
            project_id=request.project_id
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Save issues
        for issue_data in issues:
            db_issue = CodeIssue(
                line_number=issue_data["line"],
                column_number=issue_data.get("column"),
                severity=issue_data["severity"],
                category=issue_data["category"],
                message=issue_data["message"],
                rule_name=issue_data.get("rule"),
                suggestion=issue_data.get("suggestion"),
                analysis_id=db_analysis.id
            )
            db.add(db_issue)
        
        db.commit()
        db.refresh(db_analysis)
        return db_analysis
    
    def calculate_score(self, issues: List[Dict], metrics: Dict) -> int:
        # Simple scoring algorithm (can be enhanced with ML later)
        base_score = 100
        
        for issue in issues:
            if issue["severity"] == "error":
                base_score -= 10
            elif issue["severity"] == "warning":
                base_score -= 5
            elif issue["severity"] == "info":
                base_score -= 1
        
        # Consider complexity metrics if available
        if "complexity" in metrics and metrics["complexity"] > 10:
            base_score -= (metrics["complexity"] - 10) * 2
        
        return max(0, min(100, base_score))
    
    def get_analysis(self, db: Session, analysis_id: int) -> CodeAnalysis:
        return db.query(CodeAnalysis).filter(CodeAnalysis.id == analysis_id).first()