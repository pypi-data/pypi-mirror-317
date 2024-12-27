# image_processing_toolkit/filters.py
from PIL import Image, ImageFilter

def apply_filter(image_path, output_path, filter_type):
    """Apply a filter to an image."""
    with Image.open(image_path) as img:
        if filter_type == 'BLUR':
            filtered_img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            filtered_img = img.filter(ImageFilter.CONTOUR)
        # Add more filters as needed
        filtered_img.save(output_path)
