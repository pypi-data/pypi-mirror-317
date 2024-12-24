from abc import ABC, abstractmethod

class SkillBase(ABC):    
    @abstractmethod
    def execute(self, **params) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def getDescription() -> str:
        '''provide a clear description of skill posibilities, matcher will be matching user utterance based on this description'''
        pass
    
    @staticmethod
    @abstractmethod
    def getName() -> str:
        '''name of the skill'''
        pass
    
    