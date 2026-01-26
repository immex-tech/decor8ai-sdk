"""Decor8 AI Virtual Staging nodes for ComfyUI.

Transforms empty spaces into staged interiors using AI-powered design generation.
Requires a Decor8 AI API key from www.decor8.ai
"""

import os
import requests
import torch
from PIL import Image
import io
import logging
import numpy as np

# =============================================================================
# Constants
# =============================================================================

ROOM_TYPES = [
    "livingroom", "kitchen", "diningroom", "bedroom", "bathroom",
    "kidsroom", "familyroom", "readingnook", "sunroom", "walkincloset",
    "mudroom", "toyroom", "office", "foyer", "powderroom", "laundryroom",
    "gym", "basement", "garage", "balcony", "cafe", "homebar",
    "study_room", "front_porch", "back_porch", "back_patio", "openplan",
    "boardroom", "meetingroom", "openworkspace", "privateoffice"
]

DESIGN_STYLES = [
    "minimalist", "scandinavian", "industrial", "boho", "traditional",
    "artdeco", "midcenturymodern", "coastal", "tropical", "eclectic",
    "contemporary", "frenchcountry", "rustic", "shabbychic", "vintage",
    "country", "modern", "asian_zen", "hollywoodregency", "bauhaus",
    "mediterranean", "farmhouse", "victorian", "gothic", "moroccan",
    "southwestern", "transitional", "maximalist", "arabic", "japandi",
    "retrofuturism", "artnouveau", "urbanmodern", "wabi_sabi",
    "grandmillennial", "coastalgrandmother", "newtraditional", "cottagecore",
    "luxemodern", "high_tech", "organicmodern", "tuscan", "cabin",
    "desertmodern", "global", "industrialchic", "modernfarmhouse",
    "europeanclassic", "neotraditional", "warmminimalist"
]

COLOR_SCHEMES = [f"COLOR_SCHEME_{i}" for i in range(21)]

SPECIALITY_DECORS = [f"SPECIALITY_DECOR_{i}" for i in range(8)]

SKY_TYPES = ["day", "dusk", "night"]

YARD_TYPES = ["Front Yard", "Backyard", "Side Yard"]

GARDEN_STYLES = [
    "japanese_zen", "mediterranean", "english_cottage", "tropical", "desert",
    "modern_minimalist", "french_formal", "coastal", "woodland", "prairie",
    "rock_garden", "water_garden", "herb_garden", "cutting_garden", "pollinator",
    "xeriscape", "edible_landscape", "moon_garden", "rain_garden", "sensory",
    "native_plant", "cottage_style", "formal_parterre", "naturalistic",
    "contemporary", "asian_fusion", "rustic_farmhouse", "urban_modern",
    "sustainable", "wildlife_habitat", "four_season"
]


# =============================================================================
# Base Node Class
# =============================================================================

class Decor8AIBaseNode:
    """Base class for Decor8 AI nodes with common functionality."""

    API_BASE = "https://api.decor8.ai"
    CATEGORY = "Decor8 AI"

    def __init__(self):
        self.logger = logging.getLogger('decor8ai')

    def _validate_image(self, image_tensor):
        """Validate image tensor dimensions and values."""
        if not isinstance(image_tensor, torch.Tensor):
            raise ValueError("Input must be a PyTorch tensor")
        if len(image_tensor.shape) not in [3, 4]:
            raise ValueError(f"Invalid image dimensions: {image_tensor.shape}")
        if image_tensor.max() > 1.0 or image_tensor.min() < 0.0:
            raise ValueError("Image values must be in range [0, 1]")

    def _tensor_to_file(self, image_tensor):
        """Convert PyTorch tensor to file-like object."""
        self._validate_image(image_tensor)
        image_tensor = image_tensor.squeeze(0)
        image_pil = Image.fromarray((image_tensor.numpy() * 255).astype(np.uint8))
        buffer = io.BytesIO()
        image_pil.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer

    def _url_to_tensor(self, url):
        """Download image from URL and convert to PyTorch tensor."""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        image_tensor = torch.tensor(
            list(image.getdata()),
            dtype=torch.float32
        ).reshape(image.size[1], image.size[0], -1) / 255.0
        image_tensor = image_tensor.unsqueeze(0)
        self._validate_image(image_tensor)
        return image_tensor

    def _post_multipart(self, endpoint, api_key, files, data):
        """Make multipart POST request to API."""
        response = requests.post(
            f"{self.API_BASE}{endpoint}",
            headers={"Authorization": f"Bearer {api_key}"},
            data=data,
            files=files,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            raise RuntimeError(f"API error: {result['error']}")
        return result

    def _post_json(self, endpoint, api_key, data):
        """Make JSON POST request to API."""
        response = requests.post(
            f"{self.API_BASE}{endpoint}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=data,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            raise RuntimeError(f"API error: {result['error']}")
        return result

    def _process_output_images(self, result):
        """Convert API result images to tensor batch."""
        images = [self._url_to_tensor(img["url"]) for img in result["info"]["images"]]
        return torch.cat(images, dim=0)


# =============================================================================
# Virtual Staging Node
# =============================================================================

class VirtualStagingNode(Decor8AIBaseNode):
    """Virtual Staging node - transforms empty rooms into staged interiors."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
            },
            "optional": {
                "prompt": ("STRING", {"default": ""}),
                "room_type": (ROOM_TYPES,),
                "design_style": (DESIGN_STYLES,),
                "color_scheme": (["none"] + COLOR_SCHEMES,),
                "speciality_decor": (["none"] + SPECIALITY_DECORS,),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
                "guidance_scale": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "num_inference_steps": ("INT", {"default": 0, "min": 0, "max": 75}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "scale_factor": ("INT", {"default": 1, "min": 1, "max": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_design"

    def generate_design(self, image, api_key, prompt=None, room_type=None, design_style=None,
                       color_scheme=None, speciality_decor=None, seed=0,
                       guidance_scale=0.0, num_inference_steps=0, num_images=1, scale_factor=1):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")
        if not prompt and (not room_type or not design_style):
            raise ValueError("Either prompt or both room_type and design_style required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {"num_images": num_images}
        if scale_factor > 1:
            data["scale_factor"] = scale_factor

        if prompt:
            data["prompt"] = prompt
        else:
            data["room_type"] = room_type
            data["design_style"] = design_style
            if color_scheme and color_scheme != "none":
                data["color_scheme"] = color_scheme
            if speciality_decor and speciality_decor != "none":
                data["speciality_decor"] = speciality_decor

        if seed > 0:
            data["seed"] = seed
        if guidance_scale > 0:
            data["guidance_scale"] = guidance_scale
        if num_inference_steps > 0:
            data["num_inference_steps"] = num_inference_steps

        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/generate_designs', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Wall Color Change Node
# =============================================================================

class WallColorChangeNode(Decor8AIBaseNode):
    """Change wall colors in room images."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
                "wall_color_hex": ("STRING", {"default": "#FFFFFF"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "change_wall_color"

    def change_wall_color(self, image, api_key, wall_color_hex):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        # Upload image and get URL, then call change_wall_color
        # For now, use multipart upload approach
        files = {'input_image': ('image.png', image_file, 'image/png')}
        data = {'wall_color_hex_code': wall_color_hex}

        result = self._post_multipart('/change_wall_color', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Kitchen Remodel Node
# =============================================================================

class KitchenRemodelNode(Decor8AIBaseNode):
    """Remodel kitchen images with different design styles."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
                "design_style": (DESIGN_STYLES,),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "scale_factor": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "remodel_kitchen"

    def remodel_kitchen(self, image, api_key, design_style, num_images=1, scale_factor=1):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {"design_style": design_style}
        if num_images > 1:
            data["num_images"] = num_images
        if scale_factor > 1:
            data["scale_factor"] = scale_factor

        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/remodel_kitchen', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Bathroom Remodel Node
# =============================================================================

class BathroomRemodelNode(Decor8AIBaseNode):
    """Remodel bathroom images with different design styles."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
                "design_style": (DESIGN_STYLES,),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "scale_factor": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "remodel_bathroom"

    def remodel_bathroom(self, image, api_key, design_style, num_images=1, scale_factor=1):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {"design_style": design_style}
        if num_images > 1:
            data["num_images"] = num_images
        if scale_factor > 1:
            data["scale_factor"] = scale_factor

        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/remodel_bathroom', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Sky Replacement Node
# =============================================================================

class SkyReplacementNode(Decor8AIBaseNode):
    """Replace sky in exterior property photos."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
                "sky_type": (SKY_TYPES,),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "replace_sky"

    def replace_sky(self, image, api_key, sky_type):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {"sky_type": sky_type}
        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/replace_sky_behind_house', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Landscaping Node
# =============================================================================

class LandscapingNode(Decor8AIBaseNode):
    """Generate landscaping designs for yards (Beta)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
                "yard_type": (YARD_TYPES,),
                "garden_style": (GARDEN_STYLES,),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_landscaping"

    def generate_landscaping(self, image, api_key, yard_type, garden_style, num_images=1):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {
            "yard_type": yard_type,
            "garden_style": garden_style,
        }
        if num_images > 1:
            data["num_images"] = num_images

        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/generate_landscaping_designs', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Object Removal Node
# =============================================================================

class ObjectRemovalNode(Decor8AIBaseNode):
    """Remove objects/furniture from room images."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
            },
            "optional": {
                "mask": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "remove_objects"

    def remove_objects(self, image, api_key, mask=None):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        files = {'input_image': ('image.png', image_file, 'image/png')}
        data = {}

        if mask is not None:
            self._validate_image(mask)
            mask_file = self._tensor_to_file(mask)
            files['mask_image'] = ('mask.png', mask_file, 'image/png')

        result = self._post_multipart('/remove_objects_from_room', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Image Upscale Node
# =============================================================================

class ImageUpscaleNode(Decor8AIBaseNode):
    """Upscale images to higher resolution."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
            },
            "optional": {
                "scale_factor": ("INT", {"default": 2, "min": 1, "max": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "upscale_image"

    def upscale_image(self, image, api_key, scale_factor=2):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        data = {"scale_factor": scale_factor}
        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/upscale_image', api_key, files, data)
        return (self._process_output_images(result),)


# =============================================================================
# Prime Walls Node
# =============================================================================

class PrimeWallsNode(Decor8AIBaseNode):
    """Prime room walls for virtual staging."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "prime_walls"

    def prime_walls(self, image, api_key):
        if not api_key:
            raise ValueError("Decor8 AI API key is required")

        self._validate_image(image)
        image_file = self._tensor_to_file(image)

        files = {'input_image': ('image.png', image_file, 'image/png')}
        result = self._post_multipart('/prime_the_room_walls', api_key, files, {})
        return (self._process_output_images(result),)


# =============================================================================
# Node Mappings
# =============================================================================

NODE_CLASS_MAPPINGS = {
    "VirtualStagingNode": VirtualStagingNode,
    "WallColorChangeNode": WallColorChangeNode,
    "KitchenRemodelNode": KitchenRemodelNode,
    "BathroomRemodelNode": BathroomRemodelNode,
    "SkyReplacementNode": SkyReplacementNode,
    "LandscapingNode": LandscapingNode,
    "ObjectRemovalNode": ObjectRemovalNode,
    "ImageUpscaleNode": ImageUpscaleNode,
    "PrimeWallsNode": PrimeWallsNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VirtualStagingNode": "Virtual Staging",
    "WallColorChangeNode": "Change Wall Color",
    "KitchenRemodelNode": "Kitchen Remodel",
    "BathroomRemodelNode": "Bathroom Remodel",
    "SkyReplacementNode": "Replace Sky",
    "LandscapingNode": "Landscaping Design",
    "ObjectRemovalNode": "Remove Objects",
    "ImageUpscaleNode": "Upscale Image",
    "PrimeWallsNode": "Prime Walls",
}
