from gai.lib.common.utils import get_app_path,get_rc,get_packaged_gai_config_path
from gai.lib.config.config_utils import get_gai_config
import os

def test_get_app_path():
    app_path=get_app_path()
    assert app_path==os.path.expanduser("~/.gai")

def test_get_rc():
    rc=get_rc()
    assert rc["app_dir"]=="~/.gai"

def test_get_packaged_gai_config_path():
    config_path = get_packaged_gai_config_path()
    print(config_path)

