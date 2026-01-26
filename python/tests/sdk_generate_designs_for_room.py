from decor8ai.client import generate_designs_for_room
import os
import base64
import requests

def save_generated_images(response_json):
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

                print(f"Saved Image  : {output_directory}/{uuid}.jpg")

        mask_info = response_json.get("info", {}).get("mask_info", {})
        print("Mask Info:", mask_info)

# Test 1: Original usage (backward compatibility)
print("\nTest 1: Original parameter usage")
# Mandatory Parameters
input_image_url = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png'
mask_info = None
num_images = 1

# Standard parameters
room_type = 'bedroom'
design_style = 'frenchcountry'
color_scheme = 'COLOR_SCHEME_0'
speciality_decor = 'SPECIALITY_DECOR_0'
keep_original_floor = False

response_json = generate_designs_for_room(
    input_image_url=input_image_url,
    mask_info=mask_info,
    room_type=room_type,
    design_style=design_style,
    num_images=num_images,
    color_scheme=color_scheme,
    speciality_decor=speciality_decor,
    keep_original_floor=keep_original_floor
)
save_generated_images(response_json)

# Test 2: New parameters usage
print("\nTest 2: New parameter usage")



response_json = generate_designs_for_room(
    input_image_url=input_image_url,
    num_images=2,
    prompt="bedroom with bed, wardrobe, Table Lamps, Dresser, Minimalist design style with simple lines, neutral colors",
    prompt_prefix="Real Estate Property Listing, Award Winning photo of ",
    prompt_suffix="4K, Trending, natural lighting, detailed textures",
    negative_prompt="cluttered, dark, cartoon, unreal, person, baby, kid, child, pet, animal, human, face, body, limbs",
    seed=7566969,
    guidance_scale=15.0,
    num_inference_steps=50
)





save_generated_images(response_json)

# Test 3: Mixed usage with custom prompt overriding style
print("\nTest 3: Custom prompt with some standard parameters")
response_json = generate_designs_for_room(
    input_image_url=input_image_url,
    num_images=1,
    keep_original_floor=True,
    prompt="A cozy reading nook with built-in bookshelves",
    guidance_scale=15.0
)
save_generated_images(response_json)







