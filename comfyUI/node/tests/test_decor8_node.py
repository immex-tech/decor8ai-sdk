import os
import pytest
import requests
import sys
import numpy as np
from pathlib import Path
from PIL import Image
import io
import torch

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from virtual_staging_node import VirtualStagingNode

@pytest.fixture
def node():
    if not os.getenv('DECOR8AI_API_KEY'):
        raise ValueError("DECOR8AI_API_KEY environment variable must be set to run tests")
    return VirtualStagingNode()

@pytest.fixture
def test_image():
    """Load test image as PyTorch tensor"""
    url = "https://prod-files.decor8.ai/test-images/sdk_test_image.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download test image")
    
    image = Image.open(io.BytesIO(response.content))
    print(f"PIL Image size: {image.size}")  # PIL uses (width, height)
    
    numpy_array = np.array(image, dtype=np.float32) / 255.0
    print(f"Numpy array shape: {numpy_array.shape}")
    
    tensor = torch.from_numpy(numpy_array).unsqueeze(0)
    print(f"Tensor shape: {tensor.shape}")
     
    print(f"Original image shape: {np.array(image).shape}")
    print(f"Numpy array shape: {numpy_array.shape}")
    print(f"Final tensor shape: {tensor.shape}")
    
    return tensor

@pytest.fixture
def api_key():
    key = os.getenv('DECOR8AI_API_KEY')
    if not key:
        raise ValueError("DECOR8AI_API_KEY environment variable must be set to run tests")
    return key

def test_input_types(node):
    input_types = node.INPUT_TYPES()
    assert "image" in input_types["required"]
    assert "api_key" in input_types["required"]
    assert "prompt" in input_types["optional"]
    assert "room_type" in input_types["optional"]
    assert "design_style" in input_types["optional"]

def test_return_types(node):
    assert node.RETURN_TYPES == ("IMAGE",)
    assert node.CATEGORY == "Decor8 AI"

@pytest.mark.skipif(not os.getenv('DECOR8AI_API_KEY'), 
                   reason="DECOR8AI_API_KEY not set")
def test_generate_design_with_room_and_style(node, test_image, api_key):
    """Test generation using room_type and design_style without prompt"""
    result = node.generate_design(
        image=test_image,
        api_key=api_key,
        room_type="livingroom",
        design_style="rustic",
        num_images=1
    )
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], torch.Tensor)
    assert len(result[0].shape) == 4  # (N, C, H, W) for PyTorch
    assert result[0].shape[0] == 1    # num_images
    assert result[0].shape[3] == 3    # RGB channels for PyTorch
    assert result[0].dtype == torch.float32
    assert torch.max(result[0]) <= 1.0
    assert torch.min(result[0]) >= 0.0
    assert not torch.isnan(result[0]).any()  # PyTorch NaN check

@pytest.mark.skipif(not os.getenv('DECOR8AI_API_KEY'), 
                   reason="DECOR8AI_API_KEY not set")
def test_generate_design_with_prompt(node, test_image, api_key):
    """Test generation using prompt with room_type and design_style"""
    result = node.generate_design(
        image=test_image,
        api_key=api_key,
        prompt="a rustic cabin interior design living room with antique furniture and decor",
        num_images=2
    )
    
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], torch.Tensor)
    assert len(result[0].shape) == 4
    assert result[0].shape[0] == 2

@pytest.mark.skipif(not os.getenv('DECOR8AI_API_KEY'), 
                   reason="DECOR8AI_API_KEY not set")
def test_generate_design_with_all_parameters(node, test_image, api_key):
    """Test generation with all available parameters"""
    result = node.generate_design(
        image=test_image,
        api_key=api_key,
        prompt="cozy mountain cabin",
        room_type="livingroom",
        design_style="rustic",
        prompt_prefix="high quality, photorealistic",
        prompt_suffix="warm lighting, evening",
        negative_prompt="modern, minimalist",
        seed=42,
        color_scheme="COLOR_SCHEME_1",
        speciality_decor="SPECIALITY_DECOR_1",
        guidance_scale=12.5,
        num_inference_steps=60,
        num_images=2,
        scale_factor=1
    )
    
    assert isinstance(result, tuple)
    assert len(result) == 1
    assert isinstance(result[0], torch.Tensor)
    assert len(result[0].shape) == 4
    assert result[0].shape[0] == 2

def test_parameter_validation(node, test_image, api_key):
    """Test parameter validation rules"""
    # Should raise error when neither prompt nor room_type/design_style provided
    with pytest.raises(RuntimeError):
        node.generate_design(
            image=test_image,
            api_key=api_key
        )
    
    # Should raise error when only room_type provided
    with pytest.raises(RuntimeError):
        node.generate_design(
            image=test_image,
            api_key=api_key,
            room_type="livingroom"
        )
    
    # Should raise error when only design_style provided
    with pytest.raises(RuntimeError):
        node.generate_design(
            image=test_image,
            api_key=api_key,
            design_style="rustic"
        )

@pytest.mark.skipif(not os.getenv('DECOR8AI_API_KEY'), 
                   reason="DECOR8AI_API_KEY not set")
def test_generate_design_with_scale_factor(node, test_image, api_key):
    """Test generation with different scale factors"""
    # Test with scale_factor = 2
    result_scaled = node.generate_design(
        image=test_image,
        api_key=api_key,
        room_type="livingroom",
        design_style="rustic",
        scale_factor=2,
        num_images=1
    )
    
    # Test with default scale_factor = 1
    result_default = node.generate_design(
        image=test_image,
        api_key=api_key,
        room_type="livingroom",
        design_style="rustic",
        num_images=1
    )
    
    # Basic validation
    assert isinstance(result_scaled, tuple)
    assert isinstance(result_default, tuple)
    
    # Check dimensions
    scaled_image = result_scaled[0]
    default_image = result_default[0]
    
    assert isinstance(scaled_image, torch.Tensor)
    assert isinstance(default_image, torch.Tensor)
    
    print(scaled_image.shape)
    print(default_image.shape)
    # Scaled image should be exactly 2x the dimensions of default
    assert scaled_image.shape[1] == default_image.shape[1] * 2  # Height
    assert scaled_image.shape[2] == default_image.shape[2] * 2  # Width
    
    # Value range check
    assert torch.max(scaled_image) <= 1.0
    assert torch.min(scaled_image) >= 0.0
    assert not torch.isnan(scaled_image).any()  # PyTorch NaN check 