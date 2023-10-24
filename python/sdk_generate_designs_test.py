from decor8ai.client import generate_designs
import os
import base64

# Mandatory Parameters
input_image = './sdk_test_image.png'  # or URL or bytes
room_type = 'livingroom'
design_style = 'frenchcountry'
num_images = 1

response_json = generate_designs(input_image=input_image, room_type=room_type, design_style=design_style, num_images=num_images, num_captions=1)
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
#                 "data": "<base64-encoded_data>",
#                 "width": 768,
#                 "height": 512,
#                 "captions":
#                 [
#                     "Unveiling the art of rustic elegance in this French Country haven, where warmth and sophistication meet effortlessly."
#                 ]
#             }
#         ]
#     }
# }

# Sample response when unsuccessful. "error" will be non-empty value.
# {
#     "error": "InvalidInput",
#     "message": "Invalid input image. Please check the input image and try again.",
# }


if response_json['error'] != '': 
    print('Error : ' + response_json['error'] + ' : ' + response_json['message'])
else:
    # Show the images
    images = response_json.get("info", {}).get("images", [])
    for image in images:
        uuid = image.get("uuid")
        data = image.get("data")
        
        if uuid and data:
            # Decode the base64 data
            image_data = base64.b64decode(data)
            
            # Save the image in the specified directory
            output_directory = "output-data"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            with open(f"{output_directory}/{uuid}.jpg", "wb") as image_file:
                image_file.write(image_data)

            print (f"Saved Image  : {output_directory}/{uuid}.jpg")

    # Show the captions
    captions = response_json.get("info", {}).get("captions", [])
    for caption in captions:
        print(caption)







