"""
Module for the methods regarding the documents
"""

import copy
import operator
from functools import reduce

import jsonpatch
import jsonpath_ng.ext
from fastapi import APIRouter

from datatypes.models import *
from dependencies import *

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[]
)


@router.post("/",
             response_model=DocumentReturn,
             dependencies=[Depends(require_document_permission(Permissions.create))])
async def add_document_schema_to_project(request_body: Dict    = Depends(get_request_body),
                                         user        : User    = Depends(get_current_active_user),
                                         db_project  : Project = Depends(get_project),
                                         session     : Session = Depends(get_session)):
    """
    Add a document schema to a project
    Requires the authenticated user to have the permission to create a document

    :param request_body: schema to add
    :param user: current user from dependencies
    :param db_project: project of path from dependencies
    :param session: session from dependencies
    :return: the document added
    """

    document_name = list(request_body.keys())[0]
    document_body = request_body[document_name]

    if crud.get_document_of_project(session,
                                    db_project.project_name,
                                    document_name) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document already exists")

    if 'jsonschema' not in document_body.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing jsonschema of document")

    jsonschema = document_body['jsonschema']

    db_doc = Document(project_name=db_project.project_name,
                      document_name=document_name,
                      author_name=user.user_name,
                      jsonschema=jsonschema)

    if "computed_fields" in document_body.keys():
        computed_fields = document_body['computed_fields']

        for field_name, field_body in computed_fields.items():
            session.add(ComputedField(project_name            =db_project.project_name,
                                      field_document_name     =document_name,
                                      field_name              =field_name,
                                      reference_document_name =field_body['reference_document'],
                                      jsonpath                =field_body['jsonpath']))

    if "ms_computed_fields" in document_body.keys():
        ms_computed_fields = document_body['ms_computed_fields']

        for field_name, field_body in ms_computed_fields.items():
            computed_field = MSProjectComputedField(project_name        =db_project.project_name,
                                                    ms_project_name     =field_body['ms_project_name'],
                                                    field_document_name =document_name,
                                                    field_name          =field_name,
                                                    field_from          =field_body['field_from'],
                                                    jsonpath            =field_body['jsonpath'])
            jsonpath_expr = jsonpath_ng.ext.parse(computed_field.jsonpath)
            db_msproj = crud.get_ms_project(session, db_project.project_name, computed_field.ms_project_name)
            match field_body['field_from']:
                case MSProjectField.tasks.value:
                    computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_msproj.tasks)))
                case MSProjectField.resources.value:
                    computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_msproj.resources)))
                case MSProjectField.proj_info.value:
                    computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_msproj.proj_info)))
            session.add(computed_field)

    for permission in (DocPermissions.view, DocPermissions.edit, DocPermissions.delete):
        session.add(DocumentPermission(project_name=db_project.project_name, document_name=document_name,
                                       user_name=user.user_name, permission=permission))

    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)
    return db_doc


@router.put("/{document_name}",
            response_model=DocumentReturn,
            dependencies=[Depends(require_document_permission(Permissions.edit)),
                          Depends(check_document_process),
                          Depends(validate_document)])
async def put_document_to_project(document_body: Dict     = Depends(get_request_body),
                                  user         : User     = Depends(get_current_active_user),
                                  db_project   : Project  = Depends(get_project),
                                  db_doc       : Document = Depends(get_document),
                                  session      : Session  = Depends(get_session)):
    """
    Add or update content of document
    Requires the authenticated user to have the permission to edit the document

    :param document_body: document content to add or update
    :param user: current user from dependencies
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :param session: session from dependencies
    :return: the document
    """

    last = db_doc.last
    time = datetime.utcnow()
    db_doc.last = document_body
    db_doc.updated_date = time

    if not bool(db_doc.first):
        db_doc.first = document_body
        db_doc.creation_date = time
        db_doc.author_name = user.user_name
    else:
        patch = json.loads(jsonpatch.JsonPatch.from_diff(last, db_doc.last).to_string())
        diff = Patch(project_name=db_project.project_name, patch=patch, user_name=user.user_name)
        db_doc.patches.append(diff)

    for computed_field in db_doc.computed_fields_reference:
        jsonpath_expr = jsonpath_ng.ext.parse(computed_field.jsonpath)
        computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_doc.last)))

    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)

    db_doc.update_forward_refs()

    return db_doc


@router.patch("/{document_name}",
              response_model=DocumentReturn,
              dependencies=[Depends(require_document_permission(Permissions.edit)),
                            Depends(check_document_process),
                            Depends(validate_document)])
async def patch_document_of_project(document_body: Dict     = Depends(get_request_body),
                                    user         : User     = Depends(get_current_active_user),
                                    db_project   : Project  = Depends(get_project),
                                    db_doc       : Document = Depends(get_document),
                                    session      : Session  = Depends(get_session)):
    """
    Patch content of document
    Requires the authenticated user to have the permission to edit the document

    :param document_body: document content to patch
    :param user: current user from dependencies
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :param session: session from dependencies
    :return: the document
    """

    new_last = copy.deepcopy(db_doc.last)
    new_last.update(document_body)

    return await put_document_to_project(document_body=new_last,
                                         user=user,
                                         db_project=db_project,
                                         db_doc=db_doc,
                                         session=session)

@router.get("/{document_name}",
            response_model=DocumentReturn,
            dependencies=[Depends(get_current_active_user),
                          Depends(require_document_permission(Permissions.view))])
@router.get("/{document_name}/{field}/{path:path}",
            response_model=DocumentReturn,
            dependencies=[Depends(get_current_active_user),
                          Depends(require_document_permission(Permissions.view))])
def get_document_of_project(field : str | None = None,
                            path  : str | None = None,
                            db_doc: Document   = Depends(get_document)):
    """
    Get specified content in path of field of document
    Requires the authenticated user to have the permission to view the document

    :param field: field of document
    :param path: path in field
    :param db_doc: document of path from dependencies
    :return: content in path of field of document
    """

    if field is None:
        return db_doc

    element = getattr(db_doc, field)

    def find(el, json_doc):
        return reduce(operator.getitem, el.split('/'), json_doc)

    if path is not None and path != "":
        element = find(path, element)

    return element


@router.post("/{document_name}/last/{path:path}",
            response_model=DocumentReturn,
            dependencies=[Depends(require_document_permission(Permissions.edit))])
async def post_path_document_of_project(path         : str | None = None,
                                        session      : Session    = Depends(get_session),
                                        user         : User       = Depends(get_current_active_user),
                                        document_body: Dict       = Depends(get_request_body),
                                        db_project   : Project    = Depends(get_project),
                                        db_doc       : Document   = Depends(get_document)):
    """
    Post content in path of document content
    Requires the authenticated user to have the permission to edit the document

    :param path: path in document content
    :param session: session from dependencies
    :param user: current user from dependencies
    :param document_body: document content to post
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :return: the document
    """

    last_el = path.split('/')[-1]

    last = copy.deepcopy(db_doc.last)

    def get_item(obj, item: str):
        if type(obj) is dict:
            return obj[item]
        elif type(obj) is list and item.isdigit() and int(item) < len(obj):
            return obj[int(item)]
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    element = reduce(get_item, path.split('/')[:-1], last)

    if type(element) is dict:
        if last_el in element.keys():
            if type(element[last_el]) is list:
                element[last_el].append(document_body)
            else:
                element[last_el] = document_body
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    elif type(element) is list:
        if type(element[int(last_el)]) is list:
            element[int(last_el)].append(document_body)
        else:
            element[last_el] = document_body
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        validate(last, db_doc.jsonschema)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await put_document_to_project(last, user, db_project, db_doc, session)


@router.delete("/{document_name}",
               status_code=status.HTTP_200_OK,
               dependencies=[Depends(get_current_active_user),
                             Depends(require_document_permission(Permissions.delete))])
def delete_document_of_project(db_doc : Document = Depends(get_document),
                               session: Session  = Depends(get_session)):
    """
    Delete document of project
    Requires the authenticated user to have the permission to delete the document

    :param db_doc:
    :param session:
    :return: 200 OK if document is deleted, else the corresponding error
    """
    session.delete(db_doc)
    session.commit()


@router.post("/{document_name}/permissions",
             response_model=DocumentPermissionsInput,
             dependencies=[Depends(require_document_permission(Permissions.edit_permissions))])
def add_document_permissions(doc_permissions: DocumentPermissionsInput,
                             db_project : Project  = Depends(get_project),
                             db_doc     : Document = Depends(get_document),
                             session    : Session  = Depends(get_session)):
    """
    Add user permissions to document
    Requires the authenticated user to have the permission to edit the document permissions

    :param doc_permissions: permissions to add
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :param session: session from dependencies
    :return: current user permissions of the document
    """

    if crud.get_user(session, doc_permissions.user_name) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for perm in doc_permissions.permissions:
        if crud.get_document_permission(session=session,
                                        user_name=doc_permissions.user_name,
                                        project_name=db_project.project_name,
                                        document_name=db_doc.document_name,
                                        permission=perm) is None:
            session.add(DocumentPermission(user_name=doc_permissions.user_name,
                                           project_name=db_project.project_name,
                                           document_name=db_doc.document_name,
                                           permission=perm))
    session.commit()

    perm_list = list(map(lambda item: item.permission,
                         crud.get_document_permissions(session,
                                                       doc_permissions.user_name,
                                                       db_project.project_name,
                                                       db_doc.document_name)))
    return DocumentPermissionsInput(user_name=doc_permissions.user_name, permissions=perm_list)


@router.delete("/{document_name}/permissions",
               response_model=DocumentPermissionsInput,
               dependencies=[Depends(require_document_permission(Permissions.edit_permissions))])
def delete_document_permissions(doc_permissions: DocumentPermissionsInput,
                                db_project : Project  = Depends(get_project),
                                db_doc     : Document = Depends(get_document),
                                session    : Session  = Depends(get_session)):
    """
    Deletes user permissions of document
    Requires the authenticated user to have the permission to edit the document permissions

    :param doc_permissions: permissions to delete
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :param session: session from dependencies
    :return: current user permissions of the document
    """

    if crud.get_user(session, doc_permissions.user_name) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for perm in doc_permissions.permissions:
        p = crud.get_document_permission(session=session,
                                         user_name=doc_permissions.user_name,
                                         project_name=db_project.project_name,
                                         document_name=db_doc.document_name,
                                         permission=perm)
        if p is not None:
            session.delete(p)
    session.commit()

    perm_list = list(map(lambda item: item.permission,
                         crud.get_document_permissions(session,
                                                       doc_permissions.user_name,
                                                       db_project.project_name,
                                                       db_doc.document_name)))
    return DocumentPermissionsInput(user_name=doc_permissions.user_name, permissions=perm_list)


@router.get("/{document_name}/permissions/{user_name}",
            response_model=DocumentPermissionsInput,
            dependencies=[Depends(require_document_permission(Permissions.edit_permissions))])
def get_document_permissions_for_user(user_name : str,
                                      db_project: Project  = Depends(get_project),
                                      db_doc    : Document = Depends(get_document),
                                      session   : Session  = Depends(get_session)):
    """
    Gets user permissions of document
    Requires the authenticated user to have the permission to edit the document permissions

    :param user_name: user name of permissions to get
    :param db_project: project of path from dependencies
    :param db_doc: document of path from dependencies
    :param session: session from dependencies
    :return: current user permissions of the document
    """
    perm_list = list(map(lambda item: item.permission,
                         crud.get_document_permissions(session,
                                                       user_name,
                                                       db_project.project_name,
                                                       db_doc.document_name)))
    return DocumentPermissionsInput(user_name=user_name, permissions=perm_list)
