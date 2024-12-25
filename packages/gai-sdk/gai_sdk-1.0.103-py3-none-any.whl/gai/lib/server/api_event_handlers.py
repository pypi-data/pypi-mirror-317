import os
from gai.lib.common.utils import free_mem
from gai.lib.server.singleton_host import SingletonHost
from rich.console import Console
console = Console()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.lib.server import api_dependencies

# Initialize the fastapi application state
from gai.lib.config.pydantic.gai_config import ServerLLMConfigBase

def get_startup_event(app, category:str, pyproject_toml, llm_config:ServerLLMConfigBase):

    async def startup_event():
        
        try:
            # check freemem before loading the model
            free_mem()

            # version check
            logger.info(f"Starting Gai LLM Service ({category}) v{api_dependencies.get_app_version(pyproject_toml)}")
            logger.info(f"Version of gai_sdk installed = {api_dependencies.get_sdk_version()}")
            
            # extract the default generator config for a category and add it to the app state

            app.state.llm_config = llm_config

            # initialize host and add it to the app state
            host = SingletonHost.GetInstanceFromConfig(llm_config)
            host.load()
            logger.info(f"Model loaded = [{llm_config.name}]")
            app.state.host = host

            # check freemem after loading the model
            free_mem()    
        except Exception as e:
            logger.error(f"Failed to load default model: {e}")
            raise e

        app.state.host = host

    return startup_event

def get_shutdown_event(app):
    
    async def shutdown_event():
        host = app.state.host
        if host:
            host.unload()

    return shutdown_event