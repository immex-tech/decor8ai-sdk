import 'package:decor8ai/decor8ai.dart';
import 'package:test/test.dart';

void main() async {
  const decor8aiApiKey= '<DECOR8AI_API_KEY>'; // Get it from prod-app.decor8.ai -> Profile

  group('Decor8AI generateDesigns', () {
    test('returns generated designs on successful response', () async {
      var decor8 = Decor8AI(decor8aiApiKey);

      var generateDesignsResponse = await decor8.generateDesigns(
        './test/sdk_test_image.jpg',
        'livingroom',
        'modern',
      );
      
      expect(generateDesignsResponse['error'], isEmpty);
      expect(generateDesignsResponse['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));
  });

  group('Decor8AI primeTheRoomWalls', () {
    test('returns primed wall designs on successful response', () async {
      var decor8 = Decor8AI(decor8aiApiKey);
      var primeWallsResponse = await decor8.primeTheRoomWalls('./test/sdk_prime_the_walls_image.jpg');
      expect(primeWallsResponse['error'], isEmpty);
      expect(primeWallsResponse['info']['images'], isNotEmpty);
    }, timeout: Timeout(Duration(minutes: 2)));
  });




}
