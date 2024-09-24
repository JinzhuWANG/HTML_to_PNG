import io
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from glob import glob
from tqdm.auto import tqdm

# Create Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
# Initialize the WebDriver (Chrome) with options
driver = webdriver.Chrome(options=options)
# Set the window size to capture the full page
driver.set_window_size(1920, 1080)




def save_html_as_image(html_file, output_image_path):
    # Open the HTML file
    driver.get("file://" + html_file)
    time.sleep(0.2)
    
    # Create an ActionChains object
    actions = ActionChains(driver)
    # Locate the element with the specified class
    element = driver.find_element(By.CLASS_NAME, "leaflet-image-layer.leaflet-zoom-animated.leaflet-interactive")
    # Move to the element, click and hold, then move by offset
    actions.move_to_element(element).click_and_hold().move_by_offset(0, -20).release().perform()

    # Give the page time to load
    time.sleep(0.2)
    # Take screenshot and save
    screenshot = driver.get_screenshot_as_png()
    # Open the image with Pillow
    image = Image.open(io.BytesIO(screenshot))
    # Save the image as a static file
    image.save(output_image_path)



# Find all HTML files and convert to absolute paths
html_files = [os.path.abspath(file) for file in glob('htmls/*.html')]
for html_file in tqdm(html_files):
    f_name = os.path.basename(html_file)
    save_name = f_name.replace('.html', '.png')
    save_html_as_image(html_file, f'output/{save_name}')

# Close the driver after processing
driver.quit()



