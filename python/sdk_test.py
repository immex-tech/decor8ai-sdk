from decor8ai.client import generate_designs
import os
import base64
# Specify paths and data
input_image = './sdk_test_image.png'  # or URL or bytes
room_type = 'livingroom'
design_style = 'frenchcountry'
num_images = 1

# Call the function
response_json = generate_designs(input_image, room_type, design_style, num_images)

# Now you can work with response_json as a normal dictionary
print(response_json)

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







