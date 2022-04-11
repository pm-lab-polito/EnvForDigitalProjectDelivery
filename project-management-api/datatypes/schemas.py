from typing import List, Dict

from pydantic import BaseModel, Extra


class ProcessSchema(BaseModel):
    inputs : List[str]
    outputs: List[str]

    class Config:
        extra = Extra.forbid


class PermissionSchema(BaseModel):
    documents: Dict

    class Config:
        extra = Extra.forbid


class ProjectCreateSchema(BaseModel):
    project_name: str
    documents   : Dict[str, Dict]
    processes   : List[ProcessSchema]
    permissions : Dict[str, PermissionSchema]

    class Config:
        extra = Extra.forbid
