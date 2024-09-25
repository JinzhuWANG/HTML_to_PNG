import os
import re

from glob import glob
from tqdm.auto import tqdm
from PIL import Image, ImageDraw, ImageFont

# Get the list of PNG files
PNGs = glob('output/*.png')
font = ImageFont.load_default(size=75)

def write_text_to_png(png_file, text, font, show_text=True, color=(227, 64, 50)):
    # Open the image
    image = Image.open(png_file)
    
    # Check if the text should be added to the image
    if  show_text:
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        # Define the position for the text (bottom-right corner)
        text_position = (100, 120)  # Adjust as needed
        # Add text to the image
        draw.text(text_position, text, font=font, fill=color)  # White text
        
    # Save the modified image
    save_path = png_file.replace('\\', f'\\show_{text}_') if show_text else png_file.replace('\\', f'\\noshow_{text}_')
    image.save(save_path)
    


for png in tqdm(PNGs):
    for show_txt in [True, False]:
        # Extract the year from the PNG file name
        year = re.compile(r'(\d{4})').search(png).group(0)
        # Change the 2010 to 2020
        year = str(int(year) + 10)
        # Only need years in range(2020, 2051, 3)
        if int(year) not in range(2020, 2051, 3):
            continue
        # Add the year to the PNG image
        write_text_to_png(png, year, font, show_txt)

