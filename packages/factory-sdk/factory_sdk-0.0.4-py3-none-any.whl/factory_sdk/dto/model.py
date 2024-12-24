from factory_sdk.dto.resource import FactoryResourceInitData, FactoryResourceMeta, FactoryResourceRevision, FactoryResourceObject
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from transformers import AutoModelForCausalLM, AutoProcessor, AutoTokenizer
from PIL import Image
from typing import List, Dict, Union

class ModelArchitecture(str,Enum):
    Gemma2ForCausalLM="Gemma2ForCausalLM"
    LlamaForCausalLM="LlamaForCausalLM"
    MistralForCausalLM="MistralForCausalLM"
    Phi3ForCausalLM="Phi3ForCausalLM"
    Qwen2ForCausalLM="Qwen2ForCausalLM"
    PaliGemmaForConditionalGeneration="PaliGemmaForConditionalGeneration"
    Phi3VForCausalLM="Phi3VForCausalLM"

class SupportedModels(str,Enum):
    #meta-llama/Llama-3.2-3B-Instruct
    LLama3_2_Instruct_3B="meta-llama/Llama-3.2-3B-Instruct"
    #meta-llama/Llama-3.2-1B-Instruct
    LLama3_2_Instruct_1B="meta-llama/Llama-3.2-1B-Instruct"
    #Qwen/Qwen2.5-0.5B-Instruct
    Qwen2_5_Instruct_0_5B="Qwen/Qwen2.5-0.5B-Instruct"
    #Qwen/Qwen2.5-1.5B-Instruct
    Qwen2_5_Instruct_1_5B="Qwen/Qwen2.5-1.5B-Instruct"
    #Qwen/Qwen2.5-3B-Instruct
    Qwen2_5_Instruct_3B="Qwen/Qwen2.5-3B-Instruct"
    #Qwen/Qwen2.5-7B-Instruct
    Qwen2_5_Instruct_7B="Qwen/Qwen2.5-7B-Instruct"
    #mistralai/Mistral-7B-Instruct-v0.3
    Mistral7BInstruct="mistralai/Mistral-7B-Instruct-v0.3"
    #google/gemma-2-2b
    Gemma2_Instruct_2B="google/gemma-2-2b-it"
    #google/gemma-2-9b-it
    Gemma2_Instruct_9B="google/gemma-2-9b-it"
    #microsoft/Phi-3.5-mini-instruct
    Phi3_5_Mini_Instruct="microsoft/Phi-3.5-mini-instruct"
    #google/paligemma2-3b-pt-224
    PaliGemma_3B_224="google/paligemma2-3b-pt-224"
    #google/paligemma2-3b-pt-448
    PaliGemma_3B_448="google/paligemma2-3b-pt-448"
    #google/paligemma2-3b-pt-896
    PaliGemma_3B_896="google/paligemma2-3b-pt-896"
    #manufactAILabs/ModelOne
    ModelOne="manufactAILabs/ModelOne"
    #microsoft/Phi-3.5-vision-instruct
    Phi3_5_Vision_Instruct="microsoft/Phi-3.5-vision-instruct"

MODEL2ARCH={
    SupportedModels.LLama3_2_Instruct_3B:ModelArchitecture.LlamaForCausalLM,
    SupportedModels.LLama3_2_Instruct_1B:ModelArchitecture.LlamaForCausalLM,
    SupportedModels.Qwen2_5_Instruct_0_5B:ModelArchitecture.Qwen2ForCausalLM,
    SupportedModels.Qwen2_5_Instruct_1_5B:ModelArchitecture.Qwen2ForCausalLM,
    SupportedModels.Qwen2_5_Instruct_3B:ModelArchitecture.Qwen2ForCausalLM,
    SupportedModels.Qwen2_5_Instruct_7B:ModelArchitecture.Qwen2ForCausalLM,
    SupportedModels.Mistral7BInstruct:ModelArchitecture.MistralForCausalLM,
    SupportedModels.Gemma2_Instruct_2B:ModelArchitecture.Gemma2ForCausalLM,
    SupportedModels.Gemma2_Instruct_9B:ModelArchitecture.Gemma2ForCausalLM,
    SupportedModels.Phi3_5_Mini_Instruct:ModelArchitecture.Phi3ForCausalLM,
    SupportedModels.PaliGemma_3B_224:ModelArchitecture.PaliGemmaForConditionalGeneration,
    SupportedModels.PaliGemma_3B_448:ModelArchitecture.PaliGemmaForConditionalGeneration,
    SupportedModels.PaliGemma_3B_896:ModelArchitecture.PaliGemmaForConditionalGeneration,
    SupportedModels.ModelOne:ModelArchitecture.Phi3VForCausalLM,
    SupportedModels.Phi3_5_Vision_Instruct:ModelArchitecture.Phi3VForCausalLM
}

ARCH2AUTO={
    ModelArchitecture.LlamaForCausalLM:AutoModelForCausalLM,
    ModelArchitecture.Qwen2ForCausalLM:AutoModelForCausalLM,
    ModelArchitecture.MistralForCausalLM:AutoModelForCausalLM,
    ModelArchitecture.Gemma2ForCausalLM:AutoModelForCausalLM,
    ModelArchitecture.Phi3ForCausalLM:AutoModelForCausalLM,
    ModelArchitecture.PaliGemmaForConditionalGeneration:AutoModelForCausalLM,
    ModelArchitecture.Phi3VForCausalLM:AutoModelForCausalLM
}
ARCH2PROCESSOR={
    ModelArchitecture.LlamaForCausalLM:AutoTokenizer,
    ModelArchitecture.Qwen2ForCausalLM:AutoTokenizer,
    ModelArchitecture.MistralForCausalLM:AutoTokenizer,
    ModelArchitecture.Gemma2ForCausalLM:AutoTokenizer,
    ModelArchitecture.Phi3ForCausalLM:AutoTokenizer,
    ModelArchitecture.PaliGemmaForConditionalGeneration:AutoProcessor,
    ModelArchitecture.Phi3VForCausalLM:AutoProcessor
}

class ModelMeta(FactoryResourceMeta):
    pass

class ModelInitData(FactoryResourceInitData):
    def create_meta(self,tenant_name,project_name)->ModelMeta:
        return ModelMeta(name=self.name,project=project_name,tenant=tenant_name)

class ModelRevision(FactoryResourceRevision):
    pass

class ModelObject(BaseModel):
    meta: ModelMeta
    revision: ModelRevision

class Message(BaseModel):
    role: str
    content: str

class ModelInput(BaseModel):
    messages: List[Message]

class Token(BaseModel):
    text:str

class GeneratedToken(Token):
    logprob: float
    rank: int
    
class TrainModelInput(ModelInput):
    label: str

class TensorInfo(BaseModel):
    name: str
    num_params: int
    shape: List[int]
    dtype: str
    metrics: Dict[str, Optional[float]]

class TensorMap(BaseModel):
    tensors: Dict[str, TensorInfo]


class LayerInfo(BaseModel):
    name: str
    num_params: List[int]
    tensors: List[str]
    shapes:List[List[int]]
    dtypes: List[str]
    metrics: Dict[str, List[Optional[float]]]

class LayerMap(BaseModel):
    layers: Dict[str, LayerInfo]

    @staticmethod
    def from_tensors(tensor_map: TensorMap):
        layer_map=LayerMap(layers={})
        for key, tensor in tensor_map.tensors.items():
            #remove .weight or .bias from the key to get the layer name
            keys=key.split(".")
            tensor_name=keys[-1]
            if keys[-1] in ["weight","bias"]:
                layer_name=".".join(keys[:-1])
                keys=keys[:-1]
            else:
                layer_name=key

            if layer_name not in layer_map.layers:
                layer_map.layers[layer_name]=LayerInfo(
                    name=layer_name,
                    num_params=[tensor.num_params],
                    tensors=[tensor_name],
                    shapes=[tensor.shape],
                    dtypes=[tensor.dtype],
                    metrics={k:[v] for k,v in tensor.metrics.items()}
                )
            else:
                layer=layer_map.layers[layer_name]
                layer.num_params.append(tensor.num_params)
                layer.tensors.append(tensor_name)
                layer.shapes.append(tensor.shape)
                layer.dtypes.append(tensor.dtype)
                for k,v in tensor.metrics.items():
                    layer.metrics[k].append(v)
        return layer_map