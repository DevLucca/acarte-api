import os
import json
from .. import utils

class Settings:
    """ This class implements the import of variables that will be used throughout
    the application.
    It uses a sequential order to get the variables, being low -> high precedence:
        * Envs - gets the enviroments from the local machine.
        * Config file - gets the enviroments from a local JSON/yaml file
    """

    def __init__(self, *var_names: list):
        for k in var_names: setattr(self, k, None)

    def get_envs(self) -> dict:
        self.all_vars = {key: {'value': value, 'setby': None} for key, value in self.__dict__.items()}

        config_file_exists = utils.check_exists_file("config.json")
        if config_file_exists:
            f = open("config.json", "r")
            self.configjson = json.load(f)
        
        for key in self.all_vars:
            if config_file_exists:
                self.__get_from_file(key)
                continue
            elif self.__get_from_env(key):
                continue

        return self.all_vars

    def __get_from_env(self, key: str) -> bool:
        prefix = "app_"
        if utils.check_env_by_name(prefix+key):
            self.all_vars[key]['value'] = os.getenv(prefix+key)
            self.all_vars[key]['setby'] = 'ENV'
            return True
        return False

    def __get_from_file(self, key: str) -> None:
        if value := self.configjson.get(key):
            self.all_vars[key]['value'] = value
            self.all_vars[key]['setby'] = 'CONFIG-FILE'
            return True
        return False
