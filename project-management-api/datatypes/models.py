import enum
from datetime import datetime
from typing import Dict, List

import sqlalchemy.orm
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlmodel import SQLModel, Field, Relationship, JSON


class StringFields(type):
    """Helper class that prepends the table name to the fields"""
    def __getattribute__(self, item):
        if item != "table_name":
            return f'{object.__getattribute__(self, "table_name")}.{object.__getattribute__(self, item)}'
        return object.__getattribute__(self, item)


class UserBase(SQLModel):
    user_name: str


class UserCreate(UserBase):
    password: str


class User(SQLModel, table=True):
    # field name | type | options
    user_name    : str  = Field(default=None, primary_key=True)
    password     : str  = Field(nullable=False)

    # relationship name  | type                       | options
    system_permissions   : List["SystemPermission"]   = Relationship(back_populates="user")
    project_permissions  : List["ProjectPermission"]  = Relationship(back_populates="user")
    documents_permissions: List["DocumentPermission"] = Relationship(back_populates="user")
    owned_projects       : List["Project"]            = Relationship(back_populates="owner")

    class Fields(metaclass=StringFields):
        table_name = "user"
        user_name  = "user_name"
        password   = "password"


class SysPermissions(str, enum.Enum):
    create_projects = "create_projects"
    view_projects   = "view_projects"
    edit_projects   = "edit_projects"
    delete_projects = "delete_projects"

    view_users   = "view_users"
    edit_users   = "edit_users"
    delete_users = "delete_users"

    edit_users_permissions    = "edit_users_permissions"
    edit_projects_permissions = "edit_projects_permissions"

class SystemPermission(SQLModel, table=True):
    # field name | type           | options
    user_name    : str            = Field(default=None, primary_key=True, foreign_key=User.Fields.user_name)
    permission   : SysPermissions = Field(sa_column=Column(Enum(SysPermissions), primary_key=True))

    # relationship name | type | options
    user                : User = Relationship(back_populates="system_permissions")

    class Fields(metaclass=StringFields):
        table_name = "systempermission"
        user_name  = "user_name"
        permission = "permission"


class Project(SQLModel, table=True):
    # field name | type | options
    project_name : str  = Field(default=None, primary_key=True)
    owner_name   : str  = Field(default=None, foreign_key=User.Fields.user_name)

    # relationship name | type                      | options
    owner               : User                      = Relationship(back_populates="owned_projects")
    documents           : List["Document"]          = Relationship(back_populates="project",
                                                                   sa_relationship_kwargs={
                                                                       "cascade": "all, delete, delete-orphan"})
    users_permissions   : List["ProjectPermission"] = Relationship(back_populates="project",
                                                                   sa_relationship_kwargs={
                                                                       "cascade": "all, delete, delete-orphan"})
    processes           : List["Process"]           = Relationship(back_populates="project",
                                                                   sa_relationship_kwargs={
                                                                       "cascade": "all, delete, delete-orphan"})

    class Fields(metaclass=StringFields):
        table_name   = "project"
        project_name = "project_name"
        owner_name   = "owner_name"


class ProjPermissions(str, enum.Enum):
    view   = "view"
    edit   = "edit"
    delete = "delete"

    create_documents = "create_documents"
    view_documents   = "view_documents"
    edit_documents   = "edit_documents"
    delete_documents = "delete_documents"

    edit_project_permissions   = "edit_project_permissions"
    edit_documents_permissions = "edit_documents_permissions"


class ProjectPermission(SQLModel, table=True):
    # field name | type            | options
    user_name    : str             = Field(default=None, primary_key=True, foreign_key=User.Fields.user_name)
    project_name : str             = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    permission   : ProjPermissions = Field(sa_column=Column(Enum(ProjPermissions), primary_key=True))

    # relationship name | type    | options
    user                : User    = Relationship(back_populates="project_permissions")
    project             : Project = Relationship(back_populates="users_permissions")

    class Fields(metaclass=StringFields):
        table_name = "projectpermission"
        user_name  = "user_name"
        permission = "permission"


class Document(SQLModel, table=True):
    # field name   | type            | options
    project_name   : str             = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    document_name  : str             = Field(default=None, primary_key=True)
    author_name    : str             = Field(default=None, foreign_key=User.Fields.user_name)
    jsonschema     : Dict            = Field(default={}, sa_column=Column(JSON))
    first          : Dict            = Field(default={}, sa_column=Column(JSON))
    last           : Dict            = Field(default={}, sa_column=Column(JSON))
    schema_add_date: datetime        = Field(default_factory=datetime.utcnow)
    creation_date  : datetime | None = Field(default=None)
    updated_date   : datetime | None = Field(default=None)

    # relationship name | type                       | options
    patches             : List["Patch"]              = Relationship(back_populates="document")
    project             : Project                    = Relationship(back_populates="documents")
    permissions         : List["DocumentPermission"] = Relationship(back_populates="document",
                                                                    sa_relationship_kwargs={
                                                                        "cascade": "all, delete, delete-orphan"})
    documents_processes : List["DocumentProcess"]    = Relationship(back_populates="document",
                                                                    sa_relationship_kwargs={
                                                                        "cascade": "all, delete, delete-orphan"})

    class Fields(metaclass=StringFields):
        table_name      = "document"
        project_name    = "project_name"
        document_name   = "document_name"
        author_name     = "author_name"
        jsonschema      = "jsonschema"
        first           = "first"
        last            = "last"
        schema_add_date = "schema_add_date"
        creation_date   = "creation_date"
        updated_date    = "updated_date"

    class Config:
        arbitrary_types_allowed = True


class Patch(SQLModel, table=True):
    # field name | type       | options
    id           : int | None = Field(default=None, primary_key=True)
    project_name : str        = Field(default=None, foreign_key=Project.Fields.project_name)
    document_name: str        = Field(default=None, foreign_key=Document.Fields.document_name)
    user_name    : str        = Field(default=None, foreign_key=User.Fields.user_name)
    updated_date : datetime   = Field(default_factory=datetime.utcnow)
    patch        : List[Dict] = Field(default={}, sa_column=Column(JSON))

    # relationship name | type     | options
    document            : Document = Relationship(back_populates="patches")

    class Fields(metaclass=StringFields):
        table_name    = "patch"
        project_name  = "project_name"
        document_name = "document_name"
        user_name     = "user_name"
        updated_date  = "updated_date"
        patch         = "patch"

    class Config:
        arbitrary_types_allowed = True


class DocPermissions(str, enum.Enum):
    view   = "view"
    edit   = "edit"
    delete = "delete"
    edit_permissions = "edit_permissions"


class DocumentPermission(SQLModel, table=True):
    # field name | type           | options
    project_name : str            = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    document_name: str | None     = Field(default=None, primary_key=True, foreign_key=Document.Fields.document_name)
    user_name    : str            = Field(default=None, primary_key=True, foreign_key=User.Fields.user_name)
    permission   : DocPermissions = Field(sa_column=Column(Enum(DocPermissions), primary_key=True))

    # relationship name | type     | options
    user                : User     = Relationship(back_populates="documents_permissions")
    document            : Document = Relationship(back_populates="permissions")

    class Fields(metaclass=StringFields):
        table_name    = "documentpermission"
        project_name  = "project_name"
        document_name = "document_name"
        user_name     = "user_name"
        permission    = "permission"


class Process(SQLModel, table=True):
    # field name | type | options
    project_name : str  = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    process_name : str  = Field(default=None, primary_key=True)

    # relationship name | type                    | options
    project             : Project                 = Relationship(back_populates="processes")
    documents_processes : List["DocumentProcess"] = Relationship(back_populates="process")

    class Fields(metaclass=StringFields):
        table_name   = "process"
        project_name = "project_name"
        process_name = "process_name"


class DocumentRole(int, enum.Enum):
    input  = 1
    output = 2


class DocumentProcess(SQLModel, table=True):
    # field name | type         | options
    project_name : str          = Field(default=None, primary_key=True, foreign_key=Project.Fields.project_name)
    process_name : str          = Field(default=None, primary_key=True, foreign_key=Process.Fields.process_name)
    document_name: str          = Field(default=None, primary_key=True, foreign_key=Document.Fields.document_name)
    document_role: DocumentRole = Field(sa_column=Column(Enum(DocumentRole)), nullable=False)

    # relationship name | type     | options
    document            : Document = Relationship(back_populates="documents_processes")
    process             : Process  = Relationship(back_populates="documents_processes")

    class Fields(metaclass=StringFields):
        table_name    = "documentprocess"
        project_name  = "project_name"
        process_name  = "process_name"
        document_name = "document_name"
        document_role = "document_role"


class PatchReturn(SQLModel):
    id           : int      | None
    # project_name : str      | None
    # document_name: str      | None
    user_name    : str      | None
    updated_date : datetime | None
    patch        : List[Dict] = []

    class Config:
        arbitrary_types_allowed = True


class DocumentReturn(SQLModel):
    project_name : str      | None
    document_name: str      | None
    author_name  : str      | None
    jsonschema   : Dict     | None
    first        : Dict     | None
    last         : Dict     | None
    creation_date: datetime | None
    patches      : List[PatchReturn] = []

    class Config:
        arbitrary_types_allowed = True

class ProjectReturn(SQLModel):
    project_name: str | None
    owner_name  : str | None
    documents: List[DocumentReturn] = []

class ProjectPermissionsInput(SQLModel):
    user_name: str
    permissions: List[ProjPermissions] = []

class DocumentPermissionsInput(SQLModel):
    user_name: str
    permissions: List[DocPermissions] = []
