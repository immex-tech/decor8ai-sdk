"""Integration test for sketch_to_3d_render API.

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_sketch_to_3d_test.py
"""

from decor8ai import sketch_to_3d_render
from decor8ai.constants import RENDER_TYPES
import os
import requests


def save_generated_images(response_json, prefix="sketch3d"):
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
    # Use a sketch/floor plan test image (update URL as needed)
    input_image_url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"

    print(f"Available render types: {RENDER_TYPES}")

    # Test 1: Modern perspective render
    print("\nTest 1: Modern style - perspective render")
    response = sketch_to_3d_render(
        input_image_url=input_image_url,
        design_style="modern",
        num_images=1,
        render_type="perspective"
    )
    save_generated_images(response, "sketch3d_perspective")

    # Test 2: Scandinavian isometric render
    print("\nTest 2: Scandinavian style - isometric render")
    response = sketch_to_3d_render(
        input_image_url=input_image_url,
        design_style="scandinavian",
        num_images=1,
        render_type="isometric"
    )
    save_generated_images(response, "sketch3d_isometric")

    # Test 3: Industrial render with scale factor
    print("\nTest 3: Industrial style with scale factor")
    response = sketch_to_3d_render(
        input_image_url=input_image_url,
        design_style="industrial",
        num_images=2,
        scale_factor=2
    )
    save_generated_images(response, "sketch3d_industrial")
