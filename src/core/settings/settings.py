import os
import json
from core import utils

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
        self.all_vars = {key: {'value': value, 'set_by': None} for key, value in self.__dict__.items()}

        config_file_exists = utils.check_exists_file("config.json")
        if config_file_exists:
            f = open("config.json", "r")
            self.configjson = json.load(f)
        
        for key in self.all_vars:
            self.all_vars[key] = Key(self.all_vars[key])
            if config_file_exists:
                self.__get_from_file(key)
                continue
            elif self.__get_from_env(key):
                continue

        return Key(self.all_vars)

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


class Key(dict):
    def __init__(self, *args, **kwargs):
        super(Key, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Key, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Key, self).__delitem__(key)
        del self.__dict__[key]