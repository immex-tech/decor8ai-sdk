"""Integration test for generate_landscaping_designs API (Beta).

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_landscaping_test.py
"""

from decor8ai import generate_landscaping_designs
from decor8ai.constants import YARD_TYPES, GARDEN_STYLES
import os
import requests


def save_generated_images(response_json, prefix="landscape"):
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
    # Use a yard/exterior test image (update URL as needed)
    input_image_url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"

    print(f"Available yard types: {YARD_TYPES}")
    print(f"Available garden styles (first 10): {GARDEN_STYLES[:10]}...")

    # Test 1: Japanese Zen front yard
    print("\nTest 1: Japanese Zen front yard")
    response = generate_landscaping_designs(
        input_image_url=input_image_url,
        yard_type="Front Yard",
        garden_style="japanese_zen",
        num_images=1
    )
    save_generated_images(response, "landscape_zen")

    # Test 2: Mediterranean backyard
    print("\nTest 2: Mediterranean backyard")
    response = generate_landscaping_designs(
        input_image_url=input_image_url,
        yard_type="Backyard",
        garden_style="mediterranean",
        num_images=2
    )
    save_generated_images(response, "landscape_mediterranean")

    # Test 3: Modern minimalist side yard
    print("\nTest 3: Modern minimalist side yard")
    response = generate_landscaping_designs(
        input_image_url=input_image_url,
        yard_type="Side Yard",
        garden_style="modern_minimalist",
        num_images=1
    )
    save_generated_images(response, "landscape_modern")
