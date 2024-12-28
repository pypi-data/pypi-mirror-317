from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Literal
from typing import TypedDict

class ActionType(Enum):
    Query = 1
    Command = 2

class ActionParameters(TypedDict):
    action: ActionType
    actionName: str
    parameters: Dict[str,any]

class ParameterDescription(TypedDict):
    description: str
    type: str | Dict[str, 'ParameterDescription']

class ActionDescription(TypedDict):
    description: str
    parameters: Dict[str, ParameterDescription]
    
class Reasoner(ABC):
    @abstractmethod
    def selectSkill(self, skillsAndQueries: Dict[str, ActionDescription], utterance: str) -> ActionParameters:
        '''Selects requested skill/query based on utterance and list of available skills/queries.'''
        pass
