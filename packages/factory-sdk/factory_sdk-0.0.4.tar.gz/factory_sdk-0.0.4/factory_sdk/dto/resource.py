from pydantic import BaseModel,Field
from enum import Enum
from uuid import uuid4
from datetime import datetime,timezone
from typing import Optional, Dict, List
from abc import ABC,abstractmethod

class FactoryMetaState(str,Enum):
    INITIALIZED="initialized"
    READY="ready"
    READY_FOR_TRAINING="ready_for_training"
    FAILED="failed"

class FactoryRevisionState(str,Enum):
    INITIALIZED="initialized"
    PROCESSING="processing"
    READY_FOR_TRAINING="ready_for_training"
    READY="ready"
    FAILED="failed"

class FactoryResourceObject(BaseModel):
    id: str=Field(default_factory=lambda: str(uuid4()))
    name: str
    project: str
    tenant: str
    created_at: str=Field(default_factory=lambda: datetime.now(
        timezone.utc).isoformat())
    updated_at: str=Field(default_factory=lambda: datetime.now(
        timezone.utc).isoformat())
    
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc).isoformat()

class FactoryResourceMeta(FactoryResourceObject):
    state: FactoryMetaState=Field(default=FactoryMetaState.INITIALIZED)
    lastRevision: Optional[str]=Field(default=None)

class FactoryResourceInitData(BaseModel):
    name: str

    @abstractmethod
    def create_meta(self,tenant_name:str,project_name:str)->FactoryResourceMeta:
        raise NotImplementedError()

class FactoryResourceRevision(FactoryResourceObject):
    state: FactoryRevisionState=Field(default=FactoryRevisionState.INITIALIZED)
    fingerprint: Optional[str]=Field(default=None)
    ext_fingerprints: Dict[str,str]=Field(default={})
    error_message: Optional[str]=Field(default=None)
    

class FactoryRevisionRef(BaseModel):
    object_name: str
    revision_name: str