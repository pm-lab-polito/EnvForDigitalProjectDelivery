import enum

from sqlmodel import Session

from database import crud
from datatypes.models import Document, User, ProjPermissions, DocPermissions, Project, SysPermissions


class Permissions(str, enum.Enum):
    create = "create"
    view = "view"
    edit = "edit"
    delete = "delete"
    edit_permissions = "edit_permissions"


class PermissionUtils:
    def __init__(self, session: Session, user_name: str, project_name: str = None, document_name: str = None):
        self.session = session
        self.user_name = user_name
        self.project_name = project_name
        self.document_name = document_name

    def has_sys_perm(self, permission: SysPermissions):
        return (permission is not None
                and crud.get_system_permission(
                    session=self.session,
                    user_name=self.user_name,
                    permission=permission) is not None)

    def has_proj_perm(self, permission: ProjPermissions):
        return (permission is not None
                and self.project_name is not None
                and crud.get_project_permission(
                    session=self.session,
                    user_name=self.user_name,
                    project_name=self.project_name,
                    permission=permission) is not None)

    def has_doc_perm(self, permission: DocPermissions):
        return (permission is not None
                and self.document_name is not None
                and crud.get_document_permission(
                    session=self.session,
                    user_name=self.user_name,
                    project_name=self.project_name,
                    document_name=self.document_name,
                    permission=permission) is not None)


document_map = {
    Permissions.create:           (SysPermissions.edit_projects, ProjPermissions.create_documents,           None),
    Permissions.view:             (SysPermissions.view_projects, ProjPermissions.view_documents,             DocPermissions.view),
    Permissions.edit:             (SysPermissions.edit_projects, ProjPermissions.edit_documents,             DocPermissions.edit),
    Permissions.delete:           (SysPermissions.edit_projects, ProjPermissions.delete_documents,           DocPermissions.delete),
    Permissions.edit_permissions: (SysPermissions.edit_projects, ProjPermissions.edit_documents_permissions, DocPermissions.edit_permissions)
}


def has_document_permission(session: Session, user: User, project: Project, document: Document, permission: Permissions):
    if project is None:
        return False
    if user.user_name == project.owner_name:
        return True
    if document is None:
        perm = PermissionUtils(session, user.user_name, project.project_name)
    else:
        if user.user_name == document.author_name:
            return True
        perm = PermissionUtils(session, user.user_name, document.project_name, document.document_name)

    if permission not in document_map.keys():
        return False
    p = document_map[permission]
    return (
        perm.has_sys_perm(p[0])
        or perm.has_proj_perm(p[1])
        or perm.has_doc_perm(p[2])
    )


project_map = {
    Permissions.create:           (SysPermissions.create_projects,           ProjPermissions.create_documents),
    Permissions.view:             (SysPermissions.view_projects,             ProjPermissions.view_documents),
    Permissions.edit:             (SysPermissions.edit_projects,             ProjPermissions.edit_documents),
    Permissions.delete:           (SysPermissions.delete_projects,           ProjPermissions.delete_documents),
    Permissions.edit_permissions: (SysPermissions.edit_projects_permissions, ProjPermissions.edit_documents_permissions)

}


def has_project_permission(session: Session, user: User, project: Project, permission: Permissions):
    if project is None:
        perm = PermissionUtils(session, user.user_name)
    else:
        if user.user_name == project.owner_name:
            return True
        perm = PermissionUtils(session, user.user_name, project.project_name)
    if permission not in project_map.keys():
        return False
    p = document_map[permission]
    return (
        perm.has_sys_perm(p[0])
        or perm.has_proj_perm(p[1])
    )


system_map = {
    # Permissions.create not implemented
    Permissions.view:             SysPermissions.view_users,
    Permissions.edit:             SysPermissions.edit_users,
    Permissions.delete:           SysPermissions.delete_users,
    Permissions.edit_permissions: SysPermissions.edit_users_permissions
}

def has_system_user_permission(session: Session, user: User, permission: Permissions):
    perm = PermissionUtils(session, user.user_name)
    if permission not in system_map.keys():
        return False
    p = system_map[permission]
    return perm.has_sys_perm(p)
