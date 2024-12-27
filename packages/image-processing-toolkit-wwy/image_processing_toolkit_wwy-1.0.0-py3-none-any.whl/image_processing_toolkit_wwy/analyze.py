# image_processing_toolkit/analyze.py
from PIL import Image
from collections import Counter

def color_histogram(image_path):
    """Generate a color histogram for an image."""
    with Image.open(image_path) as img:
        pixels = img.getdata()
        hist = Counter(pixels)
        return dict(hist)
