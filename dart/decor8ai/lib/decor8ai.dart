/// Decor8 AI SDK for Dart/Flutter
///
/// A comprehensive SDK for virtual staging, interior design generation,
/// landscaping, remodeling, and image processing.
///
/// Example:
/// ```dart
/// final client = Decor8AI('your-api-key');
/// final result = await client.generateDesignsForRoom(
///   inputImageUrl: 'https://example.com/room.jpg',
///   roomType: 'livingroom',
///   designStyle: 'modern',
/// );
/// ```
library decor8ai;

import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

/// Main client for Decor8 AI API
class Decor8AI {
  final String apiKey;
  final String baseUrl;

  /// Create a Decor8AI client
  ///
  /// [apiKey] - Your Decor8 AI API key
  /// [baseUrl] - API base URL (defaults to https://api.decor8.ai)
  Decor8AI(this.apiKey, {this.baseUrl = 'https://api.decor8.ai'});

  /// Get authorization headers
  Map<String, String> _getHeaders({bool isJson = true}) {
    final headers = {'Authorization': 'Bearer $apiKey'};
    if (isJson) {
      headers['Content-Type'] = 'application/json';
    }
    return headers;
  }

  /// Make a POST request with JSON payload
  Future<Map<String, dynamic>> _postJson(
      String endpoint, Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: _getHeaders(),
      body: json.encode(data),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Request failed: ${response.body}');
    }
  }

  /// Make a POST request with multipart form data
  Future<Map<String, dynamic>> _postMultipart(
    String endpoint,
    String filePath, {
    Map<String, String>? fields,
  }) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl$endpoint'),
    )
      ..headers.addAll(_getHeaders(isJson: false))
      ..files.add(await http.MultipartFile.fromPath('input_image', filePath));

    if (fields != null) {
      request.fields.addAll(fields);
    }

    final response = await request.send();
    final responseData = await response.stream.bytesToString();
    return json.decode(responseData);
  }

  // ===========================================================================
  // Virtual Staging & Design Generation
  // ===========================================================================

  /// Generate virtual staging designs for a room image
  ///
  /// [inputImageUrl] - URL of the input room image
  /// [roomType] - Type of room (e.g., 'livingroom', 'bedroom')
  /// [designStyle] - Design aesthetic (e.g., 'modern', 'scandinavian')
  /// [numImages] - Number of designs to generate (1-4)
  /// [scaleFactor] - Resolution multiplier (1-8)
  /// [colorScheme] - Predefined color palette
  /// [specialityDecor] - Seasonal/thematic decor
  /// [maskInfo] - Masking data from previous requests
  /// [prompt] - Custom text generation directive
  /// [seed] - Random seed for reproducibility
  /// [guidanceScale] - Prompt adherence (1-20, default 15)
  /// [numInferenceSteps] - Quality/speed balance (1-75, default 50)
  /// [designStyleImageUrl] - Style reference image URL
  /// [designStyleImageStrength] - Style influence (0-1, default 0.82)
  /// [designCreativity] - Creative alterations level (0-1, default 0.39)
  /// [webhooksData] - Async callback configuration
  /// [decorItems] - JSON string specifying furniture/accessories
  Future<Map<String, dynamic>> generateDesignsForRoom({
    required String inputImageUrl,
    required String roomType,
    required String designStyle,
    int numImages = 1,
    int? scaleFactor,
    String? colorScheme,
    String? specialityDecor,
    String? maskInfo,
    String? prompt,
    int? seed,
    double? guidanceScale,
    int? numInferenceSteps,
    String? designStyleImageUrl,
    double? designStyleImageStrength,
    double? designCreativity,
    String? webhooksData,
    String? decorItems,
  }) async {
    final Map<String, dynamic> payload = {
      'input_image_url': inputImageUrl,
      'room_type': roomType,
      'design_style': designStyle,
      'num_images': numImages,
    };

    if (scaleFactor != null) payload['scale_factor'] = scaleFactor;
    if (colorScheme != null) payload['color_scheme'] = colorScheme;
    if (specialityDecor != null) payload['speciality_decor'] = specialityDecor;
    if (maskInfo != null) payload['mask_info'] = maskInfo;
    if (prompt != null) payload['prompt'] = prompt;
    if (seed != null) payload['seed'] = seed;
    if (guidanceScale != null) payload['guidance_scale'] = guidanceScale;
    if (numInferenceSteps != null) payload['num_inference_steps'] = numInferenceSteps;
    if (designStyleImageUrl != null) payload['design_style_image_url'] = designStyleImageUrl;
    if (designStyleImageStrength != null) payload['design_style_image_strength'] = designStyleImageStrength;
    if (designCreativity != null) payload['design_creativity'] = designCreativity;
    if (webhooksData != null) payload['webhooks_data'] = webhooksData;
    if (decorItems != null) payload['decor_items'] = decorItems;

    return _postJson('/generate_designs_for_room', payload);
  }

  /// Generate inspirational room designs without an input image
  Future<Map<String, dynamic>> generateInspirationalDesigns({
    required String roomType,
    required String designStyle,
    int numImages = 1,
    String? colorScheme,
    String? specialityDecor,
    String? prompt,
    int? seed,
    double? guidanceScale,
    int? numInferenceSteps,
  }) async {
    final Map<String, dynamic> payload = {
      'room_type': roomType,
      'design_style': designStyle,
      'num_images': numImages,
    };

    if (colorScheme != null) payload['color_scheme'] = colorScheme;
    if (specialityDecor != null) payload['speciality_decor'] = specialityDecor;
    if (prompt != null) payload['prompt'] = prompt;
    if (seed != null) payload['seed'] = seed;
    if (guidanceScale != null) payload['guidance_scale'] = guidanceScale;
    if (numInferenceSteps != null) payload['num_inference_steps'] = numInferenceSteps;

    return _postJson('/generate_inspirational_designs', payload);
  }

  /// Generate designs using multipart file upload (legacy method)
  Future<Map<String, dynamic>> generateDesigns(
    String inputImage,
    String roomType,
    String designStyle, {
    int numImages = 1,
    String? colorScheme,
    String? specialityDecor,
    String? prompt,
    int? seed,
    double? guidanceScale,
    int? numInferenceSteps,
  }) async {
    final fields = {
      'room_type': roomType,
      'design_style': designStyle,
      'num_images': numImages.toString(),
      if (colorScheme != null) 'color_scheme': colorScheme,
      if (specialityDecor != null) 'speciality_decor': specialityDecor,
      if (prompt != null) 'prompt': prompt,
      if (seed != null) 'seed': seed.toString(),
      if (guidanceScale != null) 'guidance_scale': guidanceScale.toString(),
      if (numInferenceSteps != null) 'num_inference_steps': numInferenceSteps.toString(),
    };

    return _postMultipart('/generate_designs', inputImage, fields: fields);
  }

  // ===========================================================================
  // Wall & Surface Modifications
  // ===========================================================================

  /// Prime room walls for virtual staging from URL
  Future<Map<String, dynamic>> primeWallsForRoom(String inputImageUrl) async {
    return _postJson('/prime_walls_for_room', {'input_image_url': inputImageUrl});
  }

  /// Prime room walls using file upload (legacy method)
  Future<Map<String, dynamic>> primeTheRoomWalls(String inputImage) async {
    return _postMultipart('/prime_the_room_walls', inputImage);
  }

  /// Change the wall color in a room image
  ///
  /// [inputImageUrl] - URL of the room image
  /// [wallColorHexCode] - Desired wall color in hex format (e.g., '#FF5733')
  Future<Map<String, dynamic>> changeWallColor(
    String inputImageUrl,
    String wallColorHexCode,
  ) async {
    return _postJson('/change_wall_color', {
      'input_image_url': inputImageUrl,
      'wall_color_hex_code': wallColorHexCode,
    });
  }

  /// Change kitchen cabinet colors in an image
  ///
  /// [inputImageUrl] - URL of the kitchen image
  /// [cabinetColorHexCode] - Desired cabinet color in hex format
  Future<Map<String, dynamic>> changeKitchenCabinetsColor(
    String inputImageUrl,
    String cabinetColorHexCode,
  ) async {
    return _postJson('/change_kitchen_cabinets_color', {
      'input_image_url': inputImageUrl,
      'cabinet_color_hex_code': cabinetColorHexCode,
    });
  }

  // ===========================================================================
  // Remodeling
  // ===========================================================================

  /// Generate kitchen remodel designs
  ///
  /// [inputImageUrl] - URL of the current kitchen image
  /// [designStyle] - Design aesthetic for the remodel
  /// [numImages] - Number of designs to generate (1-4)
  /// [scaleFactor] - Resolution multiplier (1-4)
  Future<Map<String, dynamic>> remodelKitchen(
    String inputImageUrl,
    String designStyle, {
    int numImages = 1,
    int? scaleFactor,
  }) async {
    final Map<String, dynamic> payload = {
      'input_image_url': inputImageUrl,
      'design_style': designStyle,
    };

    if (numImages > 1) payload['num_images'] = numImages;
    if (scaleFactor != null) payload['scale_factor'] = scaleFactor;

    return _postJson('/remodel_kitchen', payload);
  }

  /// Generate bathroom remodel designs
  ///
  /// [inputImageUrl] - URL of the current bathroom image
  /// [designStyle] - Design aesthetic for the remodel
  /// [numImages] - Number of designs to generate (1-4)
  /// [scaleFactor] - Resolution multiplier (1-4)
  Future<Map<String, dynamic>> remodelBathroom(
    String inputImageUrl,
    String designStyle, {
    int numImages = 1,
    int? scaleFactor,
  }) async {
    final Map<String, dynamic> payload = {
      'input_image_url': inputImageUrl,
      'design_style': designStyle,
    };

    if (numImages > 1) payload['num_images'] = numImages;
    if (scaleFactor != null) payload['scale_factor'] = scaleFactor;

    return _postJson('/remodel_bathroom', payload);
  }

  // ===========================================================================
  // Exterior & Landscaping
  // ===========================================================================

  /// Replace the sky in an exterior property photo
  ///
  /// [inputImageUrl] - URL of the exterior image
  /// [skyType] - Type of sky ('day', 'dusk', or 'night')
  Future<Map<String, dynamic>> replaceSkyBehindHouse(
    String inputImageUrl,
    String skyType,
  ) async {
    return _postJson('/replace_sky_behind_house', {
      'input_image_url': inputImageUrl,
      'sky_type': skyType,
    });
  }

  /// Generate landscaping designs for a yard (Beta)
  ///
  /// [inputImageUrl] - URL of the yard image
  /// [yardType] - Type of yard ('Front Yard', 'Backyard', or 'Side Yard')
  /// [gardenStyle] - Garden design style (e.g., 'japanese_zen')
  /// [numImages] - Number of designs to generate (1-4)
  Future<Map<String, dynamic>> generateLandscapingDesigns(
    String inputImageUrl,
    String yardType,
    String gardenStyle, {
    int numImages = 1,
  }) async {
    final Map<String, dynamic> payload = {
      'input_image_url': inputImageUrl,
      'yard_type': yardType,
      'garden_style': gardenStyle,
    };

    if (numImages > 1) payload['num_images'] = numImages;

    return _postJson('/generate_landscaping_designs', payload);
  }

  // ===========================================================================
  // Image Processing
  // ===========================================================================

  /// Remove objects/furniture from a room image
  ///
  /// [inputImageUrl] - URL of the room image
  /// [maskImageUrl] - Optional black/white mask specifying areas to remove
  Future<Map<String, dynamic>> removeObjectsFromRoom(
    String inputImageUrl, {
    String? maskImageUrl,
  }) async {
    final Map<String, dynamic> payload = {'input_image_url': inputImageUrl};
    if (maskImageUrl != null) payload['mask_image_url'] = maskImageUrl;
    return _postJson('/remove_objects_from_room', payload);
  }

  /// Upscale an image to higher resolution
  ///
  /// [inputImage] - File path of the input image (max 4MB)
  /// [scaleFactor] - Resolution multiplier (1-8)
  Future<Map<String, dynamic>> upscaleImage(
    String inputImage, {
    int scaleFactor = 2,
  }) async {
    return _postMultipart(
      '/upscale_image',
      inputImage,
      fields: {'scale_factor': scaleFactor.toString()},
    );
  }

  // ===========================================================================
  // 3D & Rendering
  // ===========================================================================

  /// Convert a sketch or floor plan to a 3D rendered image
  ///
  /// [inputImageUrl] - URL of the sketch/floor plan image
  /// [designStyle] - Design aesthetic for the render
  /// [numImages] - Number of renders to generate (1-4)
  /// [scaleFactor] - Resolution multiplier (1-8)
  /// [renderType] - Render perspective ('perspective' or 'isometric')
  Future<Map<String, dynamic>> sketchTo3dRender(
    String inputImageUrl,
    String designStyle, {
    int numImages = 1,
    int? scaleFactor,
    String? renderType,
  }) async {
    final Map<String, dynamic> payload = {
      'input_image_url': inputImageUrl,
      'design_style': designStyle,
    };

    if (numImages > 1) payload['num_images'] = numImages;
    if (scaleFactor != null) payload['scale_factor'] = scaleFactor;
    if (renderType != null) payload['render_type'] = renderType;

    return _postJson('/sketch_to_3d_render', payload);
  }
}

// =============================================================================
// Constants
// =============================================================================

/// Room types supported by the API
const List<String> roomTypes = [
  'LIVINGROOM', 'KITCHEN', 'DININGROOM', 'BEDROOM', 'BATHROOM',
  'KIDSROOM', 'FAMILYROOM', 'READINGNOOK', 'SUNROOM', 'WALKINCLOSET',
  'MUDROOM', 'TOYROOM', 'OFFICE', 'FOYER', 'POWDERROOM', 'LAUNDRYROOM',
  'GYM', 'BASEMENT', 'GARAGE', 'BALCONY', 'CAFE', 'HOMEBAR',
  'STUDY_ROOM', 'FRONT_PORCH', 'BACK_PORCH', 'BACK_PATIO', 'OPENPLAN',
  'BOARDROOM', 'MEETINGROOM', 'OPENWORKSPACE', 'PRIVATEOFFICE'
];

/// Design styles supported by the API
const List<String> designStyles = [
  'MINIMALIST', 'SCANDINAVIAN', 'INDUSTRIAL', 'BOHO', 'TRADITIONAL',
  'ARTDECO', 'MIDCENTURYMODERN', 'COASTAL', 'TROPICAL', 'ECLECTIC',
  'CONTEMPORARY', 'FRENCHCOUNTRY', 'RUSTIC', 'SHABBYCHIC', 'VINTAGE',
  'COUNTRY', 'MODERN', 'ASIAN_ZEN', 'HOLLYWOODREGENCY', 'BAUHAUS',
  'MEDITERRANEAN', 'FARMHOUSE', 'VICTORIAN', 'GOTHIC', 'MOROCCAN',
  'SOUTHWESTERN', 'TRANSITIONAL', 'MAXIMALIST', 'ARABIC', 'JAPANDI',
  'RETROFUTURISM', 'ARTNOUVEAU', 'URBANMODERN', 'WABI_SABI',
  'GRANDMILLENNIAL', 'COASTALGRANDMOTHER', 'NEWTRADITIONAL', 'COTTAGECORE',
  'LUXEMODERN', 'HIGH_TECH', 'ORGANICMODERN', 'TUSCAN', 'CABIN',
  'DESERTMODERN', 'GLOBAL', 'INDUSTRIALCHIC', 'MODERNFARMHOUSE',
  'EUROPEANCLASSIC', 'NEOTRADITIONAL', 'WARMMINIMALIST'
];

/// Sky types for sky replacement
const List<String> skyTypes = ['DAY', 'DUSK', 'NIGHT'];

/// Yard types for landscaping
const List<String> yardTypes = ['FRONT_YARD', 'BACKYARD', 'SIDE_YARD'];

/// Garden styles for landscaping
const List<String> gardenStyles = [
  'JAPANESE_ZEN', 'MEDITERRANEAN', 'ENGLISH_COTTAGE', 'TROPICAL', 'DESERT',
  'MODERN_MINIMALIST', 'FRENCH_FORMAL', 'COASTAL', 'WOODLAND', 'PRAIRIE',
  'ROCK_GARDEN', 'WATER_GARDEN', 'HERB_GARDEN', 'CUTTING_GARDEN', 'POLLINATOR',
  'XERISCAPE', 'EDIBLE_LANDSCAPE', 'MOON_GARDEN', 'RAIN_GARDEN', 'SENSORY',
  'NATIVE_PLANT', 'COTTAGE_STYLE', 'FORMAL_PARTERRE', 'NATURALISTIC',
  'CONTEMPORARY', 'ASIAN_FUSION', 'RUSTIC_FARMHOUSE', 'URBAN_MODERN',
  'SUSTAINABLE', 'WILDLIFE_HABITAT', 'FOUR_SEASON'
];

/// Render types for sketch to 3D
const List<String> renderTypes = ['PERSPECTIVE', 'ISOMETRIC'];
