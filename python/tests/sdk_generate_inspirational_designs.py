from decor8ai.client import generate_inspirational_designs
import os
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
        print(mask_info)

# Test 1: Original usage (backward compatibility)
print("\nTest 1: Original parameter usage")
room_type = 'bedroom'
design_style = 'frenchcountry'
num_images = 1
color_scheme = 'COLOR_SCHEME_0'
speciality_decor = 'SPECIALITY_DECOR_0'

response_json = generate_inspirational_designs(
    room_type=room_type,
    design_style=design_style,
    num_images=num_images,
    color_scheme=color_scheme,
    speciality_decor=speciality_decor
)
save_generated_images(response_json)

# Test 2: New parameters usage
print("\nTest 2: New parameter usage")
response_json = generate_inspirational_designs(
    room_type='bedroom',
    design_style='modern',
    num_images=2,
    # New parameters
    prompt="A luxurious bedroom with ocean view",
    prompt_prefix="high end, professional photo",
    prompt_suffix="natural lighting, detailed textures",
    negative_prompt="cluttered, dark, cartoon",
    seed=42,
    guidance_scale=15.0,
    num_inference_steps=50
)
save_generated_images(response_json)

# Test 3: Mixed usage with custom prompt overriding style
print("\nTest 3: Custom prompt with some standard parameters")
response_json = generate_inspirational_designs(
    num_images=1,
    prompt="A cozy reading nook with built-in bookshelves",
    guidance_scale=15.0
)
save_generated_images(response_json)







