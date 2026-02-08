# Decor8 AI HTTP API

## Table of Contents
- [Overview](#api-overview)
- [Installation](#installation)
- [Configuration](#configure-sdk)
- [Usage](#using-this-sdk)
  - [Design With Photo](#design-with-photo)
  - [Design Without Photo](#design-without-photo)
  - [Priming the walls](#prime-the-walls)
  - [Upscale the image](#upscale-the-image)
- [Design Styles](#design-styles)
- [Room Types](#room-types)
- [Color Schemes](#color-schemes)
- [Seasonal Décor](#speciality-decor)
- [Use Cases](#use-cases)


Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from 50+ interior design styles and 25+ room types to create unique interior design styles for your space.

The app specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

Equipped with a powerful Python SDK, Decor8 AI facilitates seamless integrations, enabling enhanced design generation capabilities directly within your Python environment. Its user-friendly interface is optimized for performance on smaller screens, ensuring that your design process is as effortless and efficient as possible.

This documentation describes how you can use Decor8 AI http API to integrate Decor8 AI's powerful features in your application. 

See [complete documentation for Decor8 AI api for Virtual Staging and Interior Design](https://api-docs.decor8.ai/). Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions. 

## <a id="configure-sdk"></a>Configure Decor8 AI API key

### Sign in to [Decor8 AI](https://prod-app.decor8.ai)

### Click on Profile Photo on Top Left

![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_1.jpg?raw=true)

### Click Generate API Key
![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_2.jpg?raw=true)


## <a id="using-this-sdk">Usage

```bash
export DECOR8AI_API_KEY='<Your Decor8AI API Key>'
```

## <a id="design-with-photo"> Generating Interior Design with a Photo of the room

### Example 1: Using Room Type and Design Style
```bash
export ROOM_TYPE="livingroom"
export DESIGN_STYLE="minimalist"
export NUM_IMAGES="1"
export INPUT_IMAGE_URL="https://prod-files.decor8.ai/test-images/sdk_test_image.png"
export SERVER_URL="https://api.decor8.ai/generate_designs_for_room"
export COLOR_SCHEME="COLOR_SCHEME_5"
export SPECIALITY_DECOR="SPECIALITY_DECOR_5"

# Basic style-guided generation
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "input_image_url": "'$INPUT_IMAGE_URL'",
       "room_type": "'$ROOM_TYPE'",
       "design_style": "'$DESIGN_STYLE'",
       "num_images": '$NUM_IMAGES',
       "color_scheme": "'$COLOR_SCHEME'",
       "speciality_decor": "'$SPECIALITY_DECOR'"
     }'
```

### Example 2: Using Custom Prompt Only
```bash
export INPUT_IMAGE_URL="https://prod-files.decor8.ai/test-images/sdk_test_image.png"
export SERVER_URL="https://api.decor8.ai/generate_designs_for_room"

# Prompt-guided generation
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "input_image_url": "'$INPUT_IMAGE_URL'",
       "prompt": "A modern minimalist living space with Scandinavian influences, featuring clean lines, natural materials, and abundant natural light",
       "num_images": 1
     }'
```

### Example 3: Using Advanced Generation Controls
```bash
export INPUT_IMAGE_URL="https://prod-files.decor8.ai/test-images/sdk_test_image.png"
export SERVER_URL="https://api.decor8.ai/generate_designs_for_room"

# Advanced generation with style reference
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "input_image_url": "'$INPUT_IMAGE_URL'",
       "prompt": "A cozy reading nook with built-in bookshelves",
       "seed": 42,
       "guidance_scale": 15,
       "num_inference_steps": 50,
       "design_creativity": 0.5,
       "design_style_image_url": "https://example.com/style-reference.jpg",
       "design_style_image_strength": 0.8,
       "num_images": 1
     }'
```

The response is a JSON object containing the generated designs and other information:
```json
{
    "error": "",
    "message": "Successfully generated designs.",
    "info": {
        "images": [
            {
                "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
                "url": "http://<generated-image-path>",
                "width": 768,
                "height": 512
            }
        ]
    }
}
```

### Advanced Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seed` | integer | random | For reproducible results (≥ 0) |
| `guidance_scale` | integer | 15 | Controls prompt adherence (1-20) |
| `num_inference_steps` | integer | 50 | Number of denoising steps (1-75) |
| `design_creativity` | float | 0.39 | Controls creativity level (0-1) |
| `design_style_image_url` | string | null | Reference image URL for style guidance |
| `design_style_image_strength` | float | 0.82 | How strongly to follow reference (0-1) |
| `scale_factor` | integer | 2 | Output resolution multiplier (1-8) |
| `mask_info` | string | null | Masking information for targeted editing |
| `webhooks_data` | JSON string | null | Webhook URL for async notifications |
| `decor_items` | JSON string | null | Specific furniture/accessories to place |

## <a id="design-without-photo"> Generating Inspirational Interior Design Ideas without using a photo of the room

```bash
export ROOM_TYPE="livingroom"
export DESIGN_STYLE="minimalist"
export NUM_IMAGES="1"
export SERVER_URL="https://api.decor8.ai/generate_designs"
export COLOR_SCHEME="COLOR_SCHEME_5"
export SPECIALITY_DECOR="SPECIALITY_DECOR_5"

# Base curl command
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -F "room_type=$ROOM_TYPE" \
     -F "design_style=$DESIGN_STYLE" \
     -F "num_images=$NUM_IMAGES" \
     -F "color_scheme=@$COLOR_SCHEME" \
     -F "speciality_decor=@$SPECIALITY_DECOR" \
     -F "keep_original_dimensions=false"
```

## <a id="prime-the-walls">Priming the walls

```bash
export SERVER_URL="https://api.decor8.ai/prime_walls_for_room"
export INPUT_IMAGE_URL="https://prod-files.decor8.ai/test-images/sdk_test_image.png"

# Base curl command
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -F "input_image_url=@$INPUT_IMAGE_URL" \
```

## <a id="upscale-the-image">Upscale the image
AI generated designs may have a smaller resolution for some use-cases. Use this API to get upto 4x the original resolution of the image. Original images of upto maximum 1024px width or height or both are supported. 

```bash
export SERVER_URL="https://api.decor8.ai/upscale_image"
export INPUT_IMAGE_PATH="/path/to/your/input-image.png"
export SCALE_FACTOR=2

# Base curl command
curl -X POST $SERVER_URL \
     -H "Authorization: Bearer $DECOR8AI_API_KEY" \
     -F "input_image=@$INPUT_IMAGE_PATH" \
     -F "scale_factor=@$SCALE_FACTOR"

```


## <a id="design-styles"> Supported Design Styles

Decor8 AI supports following design styles. Learn more about these styles at [Decor8 AI Decoration Styles](https://www.decor8.ai/interior-decoration-styles/)

| **Design Styles**    |                    |                    |                    |
|---------------------|--------------------|--------------------|-------------------|
| minimalist          | scandinavian       | industrial         | boho              |
| traditional         | artdeco            | midcenturymodern   | coastal           |
| tropical            | eclectic           | contemporary       | frenchcountry     |
| rustic              | shabbychic         | vintage            | country           |
| modern              | asian_zen          | hollywoodregency   | bauhaus           |
| mediterranean       | farmhouse          | victorian          | gothic            |
| moroccan            | southwestern       | transitional       | maximalist        |
| arabic              | japandi            | retrofuturism      | artnouveau        |
| urbanmodern         | wabi_sabi          | grandmillennial    | coastalgrandmother|
| newtraditional      | cottagecore        | luxemodern         | high_tech         |
| organicmodern       | tuscan             | cabin              | desertmodern      |
| global              | industrialchic     | modernfarmhouse    | europeanclassic   |
| neotraditional      | warmminimalist     |                    |                   |

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
| back_porch     | back_patio    | openplan      | boardroom     |
| meetingroom    | openworkspace | privateoffice |               |


## <a id="color-schemes"> Supported Color Schemes
Decor8 AI supports following color schemes.

| Color Scheme Value | Description                 |
|--------------------|-----------------------------|
| COLOR_SCHEME_0     | Default                     |
| COLOR_SCHEME_1     | Moss Green, Tan, White      |
| COLOR_SCHEME_2     | Gray, Sand, Blue            |
| COLOR_SCHEME_3     | Hunter Green, Red           |
| COLOR_SCHEME_4     | White, Pops of Color        |
| COLOR_SCHEME_5     | Blue, Neon                  |
| COLOR_SCHEME_6     | Light Blue, Emerald         |
| COLOR_SCHEME_7     | Blue, Grass Green           |
| COLOR_SCHEME_8     | Blue, Beige                 |
| COLOR_SCHEME_9     | Gray, Brown                 |
| COLOR_SCHEME_10    | Black, Red                  |
| COLOR_SCHEME_11    | Gray-Green, White, Black    |
| COLOR_SCHEME_12    | Blue, Gray, Taupe           |
| COLOR_SCHEME_13    | Black, Navy                 |
| COLOR_SCHEME_14    | Emerald, Tan                |
| COLOR_SCHEME_15    | Forest Green, Light Gray    |
| COLOR_SCHEME_16    | Yellow, Gray                |
| COLOR_SCHEME_17    | Pink, Green                 |
| COLOR_SCHEME_18    | Blush Pink, Black           |
| COLOR_SCHEME_19    | Black, White                |
| COLOR_SCHEME_20    | Blue, White                 |

## <a id="speciality-decor"> Supported Seasonal / Special Décor
Decor8 AI supports following seasonal décor.

| Speciality Decor Value | Description                                                          |
|------------------------|----------------------------------------------------------------------|
| SPECIALITY_DECOR_0     | None                                                                 |
| SPECIALITY_DECOR_1     | Halloween Decor with Spooky Ambiance, Eerie Elements, Dark Colors, and Festive Accents |
| SPECIALITY_DECOR_2     | Christmas Decor with Christmas Tree, Ornaments, and Lights            |
| SPECIALITY_DECOR_3     | Thanksgiving Decor, Fall Season Decor                                 |
| SPECIALITY_DECOR_4     | Fall Season Decor                                                     |
| SPECIALITY_DECOR_5     | Spring Season Decor                                                   |
| SPECIALITY_DECOR_6     | Summer Season Decor                                                   |
| SPECIALITY_DECOR_7     | Winter Season Decor                                                   |

## <a id="use-cases"> Use Cases

### Universal Integration
- Compatible with any programming language or platform
- Perfect for custom implementations
- Ideal for legacy system integration
- Excellent for microservices architecture

### Real Estate Solutions
- Virtual staging for property listings
- Multiple design style visualization
- Empty space transformation
- Cost-effective staging alternatives

### Business Applications
- Virtual home staging services
- Photography service enhancement
- Property marketing platforms
- Interior design consultation tools

### Custom Implementations
- Web-based design tools
- Property management systems
- Real estate platforms
- E-commerce integration

The HTTP API provides maximum flexibility for integrating Decor8 AI's powerful virtual staging and interior design capabilities into any system or application. Whether you're building a custom solution or enhancing an existing platform, our API provides the foundation for professional design visualization.
