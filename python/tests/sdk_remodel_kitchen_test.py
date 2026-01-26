"""Integration test for remodel_kitchen API.

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_remodel_kitchen_test.py
"""

from decor8ai import remodel_kitchen
import os
import requests


def save_generated_images(response_json, prefix="kitchen"):
    """Save generated images to output directory."""
    if response_json.get('error'):
        print(f"Error: {response_json['error']} : {response_json.get('message', '')}")
        return

    images = response_json.get("info", {}).get("images", [])
    for image in images:
        uuid = image.get("uuid")
        image_url = image.get("url")

        if uuid and image_url:
            response = requests.get(image_url)
            output_directory = "output-data"
            os.makedirs(output_directory, exist_ok=True)

            filepath = f"{output_directory}/{prefix}_{uuid}.jpg"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Saved: {filepath}")


if __name__ == "__main__":
    # Use a kitchen test image (update URL as needed)
    input_image_url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"

    # Test 1: Modern kitchen remodel
    print("\nTest 1: Modern kitchen remodel")
    response = remodel_kitchen(
        input_image_url=input_image_url,
        design_style="modern",
        num_images=1
    )
    save_generated_images(response, "kitchen_modern")

    # Test 2: Farmhouse kitchen remodel with scale factor
    print("\nTest 2: Farmhouse kitchen remodel")
    response = remodel_kitchen(
        input_image_url=input_image_url,
        design_style="farmhouse",
        num_images=2,
        scale_factor=2
    )
    save_generated_images(response, "kitchen_farmhouse")

    # Test 3: Scandinavian kitchen remodel
    print("\nTest 3: Scandinavian kitchen remodel")
    response = remodel_kitchen(
        input_image_url=input_image_url,
        design_style="scandinavian",
        num_images=1
    )
    save_generated_images(response, "kitchen_scandinavian")
