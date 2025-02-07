import os
import requests
import torch
from PIL import Image
import io
import logging

class VirtualStagingNode:
    """Decor8 AI Virtual Staging node for ComfyUI - Transforms empty spaces into staged interiors"""
    
    def __init__(self):
        self.api_base = "https://api.decor8.ai"
        self.logger = logging.getLogger('decor8ai')
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": os.getenv('DECOR8AI_API_KEY', '')}),
            },
            "optional": {
                "prompt": ("STRING", {"default": ""}),
                "room_type": (["livingroom", "kitchen", "diningroom", "bedroom", "bathroom", 
                             "kidsroom", "familyroom", "readingnook", "sunroom", "walkincloset",
                             "mudroom", "toyroom", "office", "foyer", "powderroom", "laundryroom",
                             "gym", "basement", "garage", "balcony", "cafe", "homebar", 
                             "study_room", "front_porch", "back_porch", "back_patio", "openplan",
                             "boardroom", "meetingroom", "openworkspace", "privateoffice"],),
                "design_style": (["minimalist", "scandinavian", "industrial", "boho", "traditional",
                                "artdeco", "midcenturymodern", "coastal", "tropical", "eclectic",
                                "contemporary", "frenchcountry", "rustic", "shabbychic", "vintage",
                                "country", "modern", "asian_zen", "hollywoodregency", "bauhaus",
                                "mediterranean", "farmhouse", "victorian", "gothic", "moroccan",
                                "southwestern", "transitional", "maximalist", "arabic", "japandi",
                                "retrofuturism", "artnouveau"],),
                "prompt_prefix": ("STRING", {"default": ""}),
                "prompt_suffix": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
                "color_scheme": (["COLOR_SCHEME_0", "COLOR_SCHEME_1", "COLOR_SCHEME_2", 
                                "COLOR_SCHEME_3", "COLOR_SCHEME_4", "COLOR_SCHEME_5",
                                "COLOR_SCHEME_6", "COLOR_SCHEME_7", "COLOR_SCHEME_8",
                                "COLOR_SCHEME_9", "COLOR_SCHEME_10", "COLOR_SCHEME_11",
                                "COLOR_SCHEME_12", "COLOR_SCHEME_13", "COLOR_SCHEME_14",
                                "COLOR_SCHEME_15", "COLOR_SCHEME_16", "COLOR_SCHEME_17",
                                "COLOR_SCHEME_18", "COLOR_SCHEME_19", "COLOR_SCHEME_20"],),
                "speciality_decor": (["SPECIALITY_DECOR_0", "SPECIALITY_DECOR_1", 
                                    "SPECIALITY_DECOR_2", "SPECIALITY_DECOR_3",
                                    "SPECIALITY_DECOR_4", "SPECIALITY_DECOR_5",
                                    "SPECIALITY_DECOR_6", "SPECIALITY_DECOR_7"],),
                "guidance_scale": ("FLOAT", {"default": None, "min": 1.0, "max": 20.0}),
                "num_inference_steps": ("INT", {"default": None, "min": 1, "max": 75}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4}),
                "scale_factor": ("INT", {"default": 1, "min": 1, "max": 8}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_design"
    CATEGORY = "Decor8 AI"

    def _validate_image(self, image_tensor):
        """Validate image tensor dimensions and values"""
        if not isinstance(image_tensor, torch.Tensor):
            raise ValueError("Input must be a PyTorch tensor")
        if len(image_tensor.shape) not in [3, 4]:  # HWC or BHWC
            raise ValueError(f"Invalid image dimensions: {image_tensor.shape}")
        if image_tensor.max() > 1.0 or image_tensor.min() < 0.0:
            raise ValueError("Image values must be in range [0, 1]")

    def _tensor_to_file(self, image_tensor):
        """Convert PyTorch tensor to file-like object"""
        try:
            self._validate_image(image_tensor)
            
            # Remove batch dimension and keep HWC
            image_tensor = image_tensor.squeeze(0)
            
            # Convert to PIL Image directly from tensor
            image_pil = Image.fromarray((image_tensor.cpu() * 255).byte().numpy(), mode='RGB')
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            image_pil.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
        except Exception as e:
            self.logger.error(f"Error converting tensor to file: {str(e)}")
            raise RuntimeError(f"Failed to convert image: {str(e)}")

    def _url_to_tensor(self, url):
        """Download image from URL and convert to PyTorch tensor"""
        try:
            response = requests.get(url, timeout=10)  # Added timeout
            response.raise_for_status()  # Raises HTTPError for bad responses
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(response.content))
            
            # Convert PIL Image to tensor
            image_tensor = torch.tensor(list(image.getdata()), 
                                      dtype=torch.float32).reshape(image.size[1], image.size[0], -1) / 255.0
            image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension [1, H, W, C]
            
            self._validate_image(image_tensor)
            return image_tensor
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading image from {url}: {str(e)}")
            raise RuntimeError(f"Failed to download image: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error processing image from {url}: {str(e)}")
            raise RuntimeError(f"Failed to process image: {str(e)}")

    def generate_design(self, image, api_key, prompt=None, room_type=None, design_style=None,
                       prompt_prefix=None, prompt_suffix=None, negative_prompt=None,
                       seed=0, color_scheme=None, speciality_decor=None,
                       guidance_scale=None, num_inference_steps=None, num_images=1,
                       scale_factor=1):
        """Generate virtual staging design"""
        try:
            # Validate inputs
            if not api_key:
                raise ValueError("Decor8 AI API key is required")
            if not prompt and (not room_type or not design_style):
                raise ValueError("Either prompt or both room_type and design_style must be provided")
            
            self._validate_image(image)

            # Convert tensor to file
            image_file = self._tensor_to_file(image)

            # Prepare request data
            data = {
                "num_images": num_images,
                "scale_factor": scale_factor
            }
            
            if prompt:
                data["prompt"] = prompt

                if prompt_prefix:
                    data["prompt_prefix"] = prompt_prefix
                if prompt_suffix:
                    data["prompt_suffix"] = prompt_suffix
                if negative_prompt:
                    data["negative_prompt"] = negative_prompt

            else:
                data["room_type"] = room_type
                data["design_style"] = design_style
                if color_scheme:
                    data["color_scheme"] = color_scheme
                if speciality_decor:
                    data["speciality_decor"] = speciality_decor

            if seed > 0:
                data["seed"] = seed

            if guidance_scale:
                data["guidance_scale"] = guidance_scale
            if num_inference_steps:
                data["num_inference_steps"] = num_inference_steps
                

            # Prepare files
            files = {
                'input_image': ('image.png', image_file, 'image/png'),
            }

            # Make API request with timeout
            response = requests.post(
                f"{self.api_base}/generate_designs",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                data=data,
                files=files,
                timeout=30  # 30 second timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("error"):
                raise RuntimeError(f"API error: {result['error']}")

            # Download and convert all generated images to tensors
            images = [self._url_to_tensor(img["url"]) for img in result["info"]["images"]]
            
            # Stack tensors along batch dimension
            images = torch.cat(images, dim=0)
            
            return (images,)
            
        except Exception as e:
            self.logger.error(f"Error in generate_design: {str(e)}")
            raise RuntimeError(f"Failed to generate design: {str(e)}")

NODE_CLASS_MAPPINGS = {
    "VirtualStagingNode": VirtualStagingNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VirtualStagingNode": "Virtual Staging"
} 