from pydantic import BaseModel,Field
from typing import Dict,List, Optional
from factory_sdk.dto_old.state import FactoryState
from enum import Enum
from datetime import datetime
from factory_sdk.dto_old.revision import Revision
from typing import Dict,List, Optional

class NewModel(BaseModel):
    name: str

class TextModels(str,Enum):
    Qwen_v2_5_0_5B_Instruct="Qwen/Qwen2.5-0.5B-Instruct"

class VisionTextModels(str,Enum):
    Phi_3_5_Vision_Instruct="microsoft/Phi-3.5-vision-instruct"

class ModelInfo(BaseModel):
    state: FactoryState=Field(default=FactoryState.INITIALIZED)
    name: str
    project: str
    fingerprints:Dict[str,str]=Field(default={})
    lastRevision: Optional[str]=Field(default=None)
    created_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    revisions:Dict[str,Revision]=Field(default={})


class TensorInfo(BaseModel):
    name: str
    num_params: int
    shape: List[int]
    dtype: str
    snr: Optional[float]

class ModelRevision(BaseModel):
    fingerprint:str
    version:str=Field(default="0.0.1")
    params:Dict[str,TensorInfo]