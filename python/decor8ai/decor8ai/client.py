import requests
import os
import json
from urllib.parse import urlparse

def generate_designs(input_image, room_type, design_style, num_captions = None, num_images=1, mask_image_path=None, room_options_json=None):
    
    def is_url(path):
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    url = 'https://prod-app.decor8.ai:8000/generate_designs'
    token = os.environ.get('DECOR8AI_API_KEY')
    if not token:
        raise Exception("DECOR8AI_API_KEY environment variable is not set.")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Handling various input types for the image
    if isinstance(input_image, bytes):
        input_image_content = input_image
    elif is_url(input_image):
        response = requests.get(input_image)
        input_image_content = response.content
    else:  # Assuming it's a file path
        with open(input_image, 'rb') as img_file:
            input_image_content = img_file.read()
    
    files = {
        'input_image': ('input_image.jpg', input_image_content)
    }
    
    if mask_image_path:
        files['mask_image'] = ('mask_image.jpg', open(mask_image_path, 'rb'))
    
    data = {
        'room_type': room_type,
        'design_style': design_style,
        'num_images': num_images
    }
    if num_captions:
        data['num_captions'] = num_captions
        
    if room_options_json:
        data['room_options_json'] = room_options_json
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json


