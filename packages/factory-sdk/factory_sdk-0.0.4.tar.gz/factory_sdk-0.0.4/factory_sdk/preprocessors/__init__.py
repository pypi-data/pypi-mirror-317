from factory_sdk.utils.inspect import get_cleaned_module_source, hash_code_by_ast
import json
from hashlib import md5
from factory_sdk.dto.preprocessor import (
    PreprocessorMeta, 
    PreprocessorRevision, 
    PreprocessorInitData,
    PreprocessorCallObject,
    PreprocessorObject
)
from factory_sdk.exceptions.api import NotFoundException
from typing import Optional
from factory_sdk.dto.resource import FactoryMetaState, FactoryRevisionState
from rich import print
from tempfile import TemporaryDirectory
from glob import glob
from joblib import Parallel, delayed
import os
from tqdm_joblib import tqdm_joblib


class Preprocessors:
    def __init__(self, client):
        self.client = client

    def should_create_revision(self, fingerprint: str, model: Optional[PreprocessorMeta], revision: Optional[PreprocessorRevision]):
        # Determine if a new revision should be created based on model and revision states
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

    def from_code(self, name, ref, max_parallel_upload=8):
        # Extract code and compute fingerprint
        path, fn_name, code__src = get_cleaned_module_source(ref)
        fingerprint = hash_code_by_ast(code__src)

        # Try to fetch the preprocessor
        try:
            preprocessor = self.client.get(
                f"preprocessors/{name}",
                response_class=PreprocessorMeta
            )
        except NotFoundException:
            preprocessor = None

        # If it doesn't exist, create a new preprocessor
        if preprocessor is None:
            print("[green]🤖 Creating a new preprocessor in your factory instance...[/green]")
            preprocessor: PreprocessorMeta = self.client.post(
                "preprocessors",
                PreprocessorInitData(name=name),
                response_class=PreprocessorMeta
            )

        # Get the last revision if available
        revision = None
        if preprocessor.lastRevision is not None:
            revision = self.client.get(
                f"preprocessors/{name}/revisions/{preprocessor.lastRevision}",
                response_class=PreprocessorRevision
            )

        # Determine if we need to create a new revision
        if self.should_create_revision(fingerprint, preprocessor, revision):
            print("[cyan]🤖 Creating a new preprocessor revision in your factory instance...[/cyan]")
            revision: PreprocessorRevision = self.client.post(
                f"preprocessors/{name}/revisions",
                {},
                response_class=PreprocessorRevision
            )

            # Create a temporary directory to store code and params
            with TemporaryDirectory() as dir:
                # Write the source code
                with open(f"{dir}/code.py", "w") as f:
                    f.write(code__src)
                
                # Write the call parameters (assuming we need to specify the callable)
                with open(f"{dir}/params.json", "w") as f:
                    f.write(PreprocessorCallObject(callable=fn_name).model_dump_json(indent=4))

                # Gather files for upload
                files = glob(f"{dir}/**", recursive=True)
                files = [file for file in files if os.path.isfile(file)]
                file_paths = [os.path.relpath(file, dir) for file in files]

                print("[green]📦 Uploading files...[/green]")
                # Use parallel uploads for efficiency
                with tqdm_joblib(total=len(files)):
                    Parallel(n_jobs=max_parallel_upload)(
                        delayed(self.client.put_file)(
                            f"preprocessors/{name}/revisions/{revision.name}/files/{file_path}",
                            file
                        )
                        for file, file_path in zip(files, file_paths)
                    )

                # Update the revision state and fingerprint
                revision.state = FactoryRevisionState.PROCESSING
                revision.fingerprint = fingerprint
                self.client.put(
                    f"preprocessors/{name}/revisions/{revision.name}",
                    revision
                )

                # Wait for the revision to be ready
                self.client.wait(
                    f"preprocessors/{name}/revisions/{revision.name}/wait/{FactoryRevisionState.READY.value}"
                )

                # Refresh the revision and preprocessor metadata
                revision: PreprocessorRevision = self.client.get(
                    f"preprocessors/{name}/revisions/{revision.name}",
                    response_class=PreprocessorRevision
                )
                preprocessor: PreprocessorMeta = self.client.get(
                    f"preprocessors/{name}",
                    response_class=PreprocessorMeta
                )

        # Return an object that encapsulates the meta and revision
        return PreprocessorObject(meta=preprocessor, revision=revision)
