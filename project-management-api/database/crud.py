from sqlalchemy import func
from sqlmodel import Session, select

from datatypes.models import User, Project, Document, ProjectPermission, ProjPermissions, DocPermissions, \
    DocumentPermission, SysPermissions, SystemPermission

def get_user(session: Session, user_name: str) -> User:
    return session.exec(
        select(User).where(User.user_name == user_name)
    ).first()

def get_users_count(session: Session):
    return session.exec(select([func.count(User.user_name)])).one()

def get_projects(session: Session):
    return session.exec(select(Project)).all()


def get_project_by_name(session: Session, project_name: str):
    return session.exec(select(Project).where(Project.project_name == project_name)).first()


def get_document_of_project(session: Session, project_name: str, document_name: str):
    return session.exec(select(Document)
                        .where(Document.project_name == project_name)
                        .where(Document.document_name == document_name)
                        ).first()

def get_system_permission(session: Session, user_name: str, permission: SysPermissions):
    return session.exec(select(SystemPermission)
                        .where(SystemPermission.user_name  == user_name)
                        .where(SystemPermission.permission == permission)
                        ).first()

def get_project_permission(session: Session, user_name: str, project_name: str, permission: ProjPermissions):
    return session.exec(select(ProjectPermission)
                        .where(ProjectPermission.user_name    == user_name)
                        .where(ProjectPermission.project_name == project_name)
                        .where(ProjectPermission.permission   == permission)
                        ).first()

def get_project_permissions(session: Session, user_name: str, project_name: str):
    return session.exec(select(ProjectPermission)
                        .where(ProjectPermission.user_name    == user_name)
                        .where(ProjectPermission.project_name == project_name)
                        ).all()

def get_document_permission(session: Session, user_name: str, project_name: str, document_name: str, permission: DocPermissions):
    return session.exec(select(DocumentPermission)
                        .where(DocumentPermission.user_name     == user_name)
                        .where(DocumentPermission.project_name  == project_name)
                        .where(DocumentPermission.document_name == document_name)
                        .where(DocumentPermission.permission    == permission)
                        ).first()

def get_document_permissions(session: Session, user_name: str, project_name: str, document_name: str):
    return session.exec(select(DocumentPermission)
                        .where(DocumentPermission.user_name     == user_name)
                        .where(DocumentPermission.project_name  == project_name)
                        .where(DocumentPermission.document_name == document_name)
                        ).all()
