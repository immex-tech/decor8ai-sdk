# Decor8 AI SDK
Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from [35+ interior design styles](https://www.decor8.ai/ai-interior-design-styles) and [20+ room types](https://www.decor8.ai/ai-interior-design-room-types) to create unique interior design styles for your space.

The app specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

This documentation describes how you can use Decor8 AI Python SDK to integrate Decor8 AI's powerful features in your application. In addition to Python SDK, Decor8 AI also exposes simple HTTP based API for easy integration with language of your choice.

Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions.


## Table of Contents
- [Python SDK](#python-sdk)    
- [Javascript SDK](#javascript-sdk)
- [Flutter/Dart SDK](#dart-sdk)
- [HTTP](#http-api)
    - [Design With Photo](#http-api-design-with-photo)

# <a id="python-sdk">Python SDK
[Refer to Python SDK Readme](python/decor8ai/README.md)

# <a id="javascript-sdk">Javascript SDK
[Refer to Javascript SDK Readme](js/decor8ai/README.md)

# <a id="dart-sdk">Flutter/Dart SDK
[Refer to Dart SDK Readme](dart/decor8ai/README.md)

# <a id="http-api">HTTP

## <a id="http-api-design-with-photo">Generating Interior Design with a Photo of the room
```bash
# Variables
ROOM_TYPE="your_room_type"
DESIGN_STYLE="your_design_style"
NUM_IMAGES="1"
NUM_CAPTIONS="your_num_captions_value"  # Optional
INPUT_IMAGE_PATH="path/to/your/input/image.jpg"
TOKEN="your_decor8ai_api_key"
URL="https://prod-app.decor8.ai:8000/generate_designs"

# Base curl command
curl -X POST $URL \
     -H "Authorization: Bearer $TOKEN" \
     -F "room_type=$ROOM_TYPE" \
     -F "design_style=$DESIGN_STYLE" \
     -F "num_images=$NUM_IMAGES" \
     -F "input_image=@$INPUT_IMAGE_PATH"

# If you have num_captions
# -F "num_captions=$NUM_CAPTIONS" \

# If you have room_options_json
# -F "room_options_json=$ROOM_OPTIONS_JSON" \

```

## <a id="design-styles"> Supported Design Styles

Decor8 AI supports following design styles. Learn more about these styles at [Decor8 AI Decoration Styles](https://www.decor8.ai/ai-interior-design-styles)

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
Decor8 AI supports following room types. Learn more about these room types at [Decor8 AI Room Types](https://www.decor8.ai/ai-interior-design-room-types)

| **Room Type**  |               |               |               |
|----------------|---------------|---------------|---------------|
| livingroom     | kitchen       | diningroom    | bedroom       |
| bathroom       | kidsroom      | familyroom    | readingnook   |
| sunroom        | walkincloset  | mudroom       | toyroom       |
| office         | foyer         | powderroom    | laundryroom   |
| gym            | basement      | garage        | balcony       |
| cafe           | homebar       | study_room    | front_porch   |
| back_porch     | back_patio    |               |               |




