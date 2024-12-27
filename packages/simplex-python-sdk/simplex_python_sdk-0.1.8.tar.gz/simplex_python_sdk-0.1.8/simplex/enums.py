from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple, Optional, Union

class BrowserAction(Enum):
    CLICK = auto()
    SCROLL = auto()
    TYPE = auto()
    HOVER = auto()
    WAIT = auto()
    
    def __str__(self):
        return self.name

@dataclass
class WebElement:
    """Parameter for actions that need element description and coordinates"""
    desc: str
    coordinates: Tuple[int, int]
    
    def __str__(self):
        return self.desc
    
    def validate(self) -> bool:
        """
        Validates if the element has a description and coordinates
        """
        return self.desc and self.coordinates

@dataclass
class Text:
    """Parameter for actions that need text input"""
    body: str
    
    def __str__(self):
        return self.body
    
    def validate(self) -> bool:
        """
        Validates if the text has a body
        """
        return self.body

@dataclass
class Duration:
    """Parameter for actions that need time duration"""
    seconds: float
    
    def __str__(self):
        return str(self.seconds)

    def validate(self) -> bool:
        """
        Validates if the duration has a seconds
        """
        return self.seconds

# ActionParam is a type alias that can be any of these types
ActionParam = Union[WebElement, Text, Duration]

# Usage examples:
@dataclass
class BrowserInteraction:
    """
    Represents a browser interaction combining the action type and its required parameters.
    Different actions require different parameters:
    - CLICK: requires coordinates
    - SCROLL: requires coordinates
    - TYPE: requires coordinates and text
    - HOVER: requires coordinates, optional duration
    - WAIT: requires duration
    """
    action: BrowserAction
    action_param: ActionParam
    
    def is_type(self, action_type: str) -> bool:
        """
        Check if the interaction is of a specific type (case-insensitive)
        Example: interaction.is_type('click') or interaction.is_type('HOVER')
        """
        return self.action.name.upper() == action_type.upper()

    def validate(self) -> bool:
        """
        Validates if the interaction has all required parameters for the action.
        Each action requires specific parameter types:
        - CLICK, SCROLL, HOVER: requires WebElement
        - TYPE: requires Text
        - WAIT: requires Duration
        """
        return self.action_param.validate()
    
    def __str__(self):
        return f"{self.action}: {self.action_param}"


def str_to_browser_action(action_str: str) -> BrowserAction:
    """Convert string to BrowserAction, case-insensitive"""
    try:
        return BrowserAction[action_str.upper()]
    except KeyError:
        raise ValueError(f"Invalid action: {action_str}. Valid actions are: {[a.name for a in BrowserAction]}")

