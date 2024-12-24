from pydantic import BaseModel,Field
from typing import Dict
from factory_sdk.dto_old.state import FactoryState
from typing import Optional
from datetime import datetime
from factory_sdk.dto_old.revision import Revision
from typing import List,Dict


class NewDataset(BaseModel):
    name: str

class Shard(BaseModel):
    id: str
    num_samples: int
    fingerprint: str
    num_bytes: int

class Split(BaseModel):
    name: str
    num_samples: int
    features: Dict
    datasets_version: str
    fingerprint: str
    num_bytes: int
    shards: List[Shard]

class DatasetRevision(BaseModel):
    splits: List[str]
    fingerprint: str
    num_bytes: int
    version:str=Field(default="0.0.1")

class DatasetInfo(BaseModel):
    state: FactoryState=Field(default=FactoryState.INITIALIZED)
    name: str
    project: str
    fingerprints:Dict[str,str]=Field(default={})
    lastRevision: Optional[str]=Field(default=None)
    created_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str=Field(default_factory=lambda: datetime.now().isoformat())
    revisions:Dict[str,Revision]=Field(default={})