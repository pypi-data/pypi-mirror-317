from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from .enums import BrowserAction, BrowserInteraction, Text, WebElement, Duration
from typing import Optional, Dict, Any
from pathlib import Path
import tempfile
import time
from PIL import Image
import io
import os


class BrowserActor:
    def __init__(self, driver: Optional[Browser] = None, headless: Optional[bool] = True, record_video: Optional[bool] = False):
        if driver:
            self._browser = driver
            self._playwright = None  # We don't manage the playwright instance if driver is provided
        else:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=headless)
        
        self._recording_data = None
        self._screenshot_data = None
        
        # If recording is enabled, set up video recording
        if record_video:
            self._video_dir = Path(tempfile.mkdtemp())
            context_options = {
                "record_video_dir": str(self._video_dir),
                "record_video_size": {"width": 1280, "height": 720},
                "viewport": {"width": 1280, "height": 720}
            }
        else:
            self._video_dir = None
            context_options = {}
            
        self._context = self._browser.new_context(**context_options)
        self._page: Optional[Page] = None
        self._recording_saved = False

    @property
    def has_recording(self) -> bool:
        """Returns whether a recording is available"""
        return self._recording_data is not None

    @property
    def recording_data(self) -> Optional[bytes]:
        """Returns the cached recording data if available"""
        return self._recording_data

    @property
    def has_screenshot(self) -> bool:
        """Returns whether a screenshot is available"""
        return self._screenshot_data is not None

    @property
    def screenshot_data(self) -> Optional[bytes]:
        """Returns the cached screenshot data if available"""
        return self._screenshot_data

    def _capture_recording(self) -> None:
        """Internal method to capture the recording from the video file"""
        if self._video_dir:
            video_files = list(self._video_dir.glob('*.webm'))
            if video_files:
                with open(video_files[0], 'rb') as f:
                    self._recording_data = f.read()

    def take_screenshot(self, full_page: bool = False) -> Optional[Image.Image]:
        """
        Takes and returns a screenshot of the current page
        Args:
            full_page: If True, takes a screenshot of the full scrollable page
                      If False, takes a screenshot of the current viewport
        Returns:
            PIL Image of the screenshot if page is open, None otherwise
        """
        if self._page:
            screenshot_bytes = self._page.screenshot(full_page=full_page)
            return Image.open(io.BytesIO(screenshot_bytes))
        return None

    @property
    def page(self) -> Page:
        if self._page is None:
            self._page = self._context.new_page()
        return self._page

    def navigate_to_url(self, url: str) -> None:
        self.page.goto(url)

    def new_page(self) -> None:
        if self._page is not None:
            self._page.close()
        self._page = self._context.new_page()

    def close(self) -> None:
        """Clean up all browser resources and save recording if enabled"""
        if self._page:
            self._page.close()
        self._context.close()
        
        if self._video_dir:
            time.sleep(1)  # Give it a second to finish writing
            self._capture_recording()
            
            # Clean up video directory
            try:
                for file in self._video_dir.glob('*'):
                    file.unlink()
                self._video_dir.rmdir()
            except:
                pass
                
        # Only close browser and stop playwright if we created them
        if self._playwright:
            self._browser.close()
            self._playwright.stop()

    def execute(self, interaction: BrowserInteraction) -> None:
        """Execute a browser interaction"""
        if not interaction.validate():
            raise ValueError(f"Missing required data for action {interaction.action}")
            
        elif interaction.action == BrowserAction.CLICK:
            if isinstance(interaction.action_param, WebElement):
                print(f"Clicking on coordinates: {interaction.action_param.coordinates} {type(interaction.action_param.coordinates)}")
                self.page.mouse.click(*interaction.action_param.coordinates)
            
        elif interaction.action == BrowserAction.SCROLL:
            if isinstance(interaction.action_param, WebElement):
                self.page.mouse.wheel(0, interaction.action_param.coordinates[1])
            
        elif interaction.action == BrowserAction.TYPE:
            if isinstance(interaction.action_param, Text):
                self.page.keyboard.type(interaction.action_param.body)
            
        elif interaction.action == BrowserAction.HOVER:
            if isinstance(interaction.action_param, WebElement):
                self.page.mouse.move(*interaction.action_param.coordinates)
                # If there's a duration specified, wait that amount of time
                if hasattr(interaction.action_param, 'duration'):
                    self.page.wait_for_timeout(interaction.action_param.duration * 1000)
            
        elif interaction.action == BrowserAction.WAIT:
            if isinstance(interaction.action_param, Duration):
                self.page.wait_for_timeout(interaction.action_param.seconds * 1000)
                
    def save_recording(self, output_path: str) -> bool:
        """
        Saves the browser recording to the specified path if available.
        
        Args:
            output_path: Path where the recording should be saved
            
        Returns:
            bool: True if recording was saved successfully, False otherwise
        """
        if not output_path:
            print("Error: Output path cannot be empty")
            return False

        if not self.has_recording:
            print("Error: No recording data available")
            return False
        
        if self._recording_saved:
            print("Error: Recording was already saved")
            return False
    
        print(f"Saving recording to {output_path}")
        print(f"Recording data size: {len(self._recording_data) if self._recording_data else 0} bytes")
        
        try:
            directory = os.path.dirname(output_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(self._recording_data)
            self._recording_saved = True
            return True
        except Exception as e:
            print(f"Error saving recording: {e}")
            print(f"Current working directory: {os.getcwd()}")
            return False
                