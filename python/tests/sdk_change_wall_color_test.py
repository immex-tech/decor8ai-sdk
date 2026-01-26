"""Integration test for change_wall_color API.

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_change_wall_color_test.py
"""

from decor8ai import change_wall_color
import os
import requests


def save_generated_images(response_json, prefix="wall_color"):
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
    # Test image URL
    input_image_url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"

    # Test 1: Change wall to warm beige
    print("\nTest 1: Change wall color to warm beige (#D4A574)")
    response = change_wall_color(
        input_image_url=input_image_url,
        wall_color_hex_code="#D4A574"
    )
    save_generated_images(response, "wall_beige")

    # Test 2: Change wall to cool blue
    print("\nTest 2: Change wall color to cool blue (#87CEEB)")
    response = change_wall_color(
        input_image_url=input_image_url,
        wall_color_hex_code="#87CEEB"
    )
    save_generated_images(response, "wall_blue")

    # Test 3: Change wall to modern gray
    print("\nTest 3: Change wall color to modern gray (#808080)")
    response = change_wall_color(
        input_image_url=input_image_url,
        wall_color_hex_code="#808080"
    )
    save_generated_images(response, "wall_gray")
