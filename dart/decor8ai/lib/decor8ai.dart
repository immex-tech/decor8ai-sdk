import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class Decor8AI {
  final String apiKey;
  final String baseUrl;

  Decor8AI(this.apiKey, {this.baseUrl = 'https://api.decor8.ai'});

  Future<Map<String, dynamic>> primeTheRoomWalls(String inputImage) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/prime_the_room_walls'),
    )
      ..headers.addAll({
        'Authorization': 'Bearer $apiKey',
      })
      ..files.add(
        await http.MultipartFile.fromPath('input_image', inputImage),
      );

    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    return json.decode(responseData);
  }

  Future<Map<String, dynamic>> primeWallsForRoom(String inputImageUrl) async {
    var url = Uri.parse('$baseUrl/prime_walls_for_room');
    
    var requestBody = {
      'input_image_url': inputImageUrl,
    };

    var response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode(requestBody),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to prime walls: ${response.body}');
    }
  }

  Future<Map<String, dynamic>> generateDesignsForRoom({
    required String input_image_url,
    String? room_type,
    String? design_style,
    int num_images = 1,
    String? color_scheme,
    String? speciality_decor,
    // Advanced parameters
    String? prompt,
    String? prompt_prefix,
    String? prompt_suffix,
    String? negative_prompt,
    int? seed,
    double? guidance_scale,
    int? num_inference_steps,
  }) async {
    var url = Uri.parse('$baseUrl/generate_designs_for_room');
    
    Map<String, dynamic> requestBody = {
      'input_image_url': input_image_url,
      'num_images': num_images,
    };

    // Add optional style parameters if provided
    if (room_type != null) requestBody['room_type'] = room_type;
    if (design_style != null) requestBody['design_style'] = design_style;
    if (color_scheme != null) requestBody['color_scheme'] = color_scheme;
    if (speciality_decor != null) requestBody['speciality_decor'] = speciality_decor;

    // Add advanced parameters if provided
    if (prompt != null) requestBody['prompt'] = prompt;
    if (prompt_prefix != null) requestBody['prompt_prefix'] = prompt_prefix;
    if (prompt_suffix != null) requestBody['prompt_suffix'] = prompt_suffix;
    if (negative_prompt != null) requestBody['negative_prompt'] = negative_prompt;
    if (seed != null) requestBody['seed'] = seed;
    if (guidance_scale != null) requestBody['guidance_scale'] = guidance_scale;
    if (num_inference_steps != null) requestBody['num_inference_steps'] = num_inference_steps;

    var response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode(requestBody),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to generate designs: ${response.body}');
    }
  }

  Future<Map<String, dynamic>> generateInspirationalDesigns({
    String? room_type,
    String? design_style,
    int num_images = 1,
    String? color_scheme,
    String? speciality_decor,
    // Advanced parameters
    String? prompt,
    String? prompt_prefix,
    String? prompt_suffix,
    String? negative_prompt,
    int? seed,
    double? guidance_scale,
    int? num_inference_steps,
  }) async {
    var url = Uri.parse('$baseUrl/generate_inspirational_designs');
    
    Map<String, dynamic> requestBody = {
      'num_images': num_images,
    };

    // Add optional style parameters if provided
    if (room_type != null) requestBody['room_type'] = room_type;
    if (design_style != null) requestBody['design_style'] = design_style;
    if (color_scheme != null) requestBody['color_scheme'] = color_scheme;
    if (speciality_decor != null) requestBody['speciality_decor'] = speciality_decor;

    // Add advanced parameters if provided
    if (prompt != null) requestBody['prompt'] = prompt;
    if (prompt_prefix != null) requestBody['prompt_prefix'] = prompt_prefix;
    if (prompt_suffix != null) requestBody['prompt_suffix'] = prompt_suffix;
    if (negative_prompt != null) requestBody['negative_prompt'] = negative_prompt;
    if (seed != null) requestBody['seed'] = seed;
    if (guidance_scale != null) requestBody['guidance_scale'] = guidance_scale;
    if (num_inference_steps != null) requestBody['num_inference_steps'] = num_inference_steps;

    var response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $apiKey',
        'Content-Type': 'application/json',
      },
      body: json.encode(requestBody),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to generate inspirational designs: ${response.body}');
    }
  }

  // Legacy method for backward compatibility
  Future<Map<String, dynamic>> generateDesigns(
    String? inputImage,
    String roomType,
    String designStyle, {
    int numImages = 1,
    String? colorScheme,
    String? specialityDecor,
    // Added advanced parameters
    String? prompt,
    String? promptPrefix,
    String? promptSuffix,
    String? negativePrompt,
    int? seed,
    double? guidanceScale,
    int? numInferenceSteps,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/generate_designs'),
    )
      ..headers.addAll({
        'Authorization': 'Bearer $apiKey',
      })
      ..fields.addAll({
        'room_type': roomType,
        'design_style': designStyle,
        'num_images': '$numImages',
        if (colorScheme != null) 'color_scheme': colorScheme,
        if (specialityDecor != null) 'speciality_decor': specialityDecor,
        // Added advanced parameters to fields
        if (prompt != null) 'prompt': prompt,
        if (promptPrefix != null) 'prompt_prefix': promptPrefix,
        if (promptSuffix != null) 'prompt_suffix': promptSuffix,
        if (negativePrompt != null) 'negative_prompt': negativePrompt,
        if (seed != null) 'seed': seed.toString(),
        if (guidanceScale != null) 'guidance_scale': guidanceScale.toString(),
        if (numInferenceSteps != null) 'num_inference_steps': numInferenceSteps.toString(),
      });

    if (inputImage != null) {
      request.files.add(
        await http.MultipartFile.fromPath('input_image', inputImage),
      );
    }

    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    return json.decode(responseData);
  }
}
