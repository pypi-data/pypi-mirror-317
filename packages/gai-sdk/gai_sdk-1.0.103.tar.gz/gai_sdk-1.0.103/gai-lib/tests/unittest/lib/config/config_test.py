import os
from gai.lib.config.config_utils import get_gai_config,get_client_config
def test_get_gai_config():
    here = os.path.dirname(__file__)
    file_path =  os.path.abspath(os.path.join(here,"..","..","..","..","..","gai-data","src","gai","data","gai.yml"))
    config = get_gai_config(file_path)
    assert config["clients"]["ttt"]["default"]=="ttt-llamacpp-dolphin"

def test_get_default_client_config():
    here = os.path.dirname(__file__)
    file_path =  os.path.abspath(os.path.join(here,"..","..","..","..","..","gai-data","src","gai","data","gai.yml"))

    ### ACT
    client_config = get_client_config(config_type_or_name="ttt", file_path=file_path)

    assert client_config.name=="ttt-llamacpp-dolphin"
    assert client_config.url=="http://localhost:12031/gen/v1/chat/completions"

def test_get_named_config():
    here = os.path.dirname(__file__)
    file_path =  os.path.abspath(os.path.join(here,"..","..","..","..","..","gai-data","src","gai","data","gai.yml"))
    
    ### ACT
    client_config = get_client_config(config_type_or_name="ttt-openai-gpt4", file_path=file_path)
    
    assert client_config.name=="ttt-openai-gpt4"
    assert client_config.url is None

