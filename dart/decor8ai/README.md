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

See [complete documentation for Decor8 AI api for Virtual Staging and Interior Design](https://api-docs.decor8.ai/). Please reach out to [Decor8 AI Team](mailto:decor8@immex.tech) with questions or suggestions. 

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

  // Generate designs for input image's HTTP URL
  import 'dart:io';
  import 'dart:convert';
  import 'dart:async';
  import 'package:http/http.dart' as http;

  var generateDesignsResponse = await decor8.generateDesignsForRoom(
    'https://prod-files.decor8.ai/test-images/sdk_test_image.png',
    'livingroom',
    'modern',
  );

  var designImages = generateDesignsResponse['info']['images'];
  for (var image in designImages) {
    var uuid = image['uuid'];
    var url = image['url'];

    // Define the output file path
    var outputFile = File('output-data/$uuid.jpg');
    await outputFile.create(recursive: true); // This will create the directory if it does not exist

    // Fetch the image data from the URL
    var response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      // Write the bytes to the file
      await outputFile.writeAsBytes(response.bodyBytes);
      print('Image saved: output-data/$uuid.jpg');
    } else {
      print('Failed to download image: $url');
    }
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
  // Use primeWallsForRoom API if you're using http url for input_image
  // var primeWallsResponse = await decor8.primeWallsForRoom('https://prod-files.decor8.ai/test-images/sdk_test_image.png');

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

## Use Cases

### Mobile App Integration
- Perfect for Flutter-based real estate applications
- Ideal for mobile interior design apps
- Great for property management mobile solutions
- Excellent for home improvement retail apps

### Real Estate Virtual Staging
- Enable real-time virtual staging in your mobile app
- Allow users to visualize empty spaces with furniture
- Provide multiple design style options instantly
- Reduce the need for physical staging

### Interactive Design Services
- Build interactive design consultation apps
- Create virtual room planners
- Develop mobile-first design visualization tools
- Enable real-time design previews

### Business Solutions
- Add virtual staging to real estate photography services
- Create value-added services for property listings
- Enhance property marketing capabilities
- Develop custom design visualization solutions

Start integrating professional interior design capabilities into your Flutter applications today with Decor8 AI's Dart SDK. Whether you're building a real estate app, design tool, or business solution, our SDK provides the robust functionality you need.
