import 'package:decor8ai/decor8ai.dart';
import 'dart:convert';
import 'dart:io';

void main() async {
  const decor8aiApiKey= '<DECOR8AI_API_KEY>'; // Get it from prod-app.decor8.ai -> Profile
  var decor8 = Decor8AI(decor8aiApiKey);

  // Example using primeTheRoomWalls with a file path
  // Priming operation applies white paint to the room walls. This is useful if the input image has dark walls or unfinished walls.
  var primeWallsResponse = await decor8.primeTheRoomWalls('./test/sdk_prime_the_walls_image.jpg');

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

  // --------------------------------------------

  // Example using generateDesigns with a file path
  // NOTE:keep input_image = null if you want Decor8 AI to generate a random design style for given room type
  // use num_captions = 1, 2 or 3 if you want to generate captions for the design images
  // use num_images = 1, 2, 3 ,or 4 if you want to generate multiple design images
  var generateDesignsResponse = await decor8.generateDesigns(
    './test/sdk_test_image.jpg',
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
  
  // --------------------------------------------

  // Generate Random Design Image for specified room type and design style
  // Note that inputImage parameter is left to be null. 
  var randomDesignsResponse = await decor8.generateDesigns(
    null,
    'livingroom',
    'modern',
  );
  // Save generated image to local directory
  var randomDesigns = randomDesignsResponse['info']['images'];
  for (var image in randomDesigns) {
    var uuid = image['uuid'];
    var data = image['data'];

    var outputFile = File('output-data/$uuid.jpg');
    await outputFile.create(recursive: true); // This will create the directory if it does not exist
    await outputFile.writeAsBytes(base64Decode(data));
    print('Image saved: output-data/$uuid.jpg');
  }
}
