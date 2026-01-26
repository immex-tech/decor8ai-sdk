"""Integration test for remodel_bathroom API.

Requires DECOR8AI_API_KEY environment variable to be set.
Run with: python sdk_remodel_bathroom_test.py
"""

from decor8ai import remodel_bathroom
import os
import requests


def save_generated_images(response_json, prefix="bathroom"):
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
    # Use a bathroom test image (update URL as needed)
    input_image_url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"

    # Test 1: Modern bathroom remodel
    print("\nTest 1: Modern bathroom remodel")
    response = remodel_bathroom(
        input_image_url=input_image_url,
        design_style="modern",
        num_images=1
    )
    save_generated_images(response, "bathroom_modern")

    # Test 2: Spa-like contemporary remodel
    print("\nTest 2: Contemporary bathroom remodel")
    response = remodel_bathroom(
        input_image_url=input_image_url,
        design_style="contemporary",
        num_images=2
    )
    save_generated_images(response, "bathroom_contemporary")
