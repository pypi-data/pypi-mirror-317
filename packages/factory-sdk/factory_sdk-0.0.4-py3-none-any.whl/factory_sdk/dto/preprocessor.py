from factory_sdk.dto.resource import FactoryResourceInitData, FactoryResourceMeta, FactoryResourceRevision, FactoryResourceObject
from typing import Dict,Any, Optional
from pydantic import BaseModel

class PreprocessorMeta(FactoryResourceMeta):
    pass

class PreprocessorInitData(FactoryResourceInitData):
    def create_meta(self,tenant_name,project_name)->PreprocessorMeta:
        return PreprocessorMeta(name=self.name,project=project_name,tenant=tenant_name)

class PreprocessorRevision(FactoryResourceRevision):
    pass


class PreprocessorObject(BaseModel):
    meta: PreprocessorMeta
    revision: PreprocessorRevision
    
class PreprocessorCallObject(BaseModel):
    callable:str

