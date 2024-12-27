from abc import ABC, abstractmethod
from typing import Dict, Literal
from typing import TypedDict

class QueryDescription(TypedDict):
    name: str
    description: str

class ActionParameters(TypedDict):
    action: Literal['query', 'command', 'unknown']
    actionName: str | None
    parameters: Dict[str,any] | None
    request: str | None    

class SkillDescription(TypedDict):
    name: str
    description: str
    
class Reasoner(ABC):
    @abstractmethod
    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> ActionParameters:
        '''Selects requested skill based on utterance and list of available skills. 
        Should return index of selected skill in provided list of skills'''
        pass
