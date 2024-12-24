from factory_sdk.dto.resource import FactoryResourceInitData, FactoryResourceMeta, FactoryResourceRevision, FactoryResourceObject
from typing import List, Dict
from pydantic import BaseModel


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

class DatasetMeta(FactoryResourceMeta):
    pass

class DatasetInitData(FactoryResourceInitData):
    def create_meta(self,tenant_name,project_name)->DatasetMeta:
        return DatasetMeta(name=self.name,project=project_name,tenant=tenant_name)

class DatasetRevision(FactoryResourceRevision):
    num_bytes: int=0
    splits: List[str]=[]

class DatasetObject(BaseModel):
    meta: DatasetMeta
    revision: DatasetRevision