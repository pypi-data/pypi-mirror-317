import threading
from gai.lib.common import logging, generators_utils
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)
from gai.lib.config.pydantic.gai_config import ServerLLMConfigBase

class SingletonHost:
    __instance = None       # singleton

    @staticmethod
    def GetInstanceFromPath(generator_name,config_path=None,verbose=True):
        """Static method to access this singleton class's instance."""
        config_path=os.path.expanduser(config_path)
        config = generators_utils.load_generators_config(config_path)
        if SingletonHost.__instance == None:
            SingletonHost.__instance=SingletonHost(config[generator_name],verbose=verbose)
        else:
            # Override __instance's config and verbose if it already exists
            SingletonHost.__instance.config=config
            SingletonHost.__instance.__verbose=verbose
        return SingletonHost.__instance

    @staticmethod
    def GetInstanceFromConfig(config:ServerLLMConfigBase,verbose=True):
        """Static method to access this singleton class's instance."""
        if SingletonHost.__instance == None:
            SingletonHost.__instance=SingletonHost(config,verbose=verbose)
        else:
            # Override __instance's config and verbose if it already exists
            SingletonHost.__instance.config=config
            SingletonHost.__instance.__verbose=verbose
        return SingletonHost.__instance

    def __init__(self,config:ServerLLMConfigBase,verbose=True):
        self.__verbose=verbose

        """Virtually private constructor."""
        if SingletonHost.__instance is not None:
            raise Exception(
                "SingletonHost: This class is a singleton! Access using GetInstance().")
        else:
            # This class only has 4 attributes

            # config is always the first to be loaded from constructor
            self.config = config

            # generator is loaded by calling load()
            self.generator = None

            # generator_name matches config["generator_name"] and is loaded only when self.generator is successfully loaded 
            self.generator_name = None

            # Finally, for thread safety and since this is run locally, use semaphore to ensure only one thread can access the generator at a time
            self.semaphore = threading.Semaphore(1)

            SingletonHost.__instance = self

    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self,exc_type, exc_value,traceback):
        self.unload()
        import gc,torch
        gc.collect()
        torch.cuda.empty_cache()

    # This is idempotent
    def load(self):

        if self.generator_name == self.config.name:
            logger.debug(
                "SingletonHost.load: Generator is already loaded. Skip loading.")
            return self

        if self.generator_name and self.generator_name != self.config.name:
            logger.debug(
                "SingletonHost.load: New generator_name specified, unload current generator.")
            if self.generator:
                self.unload()
            return self

        try:
            target_name=self.config.name
            logger.info(f"SingletonHost: Loading generator {target_name}...")

            # Load generator using reflection
            import importlib
            module = importlib.import_module(self.config.module.name)
            class_ = getattr(module, self.config.module.class_)
            self.generator = class_(llm_config=self.config, verbose=self.__verbose)
            self.generator.load()
            self.generator_name=target_name
            return self
        except Exception as e:
            self.unload()
            logger.error(
                f"SingletonHost: Error loading generator {self.generator_name}: {e}")
            raise e
            
    def unload(self):
        if self.generator is not None:
            self.generator.unload()
            del self.generator
            self.generator = None
            self.generator_name = None
            import gc,torch
            gc.collect()
            torch.cuda.empty_cache()
        return self
