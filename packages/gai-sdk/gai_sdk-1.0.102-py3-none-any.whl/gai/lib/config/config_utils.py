import os
import yaml
from gai.lib.common.utils import get_app_path
from gai.lib.config.pydantic.gai_config import ClientConfig,ClientCategoryConfig,ClientLLMConfig
from typing import overload, Optional
from openai.types.chat_model import ChatModel
from typing import get_args

def get_gai_config(file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def save_gai_config(config, file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False)
    
def get_gai_url(category_name):
    config = get_gai_config()
    key = f"gai-{category_name}"
    url = config["clients"][key]["url"]
    return url

# "api_url" property contains the fully qualified domain name of this API server
def get_api_url():
    config = get_gai_config()
    url = config["api_url"]
    return url

@overload
def get_client_config(category:str, engine:str, model:str, file_path:str=None) -> ClientLLMConfig:
    ...

@overload
def get_client_config(config_type_or_name:str, file_path:str=None) -> ClientLLMConfig:
    ...

def get_client_config(
        category: Optional[str] = None,
        engine: Optional[str] = None,
        model: Optional[str] = None,
        config_type_or_name: Optional[str] = None,
        file_path: Optional[str] = None    
    ) -> ClientLLMConfig:
    """
    Retrieves a ClientLLMConfig object based on the provided arguments.

    Parameters:
        category (str, optional): The category of the configuration.
        engine (str, optional): The engine name (e.g., "openai").
        model (str, optional): The model name (e.g., "gpt-4").
        config_type_or_name (str, optional): A combined configuration identifier 
            (e.g., "ttt-llamacpp-dolphin") or a category name (e.g., "ttt").
        file_path (str, optional): Path to the configuration file.

    Returns:
        ClientLLMConfig: The configuration object based on the provided arguments.

    Raises:
        ValueError: If the arguments are invalid or required keys are missing.

    Examples:
        1. Using a combined identifier:
            config = get_client_config(config_type_or_name="ttt-llamacpp-dolphin", file_path="config.yaml")

        2. Using explicit category, engine, and model:
            config = get_client_config(category="ttt", engine="llamacpp", model="dolphin", file_path="config.yaml")

        3. Using only a category to fetch default configuration:
            config = get_client_config(category="ttt", file_path="config.yaml")

        4. Handling specific models for OpenAI:
            config = get_client_config(category="ttt", engine="openai", model="gpt-4", file_path="config.yaml")
    """
    
    # step 1: The following code will extract both config_type_or_name and (category, engine, model) from each other if one is provided.
   
    if config_type_or_name:
        # Either config name (e.g. "ttt-llamacpp-dolphin") or category name (e.g. "ttt")
        name_parts = config_type_or_name.split("-")
        if len(name_parts) >= 3:
            # Assign the first two parts and join the rest for the model
            category = name_parts[0]
            engine = name_parts[1]
            model = "-".join(name_parts[2:])  # Join all parts from the 3rd onward            
        elif len(name_parts) == 1:
            # If there's only one part, treat it as the category
            category = config_type_or_name
            engine = None
            model = None
        else:
            raise ValueError("Invalid format for config_type_or_name")
    else:
        # If config_type_or_name is not provided, then category, engine, and model must be provided
        if not (category and engine and model):
            raise ValueError("Either config_type_or_name or (category, engine and model) must be provided.")
        config_type_or_name = f"{category}-{engine}-{model}"
    
    # step 2: Extract the category config, ie. ttt_config, etc
    
    config = get_gai_config(file_path=file_path)
    config = ClientConfig.from_config(config)
    category_config:ClientCategoryConfig = getattr(config, category, None)
    if category_config is None:
        raise ValueError(f"Config type {category} not found in config")
    
    # step 3: Extract default config or named config from the category config.
    
    if engine is None or model is None:
        ## This means use default category config
        default = category_config.default
        return category_config.configs[default]
    
    if engine != None and model != None:
        if engine == "openai":
            if model in get_args(ChatModel):
                openai_config = category_config.configs["ttt-openai-gpt4"]
                openai_config.model = model
                return openai_config
            else:
                raise ValueError(f"Invalid openai model {config.model}")
        else:
            return category_config.configs.get(config_type_or_name, None)
    
    raise ValueError(f"engine and model must be provided together")

