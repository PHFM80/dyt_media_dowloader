#services\project_manager_service.py
from pathlib import Path
from typing import Optional
from models.project import Project
from utils.path_utils import create_project_dir, get_downloads_dir


class ProjectManagerService:
    """Servicio para gestionar proyectos de descarga"""
    
    def __init__(self):
        self.current_project: Optional[Project] = None
    
    def create_project(self, name: str = "", is_single_session: bool = False) -> Project:
        """Crea un nuevo proyecto"""
        project = Project(name=name, is_single_session=is_single_session)
        project.base_path = create_project_dir(project.name)
        self.current_project = project
        return project
    
    def get_current_project(self) -> Optional[Project]:
        """Obtiene el proyecto actual"""
        return self.current_project
    
    def clear_current_project(self):
        """Limpia el proyecto actual"""
        if self.current_project:
            self.current_project.clear_downloads()
        self.current_project = None
    
    def ensure_project_exists(self, name: str = "", is_single_session: bool = False) -> Project:
        """Asegura que existe un proyecto, lo crea si no existe"""
        if self.current_project is None:
            return self.create_project(name, is_single_session)
        return self.current_project