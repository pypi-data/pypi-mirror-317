from factory_sdk.dto.resource import FactoryResourceInitData, FactoryResourceMeta, FactoryResourceRevision, FactoryResourceObject, FactoryRevisionRef
from typing import Dict,Any, Optional, List
from pydantic import BaseModel
from enum import Enum


class AdapterMeta(FactoryResourceMeta):
    pass

class AdapterInitData(FactoryResourceInitData):
    
    def create_meta(self,tenant_name,project_name)->AdapterMeta:
        return AdapterMeta(name=self.name,project=project_name,tenant=tenant_name)
    
class AutoTrainingParams(str, Enum):
    AUTO_LORA="auto_lora"
    AUTO_LORA_FAST="auto_lora_fast"
   
class AdapterRevision(FactoryResourceRevision):
    model: Optional[FactoryRevisionRef]=None
    dataset: Optional[FactoryRevisionRef]=None
    metrics: Optional[List[FactoryRevisionRef]]=None
    preprocessor: Optional[FactoryRevisionRef]=None
    train_params: Optional[AutoTrainingParams]=None
    
class DatasetMappingCallObject(BaseModel):
    callable:str
    

