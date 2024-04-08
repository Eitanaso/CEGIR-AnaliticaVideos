from PIL import Image
import pyscreenshot as ImageGrab
import numpy as np

# Define the coordinates of the region to capture: (x1, y1, x2, y2)
bbox = (100, 100, 500, 500)

# Capture a specific region
region_screenshot = ImageGrab.grab()#bbox=bbox)
print(type(region_screenshot))

region_screenshot.show()

region_screenshot.save('region_screenshot.png')