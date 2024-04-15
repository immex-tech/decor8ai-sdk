from decor8ai.client import prime_the_room_walls, generate_designs
import os
import base64

# Mandatory Parameters
input_image = './sdk_prime_the_walls_image.jpg'  # or URL or bytes

print ('Priming the room walls')
response_json = prime_the_room_walls(input_image=input_image)

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
            
            primed_room_image = f"{output_directory}/{uuid}.jpg"
            with open(primed_room_image, "wb") as image_file:
                image_file.write(image_data)

            print (f"Saved Primed Walls Image  : {output_directory}/{uuid}.jpg")

            # Generate Designs

            input_image = primed_room_image
            room_type = 'livingroom'
            design_style = 'frenchcountry'
            num_images = 1

            print ('Generating Designs')
            response_json = generate_designs(input_image=input_image, room_type=room_type, design_style=design_style, num_images=num_images, num_captions=1)
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

                        print (f"Saved Generated Design Image  : {output_directory}/{uuid}.jpg")

