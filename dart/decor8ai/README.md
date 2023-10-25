# Decor8 AI Dart SDK

## Table of Contents
- [Overview](#dart-sdk-overview)
- [Installation](#installation)
- [Configuration](#configure-sdk)
- [Usage](#using-this-sdk)
  - [Design With Photo](#design-with-photo)
  - [Design Without Photo](#design-without-photo)
  - [Priming the walls](#prime-the-walls)
- [Design Styles](#design-styles)
- [Room Types](#room-types)


## <a id="dart-sdk-overview"></a>Overview

Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination. 

You can choose from 35+ interior design styles and 20+ room types to create unique interior design styles for your space.

The app specializes in virtual property staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability. 

Equipped with a powerful Dart SDK, Decor8 AI facilitates seamless integrations, enabling enhanced design generation capabilities directly within your Flutter/Dart apps. 

This documentation describes how you can use Decor8 AI Dart SDK to integrate Decor8 AI's powerful features in your application. 

Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions.

## <a id="installation"></a>Installation

Add 'decor8ai' package dependency in pubspec.yaml

```bash
dependencies:
  decor8ai: ^x.y.z
```

## <a id="configure-sdk"></a>Configure Decor8 AI API key

### Sign in to [Decor8 AI](https://prod-app.decor8.ai)

### Click on Profile Photo on Top Left

![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_1.jpg?raw=true)

### Click Generate API Key
![](https://github.com/immex-tech/decor8ai-sdk/blob/main/media/step_2.jpg?raw=true)

## <a id="design-with-photo"> Generating Interior Design with a Photo of the room

```Dart
  const decor8aiApiKey= '<DECOR8AI_API_KEY>'; // Get it from https://prod-app.decor8.ai -> Profile
  var decor8 = Decor8AI(decor8aiApiKey);

  // Example using generateDesigns with a file path
  // NOTE:keep input_image = null if you want Decor8 AI to generate a random design style for given room type
  // use num_captions = 1, 2 or 3 if you want to generate captions for the design images
  // use num_images = 1, 2, 3 ,or 4 if you want to generate multiple design images
  var generateDesignsResponse = await decor8.generateDesigns(
    'path/to/your/room/photo.png',
    'livingroom',
    'modern',
  );
  // Save generated image to local directory
  var designImages = generateDesignsResponse['info']['images'];
  for (var image in designImages) {
    var uuid = image['uuid'];
    var data = image['data'];

    var outputFile = File('output-data/$uuid.jpg');
    await outputFile.create(recursive: true); // This will create the directory if it does not exist
    await outputFile.writeAsBytes(base64Decode(data));
    print('Image saved: output-data/$uuid.jpg');
  }
```


## <a id="design-without-photo"> Generating Inspirational Interior Design Ideas without using a photo of the room

```Dart
const Decor8AI = require('decor8ai');
const fs = require('fs');
const path = require('path');

// Make sure DECOR8AI_API_KEY is set in your environment variables before running this script
const decor8 = new Decor8AI();

// Example using generateDesigns with a file path
console.log ("Generating designs for image at path " + input_image_path);

// Note that input_image parameter is null. Decor8 AI server will generate a 
// new interior design for room_type and design_style.
var generateDesignsResponse = await decor8.generateDesigns(
    null,
    'livingroom',
    'modern',
  );
  ```

## <a id="prime-the-walls">Priming the walls

If your room contains unfinished walls, unpainted walls or walls which need touch-up, use this API to get walls with basic white colored, smooth textured walls or as it's called 'primed walls'. 

You can use the returned image as input to generate_designs API for filling it with furniture. 

```Dart
  const decor8aiApiKey= '<DECOR8AI_API_KEY>'; // Get it from prod-app.decor8.ai -> Profile
  var decor8 = Decor8AI(decor8aiApiKey);

  // Example using primeTheRoomWalls with a file path
  // Priming operation applies white paint to the room walls. This is useful if the input image has dark walls or unfinished walls.
  var primeWallsResponse = await decor8.primeTheRoomWalls('path/to/your/image.jpg');

  // Save generated image to local directory
  var images = primeWallsResponse['info']['images'];
  for (var image in images) {
    var uuid = image['uuid'];
    var data = image['data'];

    var outputFile = File('output-data/$uuid.jpg');
    await outputFile.create(recursive: true); // This will create the directory if it does not exist
    await outputFile.writeAsBytes(base64Decode(data));
    print('Image saved: output-data/$uuid.jpg');
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


