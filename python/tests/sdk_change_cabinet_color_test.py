"""Integration test for change_kitchen_cabinets_color API.

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_change_cabinet_color_test.py
"""

from decor8ai import change_kitchen_cabinets_color
import os
import requests


def save_generated_images(response_json, prefix="cabinet"):
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

    # Test 1: White cabinets
    print("\nTest 1: Change cabinets to white (#FFFFFF)")
    response = change_kitchen_cabinets_color(
        input_image_url=input_image_url,
        cabinet_color_hex_code="#FFFFFF"
    )
    save_generated_images(response, "cabinet_white")

    # Test 2: Navy blue cabinets
    print("\nTest 2: Change cabinets to navy blue (#000080)")
    response = change_kitchen_cabinets_color(
        input_image_url=input_image_url,
        cabinet_color_hex_code="#000080"
    )
    save_generated_images(response, "cabinet_navy")

    # Test 3: Sage green cabinets
    print("\nTest 3: Change cabinets to sage green (#9DC183)")
    response = change_kitchen_cabinets_color(
        input_image_url=input_image_url,
        cabinet_color_hex_code="#9DC183"
    )
    save_generated_images(response, "cabinet_sage")
