from datetime import datetime
from typing import List

from flou.api.schemas import BaseModel
from pydantic import Field


class LTM(BaseModel):
    id: int
    name: str
    fqn: str
    snapshots_count: int
    created_at: datetime
    updated_at: datetime

class LTMId(BaseModel):
    id: int = Field(..., description="The LTM instance id")


class LTMCreation(BaseModel):
    fqn: str = Field(..., description="Fully qualified name of the LTM class")
    payload: dict = Field({}, description="Initial payload as a json object")
    playground: bool = Field(
        False, description="If true, the LTM will be created in the playground"
    )


class Transition(BaseModel):
    transition: str = Field(..., description="The label of the transition to perform")
    namespace: str = Field(..., description="The namespace of the transition")
    params: list[dict] | None = Field(
        None, description="If a parameterized transition, it's parameters"
    )
    payload: dict | None = Field(
        None, description="Optional payload for the transition"
    )
    wait_until_transition: str | None = Field(
        None,
        description="Await return until this transition `namespace:label` executes",
    )


class Rollback(BaseModel):
    index: int = Field(..., description="The index of the desired snapshot")
    replay: bool = Field(False, description="If true, replay the snapshot")

class RollbackIndex(BaseModel):
    index: int = Field(..., description="The index of the desired rollback")


class ErrorList(BaseModel):
    ids: List[str] = Field(..., description="The errors UUIDs to retry")
