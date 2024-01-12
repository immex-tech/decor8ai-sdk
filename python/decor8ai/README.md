# Decor8 AI Python SDK

## Table of Contents
- [Overview](#python-sdk-overview)
- [Installation](#installation)
- [Configuration](#configure-sdk)
- [Usage](#using-this-sdk)
  - [Design With Photo](#design-with-photo)
  - [Design Without Photo](#design-without-photo)
  - [Priming the walls](#prime-the-walls)
  - [Upscale the image](#upscale-the-image)
  - [Generate Captions for the image](#generate-captions-for-the-interior-image)
- [Design Styles](#design-styles)
- [Room Types](#room-types)


Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from 35+ interior design styles and 20+ room types to create unique interior design styles for your space.

The app specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

Equipped with a powerful Python SDK, Decor8 AI facilitates seamless integrations, enabling enhanced design generation capabilities directly within your Python environment. Its user-friendly interface is optimized for performance on smaller screens, ensuring that your design process is as effortless and efficient as possible.

This documentation describes how you can use Decor8 AI Python SDK to integrate Decor8 AI's powerful features in your application. 

Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions.

## <a id="installation"></a>Installation

You can install the Decor8 AI Python SDK using pip:

```bash
pip install decor8ai
```

## <a id="configure-sdk"></a>Configure Decor8 AI API key

### Sign in to [Decor8 AI](https://prod-app.decor8.ai)

### Click on Profile Photo on Top Left

![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_1.jpg?raw=true)

### Click Generate API Key
![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_2.jpg?raw=true)


## <a id="using-this-sdk">Usage

```bash
export DECOR8AI_API_KEY='<YOUR_API_KEY>'
```

## <a id="design-with-photo"> Generating Interior Design with a Photo of the room

```python
from decor8ai.client import generate_designs

# Mandatory Parameters
input_image = 'path/to/your/image.png'  #local-file-path or URL or bytes
room_type = 'livingroom' # See below for all supported room types
design_style = 'frenchcountry' # See below for all supported design Styles
num_images = 1 # Up to 4 images can be generated at a time

# Optional Parameters
num_captions = None # Choose 1 or 2 for number of image captions to generate
keep_original_dimensions = False # True or False. Generated designs retain original image's dimensions (and aspect ratio)

response_json = generate_designs(input_image=input_image, room_type=room_type, design_style=design_style, num_images=num_images, num_captions=1, keep_original_dimensions=True)

```

```
The response is a JSON object containing the generated designs and other information.

Sample response for successful design generation

{
    "error": "",
    "message": "Successfully generated designs.",
    "info":
    {
        "images":
        [
            {
                "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
                "data": "<base64-encoded_data>",
                "width": 768,
                "height": 512,
                "captions":
                [
                    "Unveiling the art of rustic elegance in this French Country haven, where warmth and sophistication meet effortlessly."
                ]
            }
        ]
    }
}

Sample response when unsuccessful. "error" will be non-empty value.
{
    "error": "InvalidInput",
    "message": "Invalid input image. Please check the input image and try again.",
}
```


## <a id="design-without-photo"> Generating Inspirational Interior Design Ideas without using a photo of the room

```Python
from decor8ai.client import generate_designs

# Here, we don't provide input image. The API generates a new interior design using following parameters.
room_type = 'livingroom' # See below for all supported room types
design_style = 'frenchcountry' # See below for all supported design Styles
num_images = 1 # Up to 4 images can be generated at a time

# Optional Parameters
num_captions = None # Choose 1 or 2 for number of image captions to generate

response_json = generate_designs(room_type=room_type, design_style=design_style, num_images=num_images, num_captions=1)
```

## <a id="prime-the-walls">Priming the walls

If your room contains unfinished walls, unpainted walls or walls which need touch-up, use this API to get walls with basic white colored, smooth textured walls or as it's called 'primed walls'. 

You can use the returned image as input to generate_designs API for filling it with furniture. 

```Python
from decor8ai.client import prime_the_room_walls

input_image = 'path/to/your/image.png'  #local-file-path or URL or bytes
response_json = prime_the_room_walls(input_image=input_image)

```
## <a id="upscale-the-image">Upscale the image
AI generated designs may have a smaller resolution for some use-cases. Use this API to get upto 4x the original resolution of the image. Original images of upto maximum 1024px width or height or both are supported. 

```Python
from decor8ai.client import upscale_image

input_image = 'path/to/your/image.png'  #local-file-path or URL or bytes
scale_factor = 2

response = upscale_image(input_image, scale_factor)
```

## <a id="image-caption-generator">Generate captions for the interior image
If you need apt captions for an image depicting a specific interior design style in a room, use this API. 

```Python
from decor8ai.client import generate_image_captions

room_type = 'livingroom'
design_style = 'frenchcountry'
num_captions = 2

response = generate_image_captions(room_type, design_style, num_captions)

```

```Text
Sample output

{
    "error": "",
    "message": "Successfully generated image captions.",
    "info":
    {
        "captions":
        [
            "\"Enchanting French Country Charm: Where cozy meets elegance in the heart of the living room.\"",
            "\"Step into a Parisian dream - where charm, elegance, and comfort seamlessly blend in this enchanting French country living room retreat. Get ready to indulge in rustic sophistication and let the cozy embrace of timeless design whisk you away to provincial bliss.\""
        ]
    }
}
```

## <a id="design-styles"> Supported Design Styles

Decor8 AI supports following design styles. Learn more about these styles at [Decor8 AI Decoration Styles](https://www.decor8.ai/interior-decoration-styles/)

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

## <a id="room-types"> Supported Room Types
Decor8 AI supports following room types. Learn more about these room types at [Decor8 AI Room Types](https://www.decor8.ai/rooms)

| **Room Type**  |               |               |               |
|----------------|---------------|---------------|---------------|
| livingroom     | kitchen       | diningroom    | bedroom       |
| bathroom       | kidsroom      | familyroom    | readingnook   |
| sunroom        | walkincloset  | mudroom       | toyroom       |
| office         | foyer         | powderroom    | laundryroom   |
| gym            | basement      | garage        | balcony       |
| cafe           | homebar       | study_room    | front_porch   |
| back_porch     | back_patio    |               |               |
