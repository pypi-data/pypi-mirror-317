import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simplex import Simplex

from PIL import Image
import time

from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    
    image = "/home/ubuntu/supreme-waffle/images/dark_mode.png"
    screenshot = Image.open(image)

    start_time = time.time()
    bbox = simplex.find_element("dark mode icon", screenshot)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    print(bbox)
