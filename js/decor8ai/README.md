# Decor8 AI Javascript SDK

## Table of Contents
- [Overview](#javascript-sdk-overview)
- [Installation](#installation)
- [Configuration](#configure-sdk)
- [Usage](#using-this-sdk)
  - [Design With Photo](#design-with-photo)
  - [Design Without Photo](#design-without-photo)
  - [Priming the walls](#prime-the-walls)
  - [Upscale the image](#upscale-the-image)
  - [Generate image captions](#image-caption-generator)
- [Design Styles](#design-styles)
- [Room Types](#room-types)
- [Color Schemes](#color-schemes)
- [Seasonal Décor](#speciality-decor)


## <a id="javascript-sdk-overview"></a>Overview

Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from 35+ interior design styles and 20+ room types to create unique interior design styles for your space.

The app specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

Equipped with a powerful Javascript SDK, Decor8 AI facilitates seamless integrations, enabling enhanced design generation capabilities directly within your Javascript environment. 

This documentation describes how you can use Decor8 AI Javascript SDK to integrate Decor8 AI's powerful features in your application. 

Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions.

## <a id="installation"></a>Installation

You can install the Decor8 AI Javascript SDK using pip:

```bash
npm install decor8ai
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

```javascript
const Decor8AI = require('decor8ai');
const fs = require('fs');
const path = require('path');

// Make sure DECOR8AI_API_KEY is set in your environment variables before running this script
const decor8 = new Decor8AI();

const input_image_path = 'path/to/your/room-photo.png';
const room_type = 'bedroom';
const design_style = 'farmhouse';
const num_images = 1;
const keep_original_dimensions = false; // Optional. true or false. If true, then generated designs have same dimensions as the original image. Although, it takes bit longer to generate the design. If false, generated designs have dimensions are chosen by the API.
const color_scheme = 'COLOR_SCHEME_4'; //Optional. 
const speciality_decor = 'SPECIALITY_DECOR_5'; // Optional. 

// Example using generateDesigns with a file path
console.log ("Generating designs for image at path " + input_image_path);
decor8.generateDesigns(input_image_path, room_type, design_style, null, num_images, keep_original_dimensions, color_scheme, speciality_decor)
    .then(response => {
        if (response.error) {
            console.error("An error occurred:", response.error);
        } else {

            //  The response is a JSON object containing the generated designs and other information.
            //  Sample response for successful design generation
            //  {
            //      "error": "",
            //      "message": "Successfully generated designs.",
            //      "info":
            //      {
            //          "images":
            //          [
            //              {
            //                  "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
            //                  "data": "<base64-encoded_data>",
            //                  "width": 768,
            //                  "height": 512,
            //                  "captions":
            //                  [
            //                      "Unveiling the art of rustic elegance in this French Country haven, where warmth and sophistication meet effortlessly."
            //                  ]
            //              }
            //          ]
            //      }
            //  }

            //  Sample response when unsuccessful. "error" will be non-empty value.
            //  {
            //      "error": "InvalidInput",
            //      "message": "Invalid input image. Please check the input image and try again.",
            //  }          
            console.log("Message:", response.message);
            const designs = response.info.images;
            designs.forEach((design, index) => {
                console.log(`Design ${index + 1}:`);
                console.log(`UUID: ${design.uuid}`);
                console.log(`Width: ${design.width}`);
                console.log(`Height: ${design.height}`);

                // If you want to save the image data as a file
                // Check if output-data directory exists, if not, create it
                const outputDir = path.join(__dirname, 'output-data');
                if (!fs.existsSync(outputDir)){
                    fs.mkdirSync(outputDir);
                }
                
                // Save the image data as a file in the output-data directory
                fs.writeFileSync(path.join(outputDir, `design_${design.uuid}.jpg`), design.data, 'base64', (err) => {
                    if (err) {
                        console.error("An error occurred while saving the image:", err);
                    } else {
                        console.log(`Image saved as design_${design.uuid}.jpg`);
                    }
                });
            });

        }
    })
    .catch(error => {
        console.error("An error occurred while generating designs:", error);
    });

```


## <a id="design-without-photo"> Generating Inspirational Interior Design Ideas without using a photo of the room

```Javascript
const Decor8AI = require('decor8ai');
const fs = require('fs');
const path = require('path');

// Make sure DECOR8AI_API_KEY is set in your environment variables before running this script
const decor8 = new Decor8AI();

const room_type = 'bedroom';
const design_style = 'farmhouse';
const num_images = 1;

// Example using generateDesigns with a file path
console.log ("Generating designs for image at path " + input_image_path);

// Note that input_image parameter is null. Decor8 AI server will generate a 
// new interior design for room_type and design_style.
decor8.generateDesigns(null, room_type, design_style, null, num_images)
```

## <a id="prime-the-walls">Priming the walls

If your room contains unfinished walls, unpainted walls or walls which need touch-up, use this API to get walls with basic white colored, smooth textured walls or as it's called 'primed walls'. 

You can use the returned image as input to generate_designs API for filling it with furniture. 

```Javascript
const Decor8AI = require('decor8ai');
const decor8 = new Decor8AI();

decor8.primeTheRoomWalls('/path_to_your_image.jpg')
    .then(response => console.log(response))
    .catch(error => console.error(error));

```

## <a id="upscale-the-image">Upscale the image
AI generated designs may have a smaller resolution for some use-cases. Use this API to get upto 4x the original resolution of the image. Original images of upto maximum 1024px width or height or both are supported. 

```Javascript
const Decor8AI = require('decor8ai');
const decor8 = new Decor8AI();

const input_image_path_for_upscaling = './sdk_upscale_this_image.jpg';
const scale_factor = 2;
decor8.upscaleImage(input_image_path_for_upscaling, scale_factor)
    .then(response => console.log(response))
    .catch(error => console.error(error));
```

## <a id="image-caption-generator">Generate captions for the interior image
If you need apt captions for an image depicting a specific interior design style in a room, use this API. 

```Javascript
const Decor8AI = require('decor8ai');
const decor8 = new Decor8AI();

room_type = 'livingroom'
design_style = 'frenchcountry'

decor8.generateImageCaptions(room_type, design_style, num_captions = 2)

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


