from factory_sdk.datasets.hf import load as load_hf, fingerprint as fingerprint_hf
from tempfile import TemporaryDirectory
from datasets import load_from_disk, load_dataset
from tqdm_joblib import tqdm_joblib
from joblib import Parallel, delayed
from glob import glob
import os
from hashlib import md5
from uuid import uuid4
from typing import Optional
from factory_sdk.exceptions.api import *
from factory_sdk.dto.dataset import DatasetInitData, DatasetMeta, DatasetRevision, DatasetObject
from factory_sdk.dto.resource import FactoryRevisionState, FactoryMetaState
import json
from rich import print


class Datasets:
    def __init__(self, client):
        self.client = client

    def upload_dataset(self, factory_name, dataset_path, dataset: Optional[DatasetMeta], fingerprints={}, max_parallel_upload=8):
        if dataset is None:
            print("[green]🤖 Creating a new dataset in your factory instance...[/green]")
            dataset: DatasetMeta = self.client.post(
                f"datasets",
                DatasetInitData(name=factory_name),
                response_class=DatasetMeta
            )
        else:
            print("[cyan]🤖 Creating a new dataset revision in your factory instance...[/cyan]")

        revision: DatasetRevision = self.client.post(
            f"datasets/{factory_name}/revisions",
            {}, response_class=DatasetRevision
        )

        files = glob(f"{dataset_path}/**", recursive=True)
        files = [file for file in files if os.path.isfile(file)]
        file_paths = [os.path.relpath(file, dataset_path) for file in files]

        print("[green]📦 Uploading files...[/green]")
        with tqdm_joblib(total=len(files)):
            Parallel(n_jobs=max_parallel_upload)(
                delayed(self.client.put_file)(
                    f"datasets/{factory_name}/revisions/{revision.name}/files/{file_path}",
                    file
                )
                for file, file_path in zip(files, file_paths)
            )

        revision.state = FactoryRevisionState.PROCESSING
        revision.ext_fingerprints = fingerprints
        hasher = md5()
        buffer_size = 65536
        for file in sorted(files):
            with open(file, "rb") as f:
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    hasher.update(data)
        revision.fingerprint = hasher.hexdigest()

        self.client.put(
            f"datasets/{factory_name}/revisions/{revision.name}",
            revision
        )

        self.client.wait(
            f"datasets/{factory_name}/revisions/{revision.name}/wait/{FactoryRevisionState.READY.value}"
        )

        revision: DatasetRevision = self.client.get(
            f"datasets/{factory_name}/revisions/{revision.name}",
            response_class=DatasetRevision
        )
        dataset: DatasetMeta = self.client.get(
            f"datasets/{factory_name}",
            response_class=DatasetMeta
        )

        print("[bold green]🎉 Dataset uploaded to the Factory successfully![/bold green]")
        return dataset, revision

    def should_create_revision(self, hf_fingerprint: str, dataset: DatasetMeta, revision: DatasetRevision):
        if dataset is None:
            return True
        if revision is None:
            return True
        if revision.state == FactoryRevisionState.FAILED:
            return True
        if dataset.state != FactoryMetaState.READY:
            return True
        if "huggingface" not in revision.ext_fingerprints:
            return True
        if revision.ext_fingerprints["huggingface"] != hf_fingerprint:
            return True
        return False

    def from_huggingface(self, name, huggingface_name, huggingface_token=None, huggingface_config=None):

        hf_fingerprint = fingerprint_hf(huggingface_name, huggingface_token)

        try:
            dataset: DatasetMeta = self.client.get(
                f"datasets/{name}", response_class=DatasetMeta
            )
            if dataset.lastRevision is not None:
                revision: DatasetRevision = self.client.get(
                    f"datasets/{name}/revisions/{dataset.lastRevision}",
                    response_class=DatasetRevision
                )
            else:
                revision = None
        except NotFoundException:
            dataset = None
            revision = None

        if self.should_create_revision(hf_fingerprint, dataset, revision):
            with TemporaryDirectory() as tempdir:
                hf_fingerprint = load_hf(
                    huggingface_name,
                    huggingface_token,
                    huggingface_config,
                    tempdir
                )
                dataset, revision = self.upload_dataset(
                    name,
                    tempdir,
                    dataset,
                    fingerprints={"huggingface": hf_fingerprint},
                    max_parallel_upload=8
                )
        else:
            print("[bold yellow]✅ Current dataset revision matches the HuggingFace fingerprint. No new revision needed.[/bold yellow]")

        return DatasetObject(meta=dataset, revision=revision)
