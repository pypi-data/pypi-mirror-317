from huggingface_hub import HfApi
from factory_sdk.logging import logger
from joblib import Parallel, delayed
from tqdm_joblib import tqdm_joblib
from transformers import AutoConfig
from tqdm_joblib import tqdm_joblib
from joblib import Parallel, delayed
from rich import print
from transformers import AutoModelForCausalLM, AutoProcessor, AutoTokenizer
from glob import glob
from safetensors import safe_open
from tqdm.auto import tqdm
from factory_sdk.dto.model import TensorInfo, TensorMap

def fingerprint(name,token):
    print("[bold yellow]🔍 Refactory_api/optimizationtrieving dataset fingerprint from HuggingFace Hub...[/bold yellow]")
    api=HfApi(
        token=token
    )
    info=api.model_info(
        name
    )
    print(f"[bold yellow]✔ Fingerprint (SHA) retrieved: {info.sha}[/bold yellow]")
    return info.sha

FILE_TYPES=[".py",".md","LICENSE",".json",".yaml",".yml",".txt",".safetensors",".model"]

def load(name,token,directory,max_parallel_download=1):
    api=HfApi(
        token=token
    )
    info=api.repo_info(
        name,repo_type="model"
    )
    siblings=info.siblings

    #filter siblings
    siblings=[sibling for sibling in siblings if any(file_type in sibling.rfilename for file_type in FILE_TYPES)]

    #download the model
    with tqdm_joblib(total=len(siblings)) as progress_bar:
        Parallel(n_jobs=max_parallel_download)(
            delayed(lambda f:api.hf_hub_download(
                repo_id=name,filename=f,repo_type="model",token=token,local_dir=directory
            ))(
                sibling.rfilename,
            )
            for sibling in siblings
        )

    
    
    return info.sha

