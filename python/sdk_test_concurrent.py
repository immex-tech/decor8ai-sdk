from decor8ai.client import generate_designs
import os
import base64
import concurrent.futures
# Specify paths and data
input_image = './sdk_test_image.png'  # or URL or bytes
room_type = 'livingroom'
design_style = 'frenchcountry'
num_images = 1




def generate_image(image_id):
    print(f"Generaring Image {image_id} .")  
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


# Define the number of workers (threads) you want in your pool
num_workers = 50
max_images = 100
# Using ThreadPoolExecutor to manage a pool of workers
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Submitting tasks to the thread pool
    futures = [executor.submit(generate_image, i) for i in range(max_images)]  # Generating 10 images

    # Retrieving the results (if any) and handling exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()  # Retrieve the result of the function execution (if any)
        except Exception as e:
            print(f"An error occurred: {e}")

