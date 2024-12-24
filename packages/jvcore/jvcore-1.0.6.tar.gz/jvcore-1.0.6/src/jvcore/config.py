from abc import ABC


class Config(ABC):
    def get(self, module_name: str, key: str = None):
        '''gets jarvis config entry for given module'''
        pass
