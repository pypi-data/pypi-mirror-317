from pydantic import BaseModel, Field
from uuid import uuid4
from factory_sdk.dto.user import TenantMember
from typing import List
from enum import Enum

class TenantType(str, Enum):
    USER="user"
    TEAM="team"

class Tenant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    members: List[TenantMember] = Field(min_length=1)
    type: TenantType = Field(default=TenantType.USER)