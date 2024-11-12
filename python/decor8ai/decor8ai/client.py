import requests
import os
import json
from urllib.parse import urlparse

dev_server_url = 'http://localhost:8000'
prod_server_url = 'https://api.decor8.ai'
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

def prime_walls_for_room(input_image_url):
            
    if not token:
        raise Exception("DECOR8AI_API_KEY environment variable is not set.")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {
        'input_image_url': input_image_url
    }
    
    response = requests.post(url + '/prime_walls_for_room', headers=headers, data=data)
    response_json = json.loads(response.text)
    
    return response_json

def replace_sky_behind_house(input_image_url, sky_type):
            
    if not token:
        raise Exception("DECOR8AI_API_KEY environment variable is not set.")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {
        'input_image_url': input_image_url,
        'sky_type': sky_type
    }
    
    response = requests.post(url + '/replace_sky_behind_house', headers=headers, data=data)
    response_json = json.loads(response.text)
    
    return response_json
def generate_designs(input_image, room_type, design_style, num_captions = None, num_images=1, keep_original_dimensions=False, color_scheme=None, speciality_decor=None):
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
    if input_image is not None:
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
    if color_scheme:
        data['color_scheme'] = color_scheme
    if speciality_decor:
        data['speciality_decor'] = speciality_decor
        
    response = requests.post(url + '/generate_designs', headers=headers, files=files, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json

def generate_designs_for_room(input_image_url,room_type, design_style,  mask_info = None, num_images=1, keep_original_dimensions=False, color_scheme=None, speciality_decor=None, scale_factor=None):
    
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
    data = {
        'input_image_url': input_image_url,
        'room_type': room_type,
        'design_style': design_style,
        'num_images': num_images,
    }
    if scale_factor:
        data['scale_factor'] = scale_factor
    if keep_original_dimensions:
        data['keep_original_dimensions'] = keep_original_dimensions
    if color_scheme:
        data['color_scheme'] = color_scheme
    if speciality_decor:
        data['speciality_decor'] = speciality_decor

    if mask_info:
        data['mask_info'] = mask_info
        
    response = requests.post(url + '/generate_designs_for_room', headers=headers, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json

def generate_inspirational_designs(room_type, design_style, num_images=1,color_scheme=None, speciality_decor=None):
    
    if not token:
        raise Exception("DECOR8AI_API_KEY environment variable is not set.")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'room_type': room_type,
        'design_style': design_style,
        'num_images': num_images
    }
    if color_scheme:
        data['color_scheme'] = color_scheme
    if speciality_decor:
        data['speciality_decor'] = speciality_decor

    response = requests.post(url + '/generate_inspirational_designs', headers=headers, data=data)
    
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


def remove_objects_from_room(input_image_url):
    
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
    data = {
        'input_image_url': input_image_url
    }

    response = requests.post(url + '/remove_objects_from_room', headers=headers, data=data)
    
    response_json = json.loads(response.text)
    
    return response_json