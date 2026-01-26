# Decor8 AI JavaScript SDK - AI Interior Design & Virtual Staging API

[![npm version](https://badge.fury.io/js/decor8ai.svg)](https://www.npmjs.com/package/decor8ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org)

The official JavaScript/Node.js SDK for **[Decor8 AI](https://www.decor8.ai)** - a powerful **AI interior design** and **AI virtual staging** platform. Build **AI room design** applications, **AI home decorations** tools, and **interior design by AI** services with ease.

## Features

- **AI Virtual Staging** - Transform empty rooms into beautifully furnished spaces
- **AI Interior Design** - Generate designs in 50+ styles for 25+ room types
- **AI Landscaping** - Create outdoor and garden designs (Beta)
- **AI Kitchen Remodeling** - Visualize kitchen renovations
- **AI Bathroom Remodeling** - Preview bathroom transformations
- **AI Wall Color Change** - Virtually repaint walls with any color
- **AI Cabinet Color Change** - Preview new cabinet finishes
- **AI Sky Replacement** - Enhance exterior photos with beautiful skies
- **Sketch to 3D Render** - Convert sketches into photorealistic renders
- **Object Removal** - Remove unwanted items from photos
- **Image Upscaling** - Enhance resolution up to 8x

## Installation

```bash
npm install decor8ai
```

**Requirements:** Node.js >= 18.0.0

## Configuration

Set your API key as an environment variable:

```bash
export DECOR8AI_API_KEY='your-api-key-here'
```

Get your API key at [Decor8 AI Platform](https://prod-app.decor8.ai).

## Quick Start

```javascript
const Decor8AI = require('decor8ai');
const client = new Decor8AI();

// AI Virtual Staging
const result = await client.generateDesignsForRoom({
    inputImageUrl: 'https://example.com/empty-room.jpg',
    roomType: 'livingroom',
    designStyle: 'modern',
    numImages: 2
});

console.log(result.info.images);
```

## Table of Contents

- [AI Virtual Staging](#ai-virtual-staging)
- [AI Interior Design (Inspirational)](#ai-interior-design-inspirational)
- [AI Wall Color Change](#ai-wall-color-change)
- [AI Cabinet Color Change](#ai-cabinet-color-change)
- [AI Kitchen Remodeling](#ai-kitchen-remodeling)
- [AI Bathroom Remodeling](#ai-bathroom-remodeling)
- [AI Landscaping](#ai-landscaping)
- [AI Sky Replacement](#ai-sky-replacement)
- [Sketch to 3D Render](#sketch-to-3d-render)
- [Object Removal](#object-removal)
- [Image Upscaling](#image-upscaling)
- [Wall Priming](#wall-priming)
- [Design Styles Reference](#design-styles-reference)
- [Room Types Reference](#room-types-reference)

---

## AI Virtual Staging

Transform empty rooms into beautifully furnished spaces using **AI virtual staging** technology.

### Using Room Type and Design Style

```javascript
const Decor8AI = require('decor8ai');
const client = new Decor8AI();

const result = await client.generateDesignsForRoom({
    inputImageUrl: 'https://example.com/empty-room.jpg',
    roomType: 'bedroom',
    designStyle: 'frenchcountry',
    numImages: 2,
    colorScheme: 'COLOR_SCHEME_5',
    specialityDecor: 'SPECIALITY_DECOR_2'  // Christmas decor
});
```

### Using Custom Prompt for AI Room Design

```javascript
const result = await client.generateDesignsForRoom({
    inputImageUrl: 'https://example.com/room.jpg',
    prompt: 'Modern minimalist room with sleek wardrobe, contemporary table lamps, and floating dresser',
    numImages: 2,
    guidanceScale: 15.0,
    numInferenceSteps: 50
});
```

### With Style Reference Image

```javascript
const result = await client.generateDesignsForRoom({
    inputImageUrl: 'https://example.com/room.jpg',
    roomType: 'livingroom',
    designStyle: 'modern',
    designStyleImageUrl: 'https://example.com/style-reference.jpg',
    designStyleImageStrength: 0.8,
    numImages: 1
});
```

---

## AI Interior Design (Inspirational)

Generate **AI interior design** concepts without an input image.

```javascript
// Using room type and style
const result = await client.generateInspirationalDesigns({
    roomType: 'bedroom',
    designStyle: 'scandinavian',
    numImages: 2
});

// Using custom prompt for AI room design
const result = await client.generateInspirationalDesigns({
    prompt: 'Luxurious master bedroom with ocean view and modern furniture',
    numImages: 2,
    guidanceScale: 15.0,
    seed: 42  // For reproducible results
});
```

---

## AI Wall Color Change

Virtually repaint walls with **AI home decorations** technology.

```javascript
const result = await client.changeWallColor(
    'https://example.com/room.jpg',
    '#4A90D9'  // Hex color code for the new wall color
);
```

---

## AI Cabinet Color Change

Preview new cabinet finishes with **AI kitchen design** capabilities.

```javascript
const result = await client.changeKitchenCabinetsColor(
    'https://example.com/kitchen.jpg',
    '#2C3E50'  // Hex color code for the new cabinet color
);
```

---

## AI Kitchen Remodeling

Visualize kitchen renovations using **AI interior design** technology.

```javascript
const result = await client.remodelKitchen(
    'https://example.com/kitchen.jpg',
    'modern',
    {
        numImages: 2,
        scaleFactor: 2
    }
);
```

---

## AI Bathroom Remodeling

Preview bathroom transformations with **AI home design** visualization.

```javascript
const result = await client.remodelBathroom(
    'https://example.com/bathroom.jpg',
    'contemporary',
    {
        numImages: 2,
        scaleFactor: 2
    }
);
```

---

## AI Landscaping

Generate **AI landscaping** designs for outdoor spaces (Beta).

```javascript
const result = await client.generateLandscapingDesigns(
    'https://example.com/yard.jpg',
    'Front Yard',       // 'Front Yard', 'Backyard', or 'Side Yard'
    'japanese_zen',     // Garden style
    { numImages: 2 }
);
```

### Garden Styles

| Style | Description |
|-------|-------------|
| japanese_zen | Tranquil Japanese garden design |
| english_cottage | Classic English garden aesthetic |
| mediterranean | Mediterranean-inspired landscaping |
| modern_minimalist | Clean, contemporary outdoor design |
| tropical | Lush tropical garden style |

---

## AI Sky Replacement

Enhance exterior property photos with beautiful skies.

```javascript
const result = await client.replaceSkyBehindHouse(
    'https://example.com/house-exterior.jpg',
    'dusk'  // 'day', 'dusk', or 'night'
);
```

---

## Sketch to 3D Render

Convert hand-drawn sketches into photorealistic **AI room design** renders.

```javascript
const result = await client.sketchTo3dRender(
    'https://example.com/floor-plan-sketch.jpg',
    'modern',
    {
        numImages: 2,
        scaleFactor: 2,
        renderType: 'perspective'  // 'perspective' or 'isometric'
    }
);
```

---

## Object Removal

Remove unwanted items from photos using **AI interior design** technology.

```javascript
// Auto-detect and remove objects
const result = await client.removeObjectsFromRoom(
    'https://example.com/cluttered-room.jpg'
);

// With custom mask for specific areas
const result = await client.removeObjectsFromRoom(
    'https://example.com/room.jpg',
    'https://example.com/mask.jpg'  // Black/white mask
);
```

---

## Image Upscaling

Enhance image resolution for professional **AI home decorations** output.

```javascript
// From URL
const result = await client.upscaleImage(
    'https://example.com/room.jpg',
    4  // Scale factor (1-8)
);

// From local file
const result = await client.upscaleImage(
    '/path/to/local/image.jpg',
    2
);
```

---

## Wall Priming

Prepare walls for **AI virtual staging** by applying uniform wall texture.

```javascript
const result = await client.primeWallsForRoom(
    'https://example.com/room-with-damaged-walls.jpg'
);
```

---

## Response Handling

All methods return a Promise with this structure:

```javascript
{
    "error": "",
    "message": "Successfully generated designs.",
    "info": {
        "images": [
            {
                "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
                "url": "https://generated-image-url.jpg",
                "width": 768,
                "height": 512,
                "captions": ["Modern minimalist bedroom..."]
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

function downloadImage(url, outputPath) {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            if (response.statusCode === 200) {
                const fileStream = fs.createWriteStream(outputPath);
                response.pipe(fileStream);
                fileStream.on('finish', () => {
                    fileStream.close();
                    resolve();
                });
            } else {
                reject(new Error(`Download failed: ${response.statusCode}`));
            }
        });
    });
}

// Usage
const result = await client.generateDesignsForRoom({...});
for (const image of result.info.images) {
    await downloadImage(image.url, `./output/${image.uuid}.jpg`);
}
```

---

## Design Styles Reference

50+ **AI interior design** styles available:

| **Styles**          |                    |                    |                    |
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

---

## Room Types Reference

25+ room types for **AI room design**:

| **Room Types**  |               |               |               |
|-----------------|---------------|---------------|---------------|
| livingroom      | kitchen       | diningroom    | bedroom       |
| bathroom        | kidsroom      | familyroom    | readingnook   |
| sunroom         | walkincloset  | mudroom       | toyroom       |
| office          | foyer         | powderroom    | laundryroom   |
| gym             | basement      | garage        | balcony       |
| cafe            | homebar       | study_room    | front_porch   |
| back_porch      | back_patio    |               |               |

---

## Links

- [Decor8 AI Platform](https://www.decor8.ai) - Get started with AI interior design
- [API Documentation](https://api-docs.decor8.ai/) - Complete API reference
- [API Playground](https://api-docs.decor8.ai/playground) - Try the API interactively
- [GitHub Repository](https://github.com/immex-tech/decor8ai-sdk) - SDK source code
- [npm Package](https://www.npmjs.com/package/decor8ai) - Package registry
- [Contact Support](mailto:decor8@immex.tech) - Questions or custom integrations

---

**Keywords:** AI Interior Design, AI Virtual Staging, AI Virtual Staging API, AI decorations, AI Home Decorations, AI room design, Interior design by AI, AI home design, virtual staging software, real estate virtual staging
