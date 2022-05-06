"""
Module for the methods regarding ms projects
"""

import copy
import operator
from functools import reduce

import jpype
import mpxj
import jsonpatch
import jsonpath_ng.ext
from fastapi import APIRouter, File, UploadFile

from datatypes.models import *
from dependencies import *

router = APIRouter(
    prefix="/msprojects",
    tags=["msprojects"],
    dependencies=[]
)


@router.post("/",
             dependencies=[Depends(require_project_permission(Permissions.edit))])
async def add_ms_file_to_project(file: UploadFile = File(...),
                                 user: User = Depends(get_current_active_user),
                                 db_project: Project = Depends(get_project),
                                 session: Session = Depends(get_session)):
    """
    Add a ms file to a project
    :param request_body: request body
    :param file: ms file to upload
    :param user: current authenticated user
    :param db_project: project to add the file to
    :param session: session to use
    :return: uploaded ms project
    """

    if not file.filename.endswith(".mpp"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a ms project")

    file_name = file.filename.split(".")[0]
    content = await file.read()

    jpype.startJVM()
    from net.sf.mpxj.reader import UniversalProjectReader
    project = UniversalProjectReader().read(jpype.java.io.ByteArrayInputStream(content))

    tasks = []

    for task in project.getTasks():
        db_task = dict()
        db_task["name"] = str(task.getName().toString())
        db_task["level"] = task.getOutlineLevel()
        db_task["duration"] = str(task.getDuration().toString())
        db_task["predecessors"] = list()
        db_task["id"] = str(task.getID().toString())
        for rel in task.getPredecessors():
            db_pred = dict()
            db_pred["target_task"] = str(rel.getTargetTask().getName().toString())
            db_pred["lag"] = str(rel.getLag().toString())
            db_pred["type"] = str(rel.getType().toString())
            db_task["predecessors"].append(db_pred)

        tasks.append(db_task)

    resources = []

    for res in project.getResources():
        if res.getName() is not None and res.getName() != "":
            db_res = dict()
            db_res["name"] = str(res.getName().toString())
            db_res["id"] = str(res.getID().toString())
            resources.append(db_res)

    tmp = crud.get_ms_project(session, db_project.project_name, file_name)

    if tmp is not None:
        db_msproj = tmp
    else:
        db_msproj = MSProject(project_name=db_project.project_name,
                              ms_project_name=file_name,
                              author_name=user.user_name)

    db_msproj.update_author_name = user.user_name
    db_msproj.tasks = tasks
    db_msproj.resources = resources

    session.add(db_msproj)
    session.commit()
    session.refresh(db_msproj)

    for computed_field in db_msproj.computed_fields_reference:
        jsonpath_expr = jsonpath_ng.ext.parse(computed_field.jsonpath)
        match computed_field.field_from:
            case MSProjectField.tasks:
                computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_msproj.tasks)))
            case MSProjectField.resources:
                computed_field.field_value = list(map(lambda a: a.value, jsonpath_expr.find(db_msproj.resources)))
        session.add(computed_field)

    session.add(db_msproj)
    session.commit()
    session.refresh(db_msproj)

    jpype.shutdownJVM()

    return db_msproj


@router.get("/{ms_project_name}",
             dependencies=[Depends(require_project_permission(Permissions.view))])
async def get_ms_file_of_project(db_ms_project: MSProject = Depends(get_ms_project)):
    """
    Get ms file of a project
    :param db_ms_project: ms project from dependencies
    :return: ms project if found, 404 otherwise
    """
    return db_ms_project


@router.delete("/{ms_project_name}",
             dependencies=[Depends(require_project_permission(Permissions.edit))])
async def delete_ms_file_of_project(db_ms_project: MSProject = Depends(get_ms_project),
                                    session: Session = Depends(get_session)):
    """
    Delete ms file of a project
    :param db_ms_project: ms project from dependencies
    :param session: session from dependencies
    :return: 200 ok if deleted, 404 if not found
    """
    session.delete(db_ms_project)
    session.commit()
    raise HTTPException(status_code=200, detail="OK")
