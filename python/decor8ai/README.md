# Decor8 AI Python SDK

## Overview

The Decor8 AI Python SDK is a powerful tool to integrate and utilize Decor8 AI’s design generation capabilities seamlessly within your Python environment. With this SDK, you can easily generate designs by providing room images in various formats, specifying room types, design styles, and various other parameters.

## Installation

You can install the Decor8 AI Python SDK using pip:

```bash
pip install decor8ai
```

## Configure Decor8 AI API key

### Sign in to [Decor8 AI](https://prod-app.decor8.ai)

### Click on Profile Photo on Top Left

![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_1.jpg?raw=true)

### Click Generate API Key
![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_2.jpg?raw=true)


## Usage

```bash
export DECOR8AI_API_KEY='<YOUR_API_KEY>'
```

```python
from decor8ai.client import generate_designs

# Mandatory Parameters
input_image = 'path/to/your/image.png'  #local-file-path or URL or bytes
room_type = 'livingroom' # See below for all supported room types
design_style = 'frenchcountry' # See below for all supported design Styles
num_images = 1 # Up to 4 images can be generated at a time

# Optional Parameters
num_captions = None # Choose 1 or 2 for number of image captions to generate

response_json = generate_designs(input_image=input_image, room_type=room_type, design_style=design_style, num_images=num_images, num_captions=1)

# The response is a JSON object containing the generated designs and other information.
# Sample response for successful design generation
# {
#     "error": "",
#     "message": "Successfully generated designs.",
#     "info":
#     {
#         "images":
#         [
#             {
#                 "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
#                 "data": "<base64-encoded_data>",
#                 "width": 768,
#                 "height": 512,
#                 "captions":
#                 [
#                     "Unveiling the art of rustic elegance in this French Country haven, where warmth and sophistication meet effortlessly."
#                 ]
#             }
#         ]
#     }
# }

# Sample response when unsuccessful. "error" will be non-empty value.
# {
#     "error": "InvalidInput",
#     "message": "Invalid input image. Please check the input image and try again.",
# }

```

## Supported Design Styles

| **Design Styles**           |                    |                    |                    |
|---------------------|--------------------|--------------------|--------------------|
| minimalist          | scandinavian       | industrial         | boho               |
| traditional         | artdeco            | midcenturymodern   | coastal            |
| tropical            | eclectic           | contemporary       | frenchcountry      |
| rustic              | shabbychic         | vintage            | country            |
| modern              | asian_zen          | hollywoodregency   | bauhaus            |
| mediterranean       | farmhouse          | victorian          | gothic             |
| moroccan            | southwestern       | transitional       | maximalist         |
| arabic              | japandi            | retrofuturism      | artnouveau         |

## Supported Room Types

| **Room Type**  |               |               |               |
|----------------|---------------|---------------|---------------|
| livingroom     | kitchen       | diningroom    | bedroom       |
| bathroom       | kidsroom      | familyroom    | readingnook   |
| sunroom        | walkincloset  | mudroom       | toyroom       |
| office         | foyer         | powderroom    | laundryroom   |
| gym            | basement      | garage        | balcony       |
| cafe           | homebar       | study_room    | front_porch   |
| back_porch     | back_patio    |               |               |


