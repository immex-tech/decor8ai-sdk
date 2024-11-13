from decor8ai.client import remove_objects_from_room, upscale_image, generate_designs
import base64, os
from PIL import Image
from io import BytesIO
import uuid

# Remove objects and upscale
empty_room_url = remove_objects_from_room(input_image_url='https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_familyroom_2.jpg')["info"]["image"]["url"]
upscaled_data = base64.b64decode(upscale_image(empty_room_url, scale_factor=2)["info"]["upscaled_image"])

# Generate and save designs
os.makedirs("output-data", exist_ok=True)
for i, img in enumerate(generate_designs(upscaled_data, room_type='familyroom', design_style='rustic', num_images=4, speciality_decor="SPECIALITY_DECOR_5")["info"]["images"]):
    Image.open(BytesIO(base64.b64decode(img["data"]))).save(f"output-data/generated_designs_{i}_{uuid.uuid4()}.jpg")
