import 'package:decor8ai/decor8ai.dart';
import 'package:test/test.dart';
import 'dart:io';

void main() async {
  // Read the API key from environment variable
  final decor8aiApiKey = Platform.environment['DECOR8AI_API_KEY'];
  
  if (decor8aiApiKey == null || decor8aiApiKey.isEmpty) {
    throw Exception('DECOR8AI_API_KEY environment variable is not set');
  }
  
  final testImageUrl = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png';

  group('Decor8AI generateDesignsForRoom', () {
    test('Test 1: Original parameter usage', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var response = await decor8.generateDesignsForRoom(
        input_image_url: testImageUrl,
        room_type: 'bedroom',
        design_style: 'frenchcountry',
        num_images: 1,
        color_scheme: 'COLOR_SCHEME_0',
        speciality_decor: 'SPECIALITY_DECOR_0',
      );
      
      expect(response['error'], isEmpty);
      expect(response['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));

    test('Test 2: New parameters usage', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var response = await decor8.generateDesignsForRoom(
        input_image_url: testImageUrl,
        num_images: 1,
        prompt: 'A luxurious bedroom with ocean view',
        prompt_prefix: 'high end, professional photo',
        prompt_suffix: 'natural lighting, detailed textures',
        negative_prompt: 'cluttered, dark, cartoon',
        seed: 42,
        guidance_scale: 15.0,
        num_inference_steps: 50,
      );
      
      expect(response['error'], isEmpty);
      expect(response['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));

    test('Test 3: Custom prompt with some standard parameters', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var response = await decor8.generateDesignsForRoom(
        input_image_url: testImageUrl,
        num_images: 1,
        prompt: 'A cozy reading nook with built-in bookshelves',
        guidance_scale: 15.0,
      );
      
      expect(response['error'], isEmpty);
      expect(response['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));
  });

  // Legacy API tests
  group('Legacy APIs', () {
    test('generateDesigns', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var response = await decor8.generateDesigns(
        './test/sdk_test_image.jpg',
        'livingroom',
        'modern',
      );
      
      expect(response['error'], isEmpty);
      expect(response['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));

    test('primeTheRoomWalls', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var response = await decor8.primeTheRoomWalls('./test/sdk_prime_the_walls_image.jpg');
      expect(response['error'], isEmpty);
      expect(response['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));
  });
}
