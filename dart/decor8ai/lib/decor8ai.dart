import 'dart:convert';
import 'package:http/http.dart' as http;

class Decor8AI {
  final String apiKey;

  Decor8AI(this.apiKey);

  Future<Map<String, dynamic>> primeTheRoomWalls(String inputImage) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('https://api.decor8.ai/prime_the_room_walls'),
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
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('https://api.decor8.ai/prime_walls_for_room'),
    )
      ..headers.addAll({
        'Authorization': 'Bearer $apiKey',
      })
      ..files.add(
        await http.MultipartFile.fromPath('input_image_url', inputImageUrl),
      );

    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    return json.decode(responseData);
  }  

  Future<Map<String, dynamic>> generateDesigns(
    String? inputImage,
    String roomType,
    String designStyle, {
    int? numCaptions,
    int numImages = 1,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('https://api.decor8.ai/generate_designs'),
    )
      ..headers.addAll({
        'Authorization': 'Bearer $apiKey',
      })
      ..fields.addAll({
        'room_type': roomType,
        'design_style': designStyle,
        'num_images': '$numImages',
        if (numCaptions != null) 'num_captions': '$numCaptions',
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

    Future<Map<String, dynamic>> generateDesignsForRoom(
    String? inputImageUrl,
    String roomType,
    String designStyle, {
    int numImages = 1,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('https://api.decor8.ai/generate_designs_for_room'),
    )
      ..headers.addAll({
        'Authorization': 'Bearer $apiKey',
      })
      ..fields.addAll({
        'room_type': roomType,
        'design_style': designStyle,
        'num_images': '$numImages',
        'input_image_url': inputImageUrl!,
      });

    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    return json.decode(responseData);
  }
}
