from factory_sdk.utils.inspect import get_cleaned_module_source, hash_code_by_ast
import json
from hashlib import md5
from factory_sdk.dto.metric import MetricMeta, MetricRevision, MetricInitData, MetricCallObject, MetricObject
from factory_sdk.exceptions.api import NotFoundException
from typing import Optional
from factory_sdk.dto.resource import FactoryMetaState, FactoryRevisionState
from rich import print
from tempfile import TemporaryDirectory
from glob import glob
from joblib import Parallel, delayed
import os
from tqdm_joblib import tqdm_joblib




class Metrics:
    def __init__(self, client):
        self.client = client

    def should_create_revision(self, fingerprint:str, model: Optional[MetricMeta], revision: Optional[MetricRevision]):
        if model is None:
            return True
        if revision is None:
            return True
        if revision.state == FactoryRevisionState.FAILED:
            return True
        if model.state != FactoryMetaState.READY:
            return True
        if revision.fingerprint != fingerprint:
            return True
        return False

    def from_code(self, name, ref,max_parallel_upload=8):
        path,fn_name,code__src=get_cleaned_module_source(ref)
        fingerprint=hash_code_by_ast(code__src)

        ##get metric from factory
        try:
            metric=self.client.get(
                f"metrics/{name}",
                response_class=MetricMeta
            )
        except NotFoundException:
            metric=None

        if metric is None:
            print("[green]🤖 Creating a new metric in your factory instance...[/green]")
            metric:MetricMeta=self.client.post(
                f"metrics",
                MetricInitData(name=name),
                response_class=MetricMeta
            )

        
        revision=None
        if metric.lastRevision is not None:
            revision=self.client.get(
                f"metrics/{name}/revisions/{metric.lastRevision}",
                response_class=MetricRevision
            )

        if self.should_create_revision(fingerprint,metric,revision):
            print("[cyan]🤖 Creating a new metric revision in your factory instance...[/cyan]")
            revision:MetricRevision=self.client.post(
                f"metrics/{name}/revisions",
                {},
                response_class=MetricRevision
            )
            with TemporaryDirectory() as dir:
                with open(f"{dir}/code.py","w") as f:
                    f.write(code__src)
                with open(f"{dir}/params.json","w") as f:
                    f.write(MetricCallObject(callable=fn_name).model_dump_json(indent=4))

                files = glob(f"{dir}/**", recursive=True)
                files = [file for file in files if os.path.isfile(file)]
                file_paths = [os.path.relpath(file, dir) for file in files]

                print("[green]📦 Uploading files...[/green]")
                with tqdm_joblib(total=len(files)):
                    Parallel(n_jobs=max_parallel_upload)(
                        delayed(self.client.put_file)(
                            f"metrics/{name}/revisions/{revision.name}/files/{file_path}",
                            file
                        )
                        for file, file_path in zip(files, file_paths)
                    )

                revision.state = FactoryRevisionState.PROCESSING
                revision.fingerprint = fingerprint
                self.client.put(
                    f"metrics/{name}/revisions/{revision.name}",
                    revision
                )

                self.client.wait(
                    f"metrics/{name}/revisions/{revision.name}/wait/{FactoryRevisionState.READY.value}"
                )

                revision:MetricRevision=self.client.get(
                    f"metrics/{name}/revisions/{revision.name}",
                    response_class=MetricRevision
                )
                metric:MetricMeta=self.client.get(
                    f"metrics/{name}",
                    response_class=MetricMeta
                )

        return MetricObject(meta=metric,revision=revision)
                
       