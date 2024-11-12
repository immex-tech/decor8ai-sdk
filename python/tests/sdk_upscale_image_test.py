from decor8ai.client import upscale_image
import os
import base64
import concurrent.futures
input_image = './sdk_prime_the_walls_image-1536xy.jpg'  # or URL or bytes
scale_factor = 3

response = upscale_image(input_image, scale_factor)
print(response)


    
