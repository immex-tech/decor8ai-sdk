# Decor8 AI Python SDK

## Overview

The Decor8 AI Python SDK is a powerful tool to integrate and utilize Decor8 AI’s design generation capabilities seamlessly within your Python environment. With this SDK, you can easily generate designs by providing room images in various formats, specifying room types, design styles, and various other parameters.

## Installation

You can install the Decor8 AI Python SDK using pip:

```bash
pip install decor8ai
```

## Usage

```python
from decor8ai import generate_designs

# Set the Decor8 AI API key in your environment
import os
os.environ['DECOR8AI_API_KEY'] = '<YOUR_API_KEY>'

# Generate designs
response = generate_designs(
    input_image='/path/to/your/image.jpg',  # Can be a file path, URL, or binary data
    room_type='livingroom',
    design_style='scandinavian',
    num_images=4
)

# The response is a JSON object containing the generated designs and other information.
