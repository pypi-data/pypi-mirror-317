from factory_sdk.dto.model import ModelMeta, ModelRevision, ModelObject
from factory_sdk.dto.dataset import DatasetMeta, DatasetRevision, DatasetObject
from factory_sdk.dto.metric import MetricMeta, MetricRevision, MetricObject
from factory_sdk.dto.preprocessor import PreprocessorMeta, PreprocessorRevision, PreprocessorObject
from factory_sdk.dto.resource import FactoryRevisionRef
from typing import List
from factory_sdk.dto.task import TrainingTask
from factory_sdk.dto.adapter import AutoTrainingParams
from factory_sdk.utils.inspect import get_cleaned_module_source, hash_code_by_ast
from factory_sdk.exceptions.api import NotFoundException
from factory_sdk.dto.adapter import AdapterMeta,AdapterInitData,AdapterRevision
from rich import print
from typing import Optional
from factory_sdk.dto.resource import FactoryMetaState, FactoryRevisionState
from hashlib import md5


class Adapters:
    def __init__(self, client):
        self.client = client

    def should_create_revision(self, fingerprint:str, adapter: Optional[AdapterMeta], revision: Optional[AdapterRevision]):
        if adapter is None:
            return True
        if revision is None:
            return True
        if revision.state == FactoryRevisionState.FAILED:
            return True
        if adapter.state not in  [FactoryMetaState.FAILED, FactoryMetaState.INITIALIZED]:
            return True
        if revision.fingerprint != fingerprint:
            return True
        return False

    def init(self,name:str,model:ModelObject, metrics:List[MetricObject],dataset:DatasetObject,preprocessor:PreprocessorObject,params:AutoTrainingParams):
        
        #check if the adapter is already registered
        try:
            meta=self.client.get(
                f"adapters/{name}",
                response_class=AdapterMeta  
            )
        except NotFoundException:
            meta=None

        if meta is None:
            print("[green]🤖 Creating a new adapter in your factory instance...[/green]")

            init_data=AdapterInitData(
                name=name
            )

            meta:AdapterMeta=self.client.post(
                f"adapters",
                init_data,
                response_class=AdapterMeta
            )

        revision=None

        if meta.lastRevision is not None:
            revision=self.client.get(
                f"adapters/{name}/revisions/{meta.lastRevision}",
                response_class=AdapterRevision
            )

        params_fp=md5(params.value.encode()).hexdigest()
        fingerprint_base=f"dataset:{dataset.revision.fingerprint},model:{model.revision.fingerprint},preprocessor:{preprocessor.revision.fingerprint},train_params:{params_fp}"
        fingerprint=md5(fingerprint_base.encode()).hexdigest()

        if self.should_create_revision(fingerprint,meta,revision):
            print("[green]🤖 Creating a new revision in your factory instance...[/green]")

            revision:AdapterRevision=self.client.post(
                f"adapters/{name}/revisions",
                {},
                response_class=AdapterRevision
            )

            revision.model=FactoryRevisionRef(
                object_name=model.meta.name,
                revision_name=model.revision.name
            )

            revision.dataset=FactoryRevisionRef(
                object_name=dataset.meta.name,
                revision_name=dataset.revision.name
            )

            revision.metrics=[FactoryRevisionRef(
                object_name=metric.meta.name,
                revision_name=metric.revision.name
            ) for metric in metrics]

            revision.preprocessor=FactoryRevisionRef(
                object_name=preprocessor.meta.name,
                revision_name=preprocessor.revision.name
            )

            revision.train_params=params

            revision.fingerprint=fingerprint
            revision.state=FactoryRevisionState.PROCESSING

            revision:AdapterRevision=self.client.put(
                f"adapters/{name}/revisions/{revision.name}",
                revision,
                response_class=AdapterRevision
            )

            #wait
            self.client.wait(
                f"adapters/{name}/revisions/{revision.name}/wait/{FactoryRevisionState.READY_FOR_TRAINING.value}"
            )

            revision:AdapterRevision=self.client.get(
                f"adapters/{name}/revisions/{revision.name}",
                response_class=AdapterRevision
            )

            meta:AdapterMeta=self.client.get(
                f"adapters/{name}",
                response_class=AdapterMeta
            )



        



        



