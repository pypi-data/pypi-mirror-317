from factory_sdk.models.hf import load as load_hf, fingerprint as fingerprint_hf
from tempfile import TemporaryDirectory
from joblib import Parallel, delayed
from tqdm_joblib import tqdm_joblib
from glob import glob
import os
from hashlib import md5
from typing import Optional, Dict
from factory_sdk.exceptions.api import NotFoundException
from factory_sdk.dto.model import ModelInitData, ModelMeta, ModelRevision, ModelObject
from factory_sdk.dto.resource import FactoryRevisionState, FactoryMetaState
from rich import print
from factory_sdk.dto.model import SupportedModels

class Models:
    def __init__(self, client):
        self.client = client

    def upload_model(
        self,
        factory_name: str,
        model_path: str,
        model: Optional[ModelMeta] = None,
        fingerprints: Dict[str, str] = {},
        max_parallel_upload: int = 8
    ):
        # If the model does not exist, create it
        if model is None:
            print("[green]🤖 Creating a new model in your factory instance...[/green]")
            model: ModelMeta = self.client.post(
                "models",
                ModelInitData(name=factory_name),
                response_class=ModelMeta
            )
        else:
            print("[cyan]🤖 Creating a new model revision in your factory instance...[/cyan]")

        # Create a new revision
        revision: ModelRevision = self.client.post(
            f"models/{factory_name}/revisions",
            {},
            response_class=ModelRevision
        )

        # Upload files
        files = glob(f"{model_path}/**", recursive=True)
        files = [file for file in files if os.path.isfile(file)]
        file_paths = [os.path.relpath(file, model_path) for file in files]

        print("[green]📦 Uploading files...[/green]")
        with tqdm_joblib(total=len(files)):
            Parallel(n_jobs=max_parallel_upload)(
                delayed(self.client.put_file)(
                    f"models/{factory_name}/revisions/{revision.name}/files/{file_path}",
                    file
                )
                for file, file_path in zip(files, file_paths)
            )

        # Update revision state and fingerprints
        revision.state = FactoryRevisionState.PROCESSING
        revision.ext_fingerprints = fingerprints

        # Compute a simple fingerprint (MD5) for all files as a convenience
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

        # PUT the updated revision
        self.client.put(
            f"models/{factory_name}/revisions/{revision.name}",
            revision
        )

        # Wait for revision to be ready
        self.client.wait(
            f"models/{factory_name}/revisions/{revision.name}/wait/{FactoryRevisionState.READY.value}"
        )

        # Get the updated revision and model
        revision: ModelRevision = self.client.get(
            f"models/{factory_name}/revisions/{revision.name}",
            response_class=ModelRevision
        )
        model: ModelMeta = self.client.get(
            f"models/{factory_name}",
            response_class=ModelMeta
        )

        print("[bold green]🎉 Model uploaded to the Factory successfully![/bold green]")
        return model, revision

    def should_create_revision(self, hf_fingerprint: str, model: Optional[ModelMeta], revision: Optional[ModelRevision]):
        if model is None:
            return True
        if revision is None:
            return True
        if revision.state == FactoryRevisionState.FAILED:
            return True
        if model.state != FactoryMetaState.READY:
            return True
        if "huggingface" not in revision.ext_fingerprints:
            return True
        if revision.ext_fingerprints["huggingface"] != hf_fingerprint:
            return True
        return False

    def from_huggingface(
        self,
        name: str,
        base_model:SupportedModels,
        huggingface_token: Optional[str] = None,
        max_parallel_upload: int = 8
    ):

        hf_fingerprint = fingerprint_hf(base_model.value, huggingface_token)

        try:
            model: ModelMeta = self.client.get(
                f"models/{name}",
                response_class=ModelMeta
            )
            if model.lastRevision is not None:
                revision: ModelRevision = self.client.get(
                    f"models/{name}/revisions/{model.lastRevision}",
                    response_class=ModelRevision
                )
            else:
                revision = None
        except NotFoundException:
            model = None
            revision = None

        if self.should_create_revision(hf_fingerprint, model, revision):
            print("[green]🤖 Downloading model from Hugging Face...[/green]")
            with TemporaryDirectory() as tempdir:
                new_hf_fingerprint = load_hf(
                    base_model.value,
                    huggingface_token,
                    tempdir
                )
                print(f"🤖 Downloaded model {base_model.value}")
                model, revision = self.upload_model(
                    factory_name=name,
                    model_path=tempdir,
                    model=model,
                    fingerprints={"huggingface": new_hf_fingerprint},
                    max_parallel_upload=max_parallel_upload
                )

            # Wait for the model meta to be READY
            self.client.wait(
                f"models/{name}/wait/{FactoryMetaState.READY.value}"
            )
            print(f"[bold green]🎉 Model {name} uploaded and is READY in Factory![/bold green]")
        else:
            print("[bold yellow]✅ Current model revision matches the HuggingFace fingerprint. No new revision needed.[/bold yellow]")

        # Retrieve the updated model and revision to return them
        model: ModelMeta = self.client.get(
            f"models/{name}",
            response_class=ModelMeta
        )
        if model.lastRevision:
            revision: ModelRevision = self.client.get(
                f"models/{name}/revisions/{model.lastRevision}",
                response_class=ModelRevision
            )
        else:
            revision = None

        return ModelObject(meta=model,revision=revision)
