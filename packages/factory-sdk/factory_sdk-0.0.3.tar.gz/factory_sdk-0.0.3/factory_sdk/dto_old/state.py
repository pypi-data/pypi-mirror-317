from pydantic import BaseModel
from enum import Enum

class FactoryState(str,Enum):
    INITIALIZED="INITIALIZED"
    PROCESSING="PROCESSING"
    READY="READY"
    FAILED="FAILED"