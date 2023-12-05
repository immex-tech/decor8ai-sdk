from decor8ai.client import generate_image_captions
import os
import base64
import concurrent.futures
room_type = 'livingroom'
design_style = 'frenchcountry'
num_captions = 2

response = generate_image_captions(room_type, design_style, num_captions)
print(response)


    
