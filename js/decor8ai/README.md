# Decor8 AI JavaScript SDK

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
  - [Room Design Generation](#room-design-generation)
  - [Inspirational Designs](#inspirational-designs)
  - [Wall Priming](#wall-priming)
  - [Image Captions](#image-captions)
  - [Image Upscaling](#image-upscaling)
- [Response Handling](#response-handling)
- [Parameters Reference](#parameters-reference)

## Installation

```bash
npm install decor8ai
```

## Configuration

Set your API key as an environment variable:
```bash
export DECOR8AI_API_KEY='your-api-key-here'
```

## Usage Examples

### Room Design Generation

#### Using Room Type and Style
```javascript
const Decor8AI = require('decor8ai');
const decor8 = new Decor8AI();

decor8.generateDesignsForRoom(
    'https://example.com/room.jpg',
    'bedroom',
    'frenchcountry',
    null,
    null,
    1,
    'COLOR_SCHEME_0',
    'SPECIALITY_DECOR_0'
)
.then(response => console.log(response))
.catch(error => console.error(error));
```

#### Using Custom Prompt with Advanced Parameters
```javascript
decor8.generateDesignsForRoom(
    'https://example.com/room.jpg',
    null,  // room_type not needed with custom prompt
    null,  // design_style not needed with custom prompt
    null,
    null,
    2,
    null,
    null,
    null,
    'Modern minimalist room with sleek wardrobe, contemporary Table Lamps, and floating Dresser',
    'high end, professional photo',
    'clean lines, ambient lighting',
    'cluttered, traditional, ornate',
    42,
    15.0,
    50
)
.then(response => console.log(response));
```

#### Using Simple Custom Prompt
```javascript
decor8.generateDesignsForRoom(
    'https://example.com/room.jpg',
    null,  // room_type not needed
    null,  // design_style not needed
    null,
    null,
    1,
    null,
    null,
    null,
    'Room with wardrobe, Table Lamps, Dresser',
    null,
    null,
    null,
    null,
    15.0
)
.then(response => console.log(response));
```

### Inspirational Designs

#### Using Room Type and Style
```javascript
decor8.generateInspirationalDesigns(
    'bedroom',
    'modern',
    2
)
.then(response => console.log(response));
```

#### Using Custom Prompt
```javascript
decor8.generateInspirationalDesigns(
    null,  // room_type not needed with custom prompt
    null,  // design_style not needed with custom prompt
    2,
    'Luxurious room with ocean view and modern furniture',
    'high end, professional photo',
    'natural lighting',
    'cluttered, dark',
    42,
    15.0,
    50
)
.then(response => console.log(response));
```

### Wall Priming
```javascript
decor8.primeWallsForRoom('https://example.com/room.jpg')
    .then(response => console.log(response));
```

### Image Captions
```javascript
decor8.generateImageCaptions('livingroom', 'modern', 2)
    .then(response => console.log(response));
```

### Image Upscaling
```javascript
decor8.upscaleImage('https://example.com/room.jpg', 2)
    .then(response => console.log(response));
```

## Response Handling

Example response structure:
```javascript
{
    "error": "",
    "message": "Successfully generated designs.",
    "info": {
        "images": [
            {
                "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
                "url": "https://example.com/image.jpg",
                "width": 768,
                "height": 512,
                "captions": [
                    "Modern minimalist bedroom with sleek furniture and ambient lighting"
                ]
            }
        ]
    }
}
```

### Saving Generated Images
```javascript
const fs = require('fs');
const https = require('https');
const path = require('path');

function downloadAndSaveImage(url, outputDir, filename) {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            if (response.statusCode === 200) {
                const fileStream = fs.createWriteStream(path.join(outputDir, filename));
                response.pipe(fileStream);
                fileStream.on('finish', () => {
                    fileStream.close();
                    resolve();
                });
            } else {
                reject(new Error(`Failed to download image: ${response.statusCode}`));
            }
        });
    });
}

// Usage in response handling
response.info.images.forEach((design, index) => {
    const filename = `design_${design.uuid}.jpg`;
    downloadAndSaveImage(design.url, './output', filename);
});
```

## Parameters Reference

### Common Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| input_image_url | string | URL of the input image |
| room_type | string | Type of room (e.g., 'bedroom', 'livingroom') |
| design_style | string | Design style (e.g., 'modern', 'frenchcountry') |
| num_images | number | Number of images to generate (default: 1) |
| prompt | string | Custom prompt describing desired outcome |
| prompt_prefix | string | Text to prepend to the prompt |
| prompt_suffix | string | Text to append to the prompt |
| negative_prompt | string | Things to avoid in generation |
| seed | number | Random seed for reproducible results |
| guidance_scale | number | Controls how closely to follow the prompt (default: 7.5) |
| num_inference_steps | number | Number of denoising steps (default: 30) |

### Additional Features
| Feature | Description |
|---------|-------------|
| color_scheme | Predefined color schemes (e.g., 'COLOR_SCHEME_0') |
| speciality_decor | Special decorative themes (e.g., 'SPECIALITY_DECOR_0') |
| scale_factor | Image scaling factor for output |


### Design Styles
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


For complete API documentation, visit [Decor8 AI API Documentation](https://api-docs.decor8.ai/)
