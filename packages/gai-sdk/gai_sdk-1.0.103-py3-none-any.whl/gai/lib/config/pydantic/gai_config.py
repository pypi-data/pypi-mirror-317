from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Dict, List

class ClientLLMConfig(BaseSettings):
    type: str
    engine: str
    model: str
    name: str
    url: Optional[str] = None
    env: Optional[Dict] = None
    extra: Optional[Dict] = None
    hyperparameters: Optional[Dict] = {}

class ClientCategoryConfig(BaseSettings):
    default: str=None
    configs: Optional[Dict[str,ClientLLMConfig]]={}
        
class ClientConfig(BaseSettings):
    ttt: ClientCategoryConfig = None
    rag: ClientCategoryConfig = None
    tti: ClientCategoryConfig = None
    tts: ClientCategoryConfig = None
    stt: ClientCategoryConfig = None
    itt: ClientCategoryConfig = None
    ttc: ClientCategoryConfig = None
    
    @classmethod
    def from_config(cls, config: dict):
        # Preprocess the config and initialize the object
        return cls(
            ttt=ClientCategoryConfig(**config["clients"]["ttt"]),
            rag=ClientCategoryConfig(**config["clients"]["rag"]),
            tti=ClientCategoryConfig(**config["clients"]["tti"]),
            tts=ClientCategoryConfig(**config["clients"]["tts"]),
            stt=ClientCategoryConfig(**config["clients"]["stt"]),
            itt=ClientCategoryConfig(**config["clients"]["itt"]),
            ttc=ClientCategoryConfig(**config["clients"]["ttc"]),
        )
    
class ModuleConfig(BaseSettings):
    name: str
    class_: str = Field(alias="class")  # Use 'class' as an alias for 'class_'

    class Config:
        allow_population_by_name = True  # Allow access via both 'class' and 'class_'

class ServerLLMConfigBase(BaseSettings):
    type: str
    engine: str
    model: str
    name: str
    module: ModuleConfig
    