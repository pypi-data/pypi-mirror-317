from huggingface_hub import HfApi
#from factory_sdk.logging import logger  # Removed logging as requested
from joblib import Parallel, delayed
from tqdm_joblib import tqdm_joblib
from datasets import load_dataset, Dataset, DatasetDict
from factory_sdk.datasets.arrow import create_pyarrow_table, batch_encode_samples, estimate_sample_size, save_shard
import os
from tqdm.auto import tqdm
from factory_sdk.dto.dataset import Shard, Split, DatasetRevision
from factory_sdk.datasets.fingerprint import compute_file_hash, merge_fingerprints
from datasets import __version__ as datasets_version
import json
from rich import print
from rich.progress import track


def hf_to_factory_dataset(dataset_dict, dir, target_shard_size=500*1024*1024, max_samples_per_shard=100_000):
    splits = []
    for k in dataset_dict:
        os.makedirs(os.path.join(dir, k, "data"), exist_ok=True)
        estimated_bytes_per_sample = estimate_sample_size(dataset_dict[k])

        samples_per_shard = max(1, target_shard_size // estimated_bytes_per_sample)
        samples_per_shard = min(samples_per_shard, max_samples_per_shard)

        shards = []
        steps = list(range(0, len(dataset_dict[k]), samples_per_shard))

        for ix, i in enumerate(steps):
            file = os.path.join(dir, k, "data", f"{ix}.parquet")
            current_shard_number = ix + 1
            total_shards = len(steps)
            num_samples = save_shard(
                dataset_dict[k],
                dataset_dict[k].features,
                i,
                i + samples_per_shard,
                file,
                pbar_text=f"Saving shard {current_shard_number}/{total_shards}"
            )

            fingerprint = compute_file_hash(file)
            num_bytes = os.path.getsize(file)
            shards.append(
                Shard(
                    id=f"{ix}.parquet",
                    num_samples=num_samples,
                    fingerprint=fingerprint,
                    num_bytes=num_bytes
                )
            )

        fingerprint = merge_fingerprints([shard.fingerprint for shard in shards])
        num_bytes = sum([shard.num_bytes for shard in shards])

        split = Split(
            name=k,
            num_samples=len(dataset_dict[k]),
            features=dataset_dict[k].features.to_dict(),
            datasets_version=datasets_version,
            fingerprint=fingerprint,
            num_bytes=num_bytes,
            shards=shards
        )

        meta_file = os.path.join(dir, k, "meta.json")
        with open(meta_file, "w") as f:
            json.dump(split.model_dump(), f, indent=2)

        splits.append(split)

    fingerprint = merge_fingerprints([split.fingerprint for split in splits])
    num_bytes = sum([split.num_bytes for split in splits])
    return num_bytes, [split.name for split in splits], fingerprint


def fingerprint(name, token):
    print("[bold yellow]🔍 Retrieving dataset fingerprint from HuggingFace Hub...[/bold yellow]")
    api = HfApi(token=token)
    info = api.dataset_info(name)
    print(f"[bold yellow]✔ Fingerprint (SHA) retrieved: {info.sha}[/bold yellow]")
    return info.sha


def load(name, token, config, directory):
    api = HfApi(token=token)
    dataset = load_dataset(name, config, token=token)

    if not isinstance(dataset, DatasetDict):
        print("[bold red]⚠ The dataset is not a DatasetDict. Wrapping it in one with a 'train' split.[/bold red]")
        dataset = DatasetDict({"train": dataset})

    print("[bold yellow]💾 Converting dataset to factory format...[/bold yellow]")
    hf_to_factory_dataset(dataset, directory)

    info = api.dataset_info(name)
    return info.sha
