from decor8ai.client import remove_objects_from_room
import requests
from PIL import Image 
from io import BytesIO

response = remove_objects_from_room(input_image_url='https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_bedroom_1.jpg')
# {
#     "error": "",
#     "message": "Successfully removed objects from room.",
#     "info":
#     {
#         "image":
#         {
#             "uuid": "6fd26b4a-d5e2-4765-a0a9-761df95fa823",
#             "width": 768,
#             "height": 576,
#             "url": "https://prod-files.decor8.ai/customer-images/decor8ai_api_user_15003/8ec7ac0b-73aa-442e-8769-bbed91a4c1b3.jpg"
#         }
#     }
# }
Image.open(BytesIO(requests.get(response["info"]["image"]["url"]).content)).save("output-data/remove_objects_from_room.jpg")