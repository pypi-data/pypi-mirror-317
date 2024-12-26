from abc import ABC, abstractmethod
from typing import Dict
from typing import TypedDict

class QueryDescription:
    pass #todo

class SkillParameters(TypedDict):
    commandName: str
    parameters: Dict[str,any]

class SkillDescription():
    pass
    
class Reasoner(ABC):
    @abstractmethod
    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> SkillParameters:
        '''Selects requested skill based on utterance and list of available skills. 
        Should return index of selected skill in provided list of skills'''
        pass
