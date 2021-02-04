import os
import json
from . import utils

class Config:
    def __init__(self, *args):
        for k in args:
            setattr(self, k, None)
    
    def get_keys(self):
        '''
        get_keys method returns the Config class populated with the defined enviroments within the __init__ method.
        It uses a sequential order to get the keys, being (low -> high precedence):
            * SSM - gets the enviroments from AWS Parameter Store SSM.
            * Envs - gets the enviroments from the local machine.
            * Config file - gets the enviroments from a local JSON file
            -----------------------------------------------------------
        Remember to keep the enviroments on the same name on each occasion, or else it won't be found
        '''
        self.all_keys = {key: {'value': value, 'setby': None} for key, value in self.__dict__.items()}

        config_file_exists = utils.check_exists_file("config.json")
        if config_file_exists:
            f = open("config.json", "r")
            self.configjson = json.load(f)
        
        for key in self.all_keys:
            if config_file_exists:
                self.__get_from_file(key)
                continue
            elif self.__get_from_env(key):
                continue

        return self.all_keys

    def __get_from_env(self, key: str) -> bool:
        prefix = "app_"
        if utils.check_env_by_name(prefix+key):
            self.all_keys[key]['value'] = os.getenv(prefix+key)
            self.all_keys[key]['setby'] = 'ENV'
            return True
        return False

    def __get_from_file(self, key: str) -> None:
        if value := self.configjson.get(key):
            self.all_keys[key]['value'] = value
            self.all_keys[key]['setby'] = 'CONFIG-FILE'
            return True
        return False
   