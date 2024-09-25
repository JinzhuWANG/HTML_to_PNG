import io
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from glob import glob
from tqdm.auto import tqdm
from joblib import Parallel, delayed

# Create Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
# Initialize the WebDriver (Chrome) with options
driver = webdriver.Chrome(options=options)
# Set the window size to capture the full page
driver.set_window_size(1300, 1024)



def save_html_as_image(html_file, output_image_path, legend=False):
    # Open the HTML file
    driver.get("file://" + html_file)
    time.sleep(0.2)
    
    # Remove the element with ID 'legend'
    if not legend:
        driver.execute_script("document.getElementById('legend').remove();")
    
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    
    # Expand the layers control
    layers_toggle_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-control-layers-toggle")))
    actions.move_to_element(layers_toggle_button).perform()
    
    # Click the layers control
    osm_radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()[contains(., 'openstreetmap')]]/preceding-sibling::input[@type='radio']")))
    osm_radio_button.click()

    # Move to the element, click and hold, then move by offset
    element = driver.find_element(By.CLASS_NAME, "leaflet-image-layer.leaflet-zoom-animated.leaflet-interactive")
    actions.move_to_element(element).click_and_hold().move_by_offset(40, -40).release().perform()

    # Take screenshot and save
    screenshot = driver.get_screenshot_as_png()
    # Open the image with Pillow
    image = Image.open(io.BytesIO(screenshot))
    # Save the image as a static file
    image.save(output_image_path)



# Find all HTML files and convert to absolute paths
html_files = [os.path.abspath(file) for file in glob('htmls/*.html')]

for html_file in tqdm(html_files):
    for lgd in [True, False]:
        f_name = os.path.basename(html_file)
        save_name = f_name.replace('.html', '_with_legend.png') if lgd else f_name.replace('.html', '_no_legend.png')
        save_html_as_image(html_file, f'output/{save_name}', lgd)

# Close the driver after processing
driver.quit()



