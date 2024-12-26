from abc import ABC, abstractmethod
from typing import Dict, Literal
from typing import TypedDict

class QueryDescription:
    pass #todo

class ActionParameters(TypedDict):
    action: Literal['query', 'command']
    actionName: str
    parameters: Dict[str,any]

class SkillDescription:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
class Reasoner(ABC):
    @abstractmethod
    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> ActionParameters:
        '''Selects requested skill based on utterance and list of available skills. 
        Should return index of selected skill in provided list of skills'''
        pass
