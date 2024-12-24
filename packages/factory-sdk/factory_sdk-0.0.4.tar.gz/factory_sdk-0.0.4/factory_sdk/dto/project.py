from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from uuid import uuid4


class NewProject(BaseModel):
    name: str

class Project(BaseModel):
    id: str=Field(default_factory=lambda: str(uuid4()))
    name: str
    tenant: str
    created_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    