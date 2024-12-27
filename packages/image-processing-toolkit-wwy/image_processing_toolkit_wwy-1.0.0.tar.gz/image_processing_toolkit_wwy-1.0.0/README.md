# Image Processing Toolkit

A simple Python toolkit for basic image processing tasks including conversion, filtering, and analysis.

## Installation

```{bash}
pip install image_processing_toolkit
```
## Usage
```{python}
from image_processing_toolkit import convert_image_format, apply_filter, color_histogram

# Convert image format
convert_image_format('path/to/input.jpg', 'path/to/output.png', 'PNG')

# Apply filter
apply_filter('path/to/input.jpg', 'path/to/output.jpg', 'BLUR')

# Generate color histogram
histogram = color_histogram('path/to/image.jpg')
print(histogram)
```




