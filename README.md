# Decor8 AI Python SDK

## Overview

The Decor8 AI Python SDK is a powerful tool to integrate and utilize Decor8 AI’s design generation capabilities seamlessly within your Python environment. With this SDK, you can easily generate designs by providing room images in various formats, specifying room types, design styles, and various other parameters.

## Installation

You can install the Decor8 AI Python SDK using pip:

```bash
pip install decor8ai
```

## Add Decor8 AI API key

Sign in to [Decor8 AI](https://prod-app.decor8.ai)

Click on Profile Photo on Top Left

![Navigate To Generate API Key] (media/step_1.jpg)

Click Generate API Key
![Generate API Key] (media/step_2.jpg)

```bash
export DECOR8AI_API_KEY='<YOUR_API_KEY>'
```

## Usage

```python
from decor8ai import generate_designs

# Generate designs
response = generate_designs(
    input_image='/path/to/your/image.jpg',  # Can be a file path, URL, or binary data
    room_type='livingroom',
    design_style='scandinavian',
    num_images=4
)

# The response is a JSON object containing the generated designs and other information.
```
