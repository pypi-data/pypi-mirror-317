import typing as t
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class V1DagNodeType(str, Enum):
    MODEL = "model"
    AUDIT = "audit"


class V1DagNode(BaseModel):
    name: str
    model_name: str
    tags: t.List[str]
    parent_names: t.List[str]
    type: V1DagNodeType
    link: HttpUrl


class V1Dag(BaseModel):
    environment: str
    start_at: datetime
    schedule_seconds: int
    schedule_cron: str
    nodes: t.List[V1DagNode]
    link: HttpUrl
