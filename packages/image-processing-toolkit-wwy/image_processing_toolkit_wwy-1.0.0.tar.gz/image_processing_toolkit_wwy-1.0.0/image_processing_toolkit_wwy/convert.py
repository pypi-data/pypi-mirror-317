# image_processing_toolkit/convert.py
from PIL import Image

def convert_image_format(image_path, output_path, format):
    """Convert an image to a different format."""
    with Image.open(image_path) as img:
        img.save(output_path, format=format)
