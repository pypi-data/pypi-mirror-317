from typing import Optional, Dict, Any, List
from PIL import Image
import requests
from io import BytesIO
import tempfile

from .enums import BrowserInteraction, BrowserAction
from .utils import _parse_action_response, center_bbox
from .browserActor import BrowserActor

# BASE_URL = "https://u3mvtbirxf.us-east-1.awsapprunner.com"


# dev: 
BASE_URL = "https://vytaq823ad.us-east-1.awsapprunner.com"

class Simplex:
    """
    Simplex client for interacting with the Simplex API.
    
    Example:
        client = SimplexAI(api_key="your-api-key")
        element = client.find_element(
            element_description="Sign up button",
            screenshot=screenshot
        )
    """

    def __init__(
        self,
        api_key: str,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        record_video: bool = False,
        headless: bool = True,
        browser_actor: Optional[BrowserActor] = None,
    ):
        """
        Initialize the SimplexAI client.

        Args:
            api_key: Your API key for SimplexAI.
            base_url: The base URL for the SimplexAI API.
            timeout: Timeout in seconds for API requests.
            max_retries: Maximum number of retries for failed requests.
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

        self.browser_actor = browser_actor or BrowserActor(headless=headless, record_video=record_video)

    def find_element(
        self,
        element_description: str,
        screenshot: Image.Image,
    ) -> List[int]:
        """
        Find an element in a screenshot based on a natural language description.
        
        Args:
            element_description: A natural language description of the element to find.
            screenshot: A screenshot of the current screen.
        
        Returns:
            A list of 4 integers representing the bounding box of the element
            [x1, y1, x2, y2]
        """
        
        if not self.api_key:
            raise Exception("API key is required")
        
        endpoint = f"{BASE_URL}/find-element"

        # Convert PIL Image to bytes and save as temp file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            screenshot.save(temp_file.name, format='PNG')
            temp_file_path = temp_file.name

            # Open and send the file
            with open(temp_file_path, 'rb') as f:
                files = {
                    'image_data': ('screenshot.png', f, 'image/png'),
                    'element_description': (None, element_description),
                    'api_key': (None, self.api_key)
                }
                response = requests.post(
                    endpoint,
                    files=files,
                )

            if response.status_code == 200:
                res = response.json()
                bbox = [int(res['x1']), int(res['y1']), int(res['x2']), int(res['y2'])]
                return bbox
            else:
                print(response.json())
                raise Exception(f"Failed to find element: {element_description}")


    def get_next_step(
        self,
        task_description: str,
        screenshot: Image.Image,
        history: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Get the next step to complete a task based on current screenshot and history.

        task_description: A natural language description of the task to complete.
        screenshot: A screenshot of the current screen.
        history: A list of previous steps taken to complete the task. 
        """

        if not self.api_key:
            raise Exception("API key is required")

        endpoint = f"{BASE_URL}/get_next_step"

        # Convert PIL Image to bytes and save as temp file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            screenshot.save(temp_file.name, format='PNG')
            temp_file_path = temp_file.name

        # Open and send the file
        with open(temp_file_path, 'rb') as f:
            files = {
                'screenshot': ('screenshot.png', f, 'image/png'),
                'high_level_task': (None, task_description),
                'api_key': (None, self.api_key)
            }

            if history:
                files['history'] = history

            response = requests.post(
                endpoint,
                files=files,
            )

            if response.status_code == 200:
                res = response.json()
                return res
            else:
                raise Exception(f"Failed to get next step: {task_description}")
            

    def is_step_complete(
        self,
        step_description: str,
        screenshot: Image.Image,
    ) -> bool:
        """
        Check if a step is complete based on a natural language description of the step.
        """
        if not self.api_key:
            raise Exception("API key is required")
        
        endpoint = f"{BASE_URL}/is_completed"

        # Convert PIL Image to bytes and save as temp file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            screenshot.save(temp_file.name, format='PNG')
            temp_file_path = temp_file.name

            # Open and send the file
            with open(temp_file_path, 'rb') as f:
                files = {
                    'screenshot': ('screenshot.png', f, 'image/png'),
                    'high_level_task': (None, step_description),
                    'api_key': (None, self.api_key)
                }

                response = requests.post(
                    endpoint,
                    files=files,
                )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to check if step is complete: {step_description}")

    def step_to_action(
        self,
        step_description: str,
        screenshot: Image.Image,
    ) -> List[BrowserInteraction]:
        """
        Convert a step description to a Simplex BrowserInteraction.

        args:
            step_description: A natural language description of the step to complete.
            screenshot: A screenshot of the current screen.

        returns:
            A list of BrowserInteractions to complete the step.
            Run find_element on any interactions that need coordinates.
        """
        
        if not self.api_key:
            raise Exception("API key is required")
        
        endpoint = f"{BASE_URL}/step_to_action"
        
        data = {
            'step': step_description,
            'api_key': self.api_key
        }

        response = requests.post(endpoint, data=data)

        if response.status_code == 200:
            action_phrase = response.json() 
            browser_interactions = _parse_action_response(action_phrase)

            ## any browser interactions that need coordinates should be run through find_element
            for interaction in browser_interactions:
                if interaction.action == BrowserAction.CLICK or interaction.action == BrowserAction.HOVER:
                    bbox = self.find_element(interaction.action_param.desc, screenshot)
                    coordinates = center_bbox(bbox)
                    interaction.action_param.coordinates = coordinates

            return browser_interactions
        else:
            print(response.json())
            raise Exception(f"Failed to convert step to action: {step_description}")

    def is_task_complete(
        self,
        task_description: str,
        screenshot: Image.Image,
    ) -> bool:
        """
        Check if a task is complete based on a natural language description of the task.
        """
        return self.is_step_complete(task_description, screenshot)


    

