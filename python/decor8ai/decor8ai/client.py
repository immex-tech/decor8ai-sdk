import requests
import os
import json
from urllib.parse import urlparse

dev_server_url = 'http://localhost:8000'
prod_server_url = 'https://prod-app.decor8.ai:8000'
url = prod_server_url
token = os.environ.get('DECOR8AI_API_KEY')


def prime_the_room_walls(input_image):
        
        def is_url(path):
            try:
                result = urlparse(path)
                return all([result.scheme, result.netloc])
            except ValueError:
                return False
        
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
        
        response = requests.post(url + '/prime_the_room_walls', headers=headers, files=files)
        response_json = json.loads(response.text)
        
        return response_json

def generate_designs(input_image, room_type, design_style, num_captions = None, num_images=1, keep_original_dimensions=False):
    
    def is_url(path):
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
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
    
    data = {
        'room_type': room_type,
        'design_style': design_style,
        'num_images': num_images
    }
    if num_captions:
        data['num_captions'] = num_captions
    if keep_original_dimensions:
        data['keep_original_dimensions'] = keep_original_dimensions
        
    response = requests.post(url + '/generate_designs', headers=headers, files=files, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json

def generate_image_captions(design_style, room_type, num_captions):
    
    if not token:
        raise Exception("DECOR8AI_API_KEY environment variable is not set.")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    data = {
        'room_type': room_type,
        'design_style': design_style,
        'num_captions': num_captions
    }
    
    response = requests.post(url + '/generate_image_captions', headers=headers, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json

def upscale_image(input_image, scale_factor=2):
        
        def is_url(path):
            try:
                result = urlparse(path)
                return all([result.scheme, result.netloc])
            except ValueError:
                return False
        
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
        
        data = {
            'scale_factor': scale_factor
        }
        
        response = requests.post(url + '/upscale_image', headers=headers, files=files, data=data)
        
        response_json = json.loads(response.text)
        
        return response_json

