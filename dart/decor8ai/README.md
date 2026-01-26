# Decor8 AI Dart SDK - AI Interior Design & Virtual Staging API

[![pub version](https://img.shields.io/pub/v/decor8ai.svg)](https://pub.dev/packages/decor8ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dart SDK](https://img.shields.io/badge/Dart-%3E%3D3.0.0-blue)](https://dart.dev)

The official Dart/Flutter SDK for **[Decor8 AI](https://www.decor8.ai)** - a powerful **AI interior design** and **AI virtual staging** platform. Build mobile **AI room design** applications, **AI home decorations** tools, and **interior design by AI** services with Flutter.

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

Add the dependency to your `pubspec.yaml`:

```yaml
dependencies:
  decor8ai: ^2.0.0
```

Then run:

```bash
flutter pub get
```

**Requirements:** Dart SDK >= 3.0.0

## Configuration

Get your API key at [Decor8 AI Platform](https://prod-app.decor8.ai):

1. Sign in to [Decor8 AI](https://prod-app.decor8.ai)
2. Click on Profile Photo on Top Left
3. Click "Generate API Key"

![Step 1](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_1.jpg?raw=true)
![Step 2](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_2.jpg?raw=true)

## Quick Start

```dart
import 'package:decor8ai/decor8ai.dart';

final client = Decor8AI('your-api-key');

// AI Virtual Staging
final result = await client.generateDesignsForRoom(
  inputImageUrl: 'https://example.com/empty-room.jpg',
  roomType: 'LIVINGROOM',
  designStyle: 'MODERN',
  numImages: 2,
);

print(result['info']['images']);
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

```dart
import 'package:decor8ai/decor8ai.dart';

final client = Decor8AI('your-api-key');

final result = await client.generateDesignsForRoom(
  inputImageUrl: 'https://example.com/empty-room.jpg',
  roomType: 'BEDROOM',
  designStyle: 'FRENCHCOUNTRY',
  numImages: 2,
  colorScheme: 'COLOR_SCHEME_5',
  specialityDecor: 'SPECIALITY_DECOR_2',  // Christmas decor
);
```

### Using Custom Prompt for AI Room Design

```dart
final result = await client.generateDesignsForRoom(
  inputImageUrl: 'https://example.com/room.jpg',
  roomType: 'LIVINGROOM',
  designStyle: 'MODERN',
  prompt: 'Modern minimalist room with sleek wardrobe and contemporary table lamps',
  guidanceScale: 15.0,
  numInferenceSteps: 50,
);
```

### With Style Reference Image

```dart
final result = await client.generateDesignsForRoom(
  inputImageUrl: 'https://example.com/room.jpg',
  roomType: 'LIVINGROOM',
  designStyle: 'MODERN',
  designStyleImageUrl: 'https://example.com/style-reference.jpg',
  designStyleImageStrength: 0.8,
);
```

### Response Structure

```json
{
  "error": "",
  "message": "Successfully generated designs.",
  "info": {
    "images": [
      {
        "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
        "url": "https://generated-image-url.jpg",
        "width": 768,
        "height": 512
      }
    ]
  }
}
```

---

## AI Interior Design (Inspirational)

Generate **AI interior design** concepts without an input image.

```dart
// Using room type and style
final result = await client.generateInspirationalDesigns(
  roomType: 'BEDROOM',
  designStyle: 'SCANDINAVIAN',
  numImages: 2,
);

// Using custom prompt for AI room design
final result = await client.generateInspirationalDesigns(
  roomType: 'LIVINGROOM',
  designStyle: 'MODERN',
  prompt: 'Luxurious master bedroom with ocean view',
  guidanceScale: 15.0,
  seed: 42,  // For reproducible results
);
```

---

## AI Wall Color Change

Virtually repaint walls with **AI home decorations** technology.

```dart
final result = await client.changeWallColor(
  'https://example.com/room.jpg',
  '#4A90D9',  // Hex color code for the new wall color
);
```

---

## AI Cabinet Color Change

Preview new cabinet finishes with **AI kitchen design** capabilities.

```dart
final result = await client.changeKitchenCabinetsColor(
  'https://example.com/kitchen.jpg',
  '#2C3E50',  // Hex color code for the new cabinet color
);
```

---

## AI Kitchen Remodeling

Visualize kitchen renovations using **AI interior design** technology.

```dart
final result = await client.remodelKitchen(
  'https://example.com/kitchen.jpg',
  'MODERN',
  numImages: 2,
  scaleFactor: 2,
);
```

---

## AI Bathroom Remodeling

Preview bathroom transformations with **AI home design** visualization.

```dart
final result = await client.remodelBathroom(
  'https://example.com/bathroom.jpg',
  'CONTEMPORARY',
  numImages: 2,
  scaleFactor: 2,
);
```

---

## AI Landscaping

Generate **AI landscaping** designs for outdoor spaces (Beta).

```dart
final result = await client.generateLandscapingDesigns(
  'https://example.com/yard.jpg',
  'FRONT_YARD',       // 'FRONT_YARD', 'BACKYARD', or 'SIDE_YARD'
  'JAPANESE_ZEN',     // Garden style
  numImages: 2,
);
```

### Garden Styles

| Style | Description |
|-------|-------------|
| JAPANESE_ZEN | Tranquil Japanese garden design |
| ENGLISH_COTTAGE | Classic English garden aesthetic |
| MEDITERRANEAN | Mediterranean-inspired landscaping |
| MODERN_MINIMALIST | Clean, contemporary outdoor design |
| TROPICAL | Lush tropical garden style |

---

## AI Sky Replacement

Enhance exterior property photos with beautiful skies.

```dart
final result = await client.replaceSkyBehindHouse(
  'https://example.com/house-exterior.jpg',
  'DUSK',  // 'DAY', 'DUSK', or 'NIGHT'
);
```

---

## Sketch to 3D Render

Convert hand-drawn sketches into photorealistic **AI room design** renders.

```dart
final result = await client.sketchTo3dRender(
  'https://example.com/floor-plan-sketch.jpg',
  'MODERN',
  numImages: 2,
  scaleFactor: 2,
  renderType: 'PERSPECTIVE',  // 'PERSPECTIVE' or 'isometric'
);
```

---

## Object Removal

Remove unwanted items from photos using **AI interior design** technology.

```dart
// Auto-detect and remove objects
final result = await client.removeObjectsFromRoom(
  'https://example.com/cluttered-room.jpg',
);

// With custom mask for specific areas
final result = await client.removeObjectsFromRoom(
  'https://example.com/room.jpg',
  maskImageUrl: 'https://example.com/mask.jpg',
);
```

---

## Image Upscaling

Enhance image resolution for professional **AI home decorations** output.

```dart
final result = await client.upscaleImage(
  '/path/to/local/image.jpg',
  scaleFactor: 4,  // Scale factor (1-8)
);
```

---

## Wall Priming

Prepare walls for **AI virtual staging** by applying uniform wall texture.

```dart
// From URL
final result = await client.primeWallsForRoom(
  'https://example.com/room-with-damaged-walls.jpg',
);

// From local file
final result = await client.primeTheRoomWalls(
  '/path/to/local/image.jpg',
);
```

### Saving Generated Images

```dart
import 'dart:convert';
import 'dart:io';

// Save images from response
final images = result['info']['images'] as List;
for (var image in images) {
  if (image['data'] != null) {
    // Base64 encoded image (from multipart endpoints)
    final outputFile = File('output/${image['uuid']}.jpg');
    await outputFile.create(recursive: true);
    await outputFile.writeAsBytes(base64Decode(image['data']));
    print('Image saved: ${outputFile.path}');
  } else if (image['url'] != null) {
    // Download from URL (from JSON endpoints)
    print('Image URL: ${image['url']}');
  }
}
```

---

## Design Styles Reference

50+ **AI interior design** styles available:

| **Styles**          |                    |                    |                    |
|---------------------|--------------------|--------------------|-------------------|
| MINIMALIST          | SCANDINAVIAN       | INDUSTRIAL         | BOHO              |
| TRADITIONAL         | ARTDECO            | MIDCENTURYMODERN   | COASTAL           |
| TROPICAL            | ECLECTIC           | CONTEMPORARY       | FRENCHCOUNTRY     |
| RUSTIC              | SHABBYCHIC         | VINTAGE            | COUNTRY           |
| MODERN              | ASIAN_ZEN          | HOLLYWOODREGENCY   | BAUHAUS           |
| MEDITERRANEAN       | FARMHOUSE          | VICTORIAN          | GOTHIC            |
| MOROCCAN            | SOUTHWESTERN       | TRANSITIONAL       | MAXIMALIST        |
| ARABIC              | JAPANDI            | RETROFUTURISM      | ARTNOUVEAU        |
| URBANMODERN         | WABI_SABI          | GRANDMILLENNIAL    | COASTALGRANDMOTHER|
| NEWTRADITIONAL      | COTTAGECORE        | LUXEMODERN         | HIGH_TECH         |
| ORGANICMODERN       | TUSCAN             | CABIN              | DESERTMODERN      |
| GLOBAL              | INDUSTRIALCHIC     | MODERNFARMHOUSE    | EUROPEANCLASSIC   |
| NEOTRADITIONAL      | WARMMINIMALIST     |                    |                   |

Learn more at [Decor8 AI Decoration Styles](https://www.decor8.ai/interior-decoration-styles/)

---

## Room Types Reference

25+ room types for **AI room design**:

| **Room Types**  |               |               |               |
|-----------------|---------------|---------------|---------------|
| LIVINGROOM      | KITCHEN       | DININGROOM    | BEDROOM       |
| BATHROOM        | KIDSROOM      | FAMILYROOM    | READINGNOOK   |
| SUNROOM         | WALKINCLOSET  | MUDROOM       | TOYROOM       |
| OFFICE          | FOYER         | POWDERROOM    | LAUNDRYROOM   |
| GYM             | BASEMENT      | GARAGE        | BALCONY       |
| CAFE            | HOMEBAR       | STUDY_ROOM    | FRONT_PORCH   |
| BACK_PORCH      | BACK_PATIO    |               |               |

Learn more at [Decor8 AI Room Types](https://www.decor8.ai/rooms)

---

## Color Schemes

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

---

## Seasonal Decor

| Speciality Decor Value | Description                              |
|------------------------|------------------------------------------|
| SPECIALITY_DECOR_0     | None                                     |
| SPECIALITY_DECOR_1     | Halloween Decor                          |
| SPECIALITY_DECOR_2     | Christmas Decor                          |
| SPECIALITY_DECOR_3     | Thanksgiving Decor                       |
| SPECIALITY_DECOR_4     | Fall Season Decor                        |
| SPECIALITY_DECOR_5     | Spring Season Decor                      |
| SPECIALITY_DECOR_6     | Summer Season Decor                      |
| SPECIALITY_DECOR_7     | Winter Season Decor                      |

---

## Use Cases

### Mobile App Integration
- Perfect for Flutter-based **AI interior design** applications
- Ideal for mobile **AI virtual staging** apps
- Great for property management mobile solutions
- Excellent for home improvement retail apps

### Real Estate AI Virtual Staging
- Enable real-time **AI virtual staging** in your mobile app
- Allow users to visualize empty spaces with **AI room design**
- Provide multiple design style options instantly
- Reduce the need for physical staging

### AI Interior Design Services
- Build interactive **interior design by AI** consultation apps
- Create virtual **AI room design** planners
- Develop mobile-first **AI home decorations** visualization tools
- Enable real-time **AI interior design** previews

---

## Links

- [Decor8 AI Platform](https://www.decor8.ai) - Get started with AI interior design
- [API Documentation](https://api-docs.decor8.ai/) - Complete API reference
- [API Playground](https://api-docs.decor8.ai/playground) - Try the API interactively
- [GitHub Repository](https://github.com/immex-tech/decor8ai-sdk) - SDK source code
- [pub.dev Package](https://pub.dev/packages/decor8ai) - Package registry
- [Contact Support](mailto:decor8@immex.tech) - Questions or custom integrations

---

**Keywords:** AI Interior Design, AI Virtual Staging, AI Virtual Staging API, AI decorations, AI Home Decorations, AI room design, Interior design by AI, AI home design, Flutter virtual staging, Dart interior design SDK
