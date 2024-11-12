from decor8ai.client import generate_designs_for_room
import os
import base64
import concurrent.futures
import requests
# Specify paths and data
input_image_url = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png'
room_type = 'livingroom'
design_style = 'frenchcountry'
num_images = 1

def generate_image(image_id):
    print(f"Generaring Image {image_id} .")  
    # Call the function
    response_json = generate_designs_for_room(input_image_url, room_type, design_style, num_images=num_images)

    # Now you can work with response_json as a normal dictionary
    print(response_json)

    # Show the images
    images = response_json.get("info", {}).get("images", [])
    for image in images:
        uuid = image.get("uuid")
        url = image.get("url")
        
        if uuid and url:
            image_data = requests.get(url).content
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
num_workers = 10
max_images = 10
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

