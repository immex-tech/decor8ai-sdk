from decor8ai.client import generate_designs_for_room
import os
import base64
import requests


# Mandatory Parameters
input_image_url = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png'
mask_info = None
num_images = 2

# Refer to https://github.com/immex-tech/decor8ai-sdk/tree/main/python/decor8ai for supported values
room_type = 'bedroom'
design_style = 'frenchcountry'
color_scheme = 'COLOR_SCHEME_5'; 
speciality_decor = 'SPECIALITY_DECOR_5'; 
#scale_factor = 4

response_json = generate_designs_for_room(input_image_url=input_image_url,mask_info=mask_info, room_type=room_type, design_style=design_style, num_images=num_images, color_scheme=color_scheme, speciality_decor=speciality_decor)
# Sample response when successful
# {
#     "error": "",
#     "message": "Successfully generated designs.",
#     "info":
#     {
#         "images":
#         [
#             {
#                 "uuid": "81133196-4477-4cdd-834a-89f5482bb9d0",
#                 "url": "http://<path-of-image>",
#                 "width": 768,
#                 "height": 512
#             }
#         ]
#     }
# }

# Sample response when unsuccessful. "error" will be non-empty value.
# {
#     "error": "InvalidInput",
#     "message": "Invalid input image. Please check the input image and try again.",
# }
print (response_json)
if response_json['error'] != '': 
    print('Error : ' + response_json['error'] + ' : ' + response_json['message'])
else:
    # Show the images
    images = response_json.get("info", {}).get("images", [])
    for image in images:
        uuid = image.get("uuid")
        image_url = image.get("url")
        
        if uuid and image_url:
            # Get image file at image_url
            response = requests.get(image_url)
            image_data = response.content
            
            # Save the image in the specified directory
            output_directory = "output-data"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            with open(f"{output_directory}/{uuid}.jpg", "wb") as image_file:
                image_file.write(image_data)

            print (f"Saved Image  : {output_directory}/{uuid}.jpg")

    mask_info = response_json.get("info", {}).get("mask_info", {})
    print (mask_info)







