import os
import sys
import json

from ansible import constants as C
from ansible.config.manager import (
    ConfigManager,
    find_ini_config_file,
    to_native,
)


def get_settings():
    """
    Retrieves current Ansible (ansible.cfg) settings as a dictionary.
    Works with newer Ansible/ansible-core (2.10+),
    where 'ConfigManager.data' no longer exists.
    """
    config_file = os.getenv('ANSIBLE_CONFIG', find_ini_config_file())
    if config_file:
        os.environ['ANSIBLE_CONFIG'] = to_native(config_file)

    config = ConfigManager()
    dict_settings = {}

    # This returns all recognized configuration definitions.
    # Then we ask the config manager for each value actually in use.
    definitions = config.get_configuration_definitions()
    vars_dict = C.__dict__.copy()
    vars_dict.update(os.environ)

    for setting_name in definitions:
        # config.get_config_value(...) is the modern approach
        value = config.get_config_value(setting_name, variables=vars_dict)
        dict_settings[str(setting_name)] = value

    return dict_settings


def handler(*args, **kwargs):
    """
    Prints Ansible config as JSON to stdout.
    """
    dict_settings = get_settings()
    json.dump(dict_settings, sys.stdout, indent=4)
    sys.stdout.flush()
