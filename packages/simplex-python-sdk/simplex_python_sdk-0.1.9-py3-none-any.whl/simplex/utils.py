from .enums import BrowserAction, WebElement, Text, Duration, BrowserInteraction
from typing import List, Tuple


def _parse_action_response(response: str) -> List[BrowserInteraction]:
        """Parse step string into list of BrowserInteractions"""
        interactions = []
        for line in response.split('\n'):
            try: 
                action, content = line.split(',', 1)
                action = action.strip()
                content = content.strip()
            except: 
                print("not parsing line because poorly formatted response: ", response)
                break
            
            try:
                browser_action = BrowserAction[action]
            except KeyError:
                raise ValueError(f"{action} is not a valid BrowserAction")
            
            # Create appropriate ActionParam based on the action type
            if browser_action == BrowserAction.TYPE:
                action_param = Text(body=content)
                
            elif browser_action == BrowserAction.WAIT:
                try:
                    duration = float(content)
                except ValueError:
                    duration = 1.0  # Default to 1 second if content is not a float
                action_param = Duration(seconds=duration)
            else:
                action_param = WebElement(
                    desc=content,
                    coordinates=None        #need to run find later
                )
            
            interaction = BrowserInteraction(
                action=browser_action,
                action_param=action_param
            )
            
            interactions.append(interaction)
        
        return interactions

def center_bbox(bbox: List[int]) -> Tuple[int, int]:
    """
    Center the bbox

    Args:
        bbox: List[int] - The bounding box coordinates [x1, y1, x2, y2]

    Returns:
        Tuple[int, int] - The center coordinates (x, y)
    """
    return (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)


