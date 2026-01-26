"""Decor8 AI SDK Client.

This module provides a Python client for the Decor8 AI API, enabling virtual staging,
interior design generation, and various image transformation capabilities.

Example:
    >>> from decor8ai import Decor8AI
    >>> client = Decor8AI()  # Uses DECOR8AI_API_KEY env var
    >>> result = client.generate_designs_for_room(
    ...     input_image_url="https://example.com/room.jpg",
    ...     room_type="livingroom",
    ...     design_style="modern"
    ... )
"""

import os
import requests
from typing import Optional, Union, Dict, Any
from urllib.parse import urlparse


# Default configuration
DEFAULT_BASE_URL = "https://api.decor8.ai"


def _is_url(path: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def _load_image_bytes(input_image: Union[str, bytes]) -> bytes:
    """Load image content from various sources.

    Args:
        input_image: File path, URL, or raw bytes.

    Returns:
        Image content as bytes.
    """
    if isinstance(input_image, bytes):
        return input_image
    elif _is_url(input_image):
        response = requests.get(input_image)
        response.raise_for_status()
        return response.content
    else:
        with open(input_image, 'rb') as img_file:
            return img_file.read()


class Decor8AI:
    """Client for Decor8 AI API.

    Args:
        api_key: API key for authentication. If not provided, uses DECOR8AI_API_KEY env var.
        base_url: Base URL for the API. Defaults to https://api.decor8.ai

    Raises:
        ValueError: If no API key is provided or found in environment.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key or os.environ.get('DECOR8AI_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Pass api_key or set DECOR8AI_API_KEY environment variable.")
        self.base_url = base_url.rstrip('/')

    def _get_headers(self, content_type: Optional[str] = None) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        if content_type:
            headers['Content-Type'] = content_type
        return headers

    def _post_json(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request with JSON payload."""
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self._get_headers('application/json'),
            json=data
        )
        return response.json()

    def _post_multipart(self, endpoint: str, files: Dict, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request with multipart form data."""
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self._get_headers(),
            files=files,
            data=data or {}
        )
        return response.json()

    def _build_payload(self, required: Dict[str, Any], optional: Dict[str, Any]) -> Dict[str, Any]:
        """Build request payload from required and optional parameters."""
        payload = dict(required)
        for key, value in optional.items():
            if value is not None:
                payload[key] = value
        return payload

    # -------------------------------------------------------------------------
    # Virtual Staging & Design Generation
    # -------------------------------------------------------------------------

    def generate_designs_for_room(
        self,
        input_image_url: str,
        room_type: str,
        design_style: str,
        num_images: int = 1,
        *,
        scale_factor: Optional[int] = None,
        color_scheme: Optional[str] = None,
        speciality_decor: Optional[str] = None,
        mask_info: Optional[str] = None,
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        num_inference_steps: Optional[int] = None,
        design_style_image_url: Optional[str] = None,
        design_style_image_strength: Optional[float] = None,
        design_creativity: Optional[float] = None,
        webhooks_data: Optional[str] = None,
        decor_items: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate virtual staging designs for a room image.

        Args:
            input_image_url: URL of the input room image.
            room_type: Type of room (e.g., 'livingroom', 'bedroom').
            design_style: Design aesthetic (e.g., 'modern', 'scandinavian').
            num_images: Number of designs to generate (1-4).
            scale_factor: Resolution multiplier (1-8).
            color_scheme: Predefined color palette (e.g., 'COLOR_SCHEME_0').
            speciality_decor: Seasonal/thematic decor (e.g., 'SPECIALITY_DECOR_0').
            mask_info: Masking data from previous requests.
            prompt: Custom text generation directive.
            seed: Random seed for reproducibility.
            guidance_scale: Prompt adherence (1-20, default 15).
            num_inference_steps: Quality/speed balance (1-75, default 50).
            design_style_image_url: Style reference image URL.
            design_style_image_strength: Style influence (0-1, default 0.82).
            design_creativity: Creative alterations level (0-1, default 0.39).
            webhooks_data: Async callback configuration.
            decor_items: JSON string specifying furniture/accessories.

        Returns:
            API response with generated images.
        """
        payload = self._build_payload(
            required={
                'input_image_url': input_image_url,
                'room_type': room_type,
                'design_style': design_style,
                'num_images': num_images,
            },
            optional={
                'scale_factor': scale_factor,
                'color_scheme': color_scheme,
                'speciality_decor': speciality_decor,
                'mask_info': mask_info,
                'prompt': prompt,
                'seed': seed,
                'guidance_scale': guidance_scale,
                'num_inference_steps': num_inference_steps,
                'design_style_image_url': design_style_image_url,
                'design_style_image_strength': design_style_image_strength,
                'design_creativity': design_creativity,
                'webhooks_data': webhooks_data,
                'decor_items': decor_items,
            }
        )
        return self._post_json('/generate_designs_for_room', payload)

    def generate_inspirational_designs(
        self,
        room_type: str,
        design_style: str,
        num_images: int = 1,
        *,
        color_scheme: Optional[str] = None,
        speciality_decor: Optional[str] = None,
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        num_inference_steps: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate inspirational room designs without an input image.

        Args:
            room_type: Type of room (e.g., 'livingroom', 'bedroom').
            design_style: Design aesthetic (e.g., 'modern', 'scandinavian').
            num_images: Number of designs to generate (1-4).
            color_scheme: Predefined color palette.
            speciality_decor: Seasonal/thematic decor.
            prompt: Custom text generation directive.
            seed: Random seed for reproducibility.
            guidance_scale: Prompt adherence (1-20, default 15).
            num_inference_steps: Quality/speed balance (1-75, default 35).

        Returns:
            API response with generated images.
        """
        payload = self._build_payload(
            required={
                'room_type': room_type,
                'design_style': design_style,
                'num_images': num_images,
            },
            optional={
                'color_scheme': color_scheme,
                'speciality_decor': speciality_decor,
                'prompt': prompt,
                'seed': seed,
                'guidance_scale': guidance_scale,
                'num_inference_steps': num_inference_steps,
            }
        )
        return self._post_json('/generate_inspirational_designs', payload)

    def generate_designs(
        self,
        input_image: Union[str, bytes],
        room_type: str,
        design_style: str,
        num_images: int = 1,
        *,
        num_captions: Optional[int] = None,
        keep_original_dimensions: bool = False,
        color_scheme: Optional[str] = None,
        speciality_decor: Optional[str] = None,
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        num_inference_steps: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate designs using multipart file upload (legacy method).

        For new integrations, prefer generate_designs_for_room() with image URLs.

        Args:
            input_image: File path, URL, or bytes of input image.
            room_type: Type of room.
            design_style: Design aesthetic.
            num_images: Number of designs to generate (1-4).
            num_captions: Number of captions to generate.
            keep_original_dimensions: Preserve original image dimensions.
            color_scheme: Predefined color palette.
            speciality_decor: Seasonal/thematic decor.
            prompt: Custom text directive.
            seed: Random seed.
            guidance_scale: Prompt adherence.
            num_inference_steps: Quality/speed balance.

        Returns:
            API response with generated images.
        """
        image_bytes = _load_image_bytes(input_image)
        files = {'input_image': ('input_image.jpg', image_bytes)}

        data = {
            'room_type': room_type,
            'design_style': design_style,
            'num_images': num_images,
        }

        if num_captions is not None:
            data['num_captions'] = num_captions
        if keep_original_dimensions:
            data['keep_original_dimensions'] = keep_original_dimensions
        if color_scheme:
            data['color_scheme'] = color_scheme
        if speciality_decor:
            data['speciality_decor'] = speciality_decor
        if prompt:
            data['prompt'] = prompt
        if seed is not None:
            data['seed'] = seed
        if guidance_scale:
            data['guidance_scale'] = guidance_scale
        if num_inference_steps:
            data['num_inference_steps'] = num_inference_steps

        return self._post_multipart('/generate_designs', files, data)

    # -------------------------------------------------------------------------
    # Wall & Surface Modifications
    # -------------------------------------------------------------------------

    def prime_walls_for_room(self, input_image_url: str) -> Dict[str, Any]:
        """Prepare room walls for virtual staging by priming them.

        Args:
            input_image_url: URL of the room image.

        Returns:
            API response with primed image URL.
        """
        return self._post_json('/prime_walls_for_room', {'input_image_url': input_image_url})

    def prime_the_room_walls(self, input_image: Union[str, bytes]) -> Dict[str, Any]:
        """Prime room walls using file upload (legacy method).

        For new integrations, prefer prime_walls_for_room() with image URLs.

        Args:
            input_image: File path, URL, or bytes of input image.

        Returns:
            API response with primed image.
        """
        image_bytes = _load_image_bytes(input_image)
        files = {'input_image': ('input_image.jpg', image_bytes)}
        return self._post_multipart('/prime_the_room_walls', files)

    def change_wall_color(self, input_image_url: str, wall_color_hex_code: str) -> Dict[str, Any]:
        """Change the wall color in a room image.

        Args:
            input_image_url: URL of the room image (HTTPS or data URL).
            wall_color_hex_code: Desired wall color in hex format (e.g., '#FF5733').

        Returns:
            API response with recolored image.
        """
        return self._post_json('/change_wall_color', {
            'input_image_url': input_image_url,
            'wall_color_hex_code': wall_color_hex_code,
        })

    def change_kitchen_cabinets_color(
        self,
        input_image_url: str,
        cabinet_color_hex_code: str
    ) -> Dict[str, Any]:
        """Change kitchen cabinet colors in an image.

        Args:
            input_image_url: URL of the kitchen image.
            cabinet_color_hex_code: Desired cabinet color in hex format (e.g., '#FFFFFF').

        Returns:
            API response with recolored cabinet image.
        """
        return self._post_json('/change_kitchen_cabinets_color', {
            'input_image_url': input_image_url,
            'cabinet_color_hex_code': cabinet_color_hex_code,
        })

    # -------------------------------------------------------------------------
    # Remodeling
    # -------------------------------------------------------------------------

    def remodel_kitchen(
        self,
        input_image_url: str,
        design_style: str,
        num_images: int = 1,
        scale_factor: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate kitchen remodel designs.

        Args:
            input_image_url: URL of the current kitchen image.
            design_style: Design aesthetic for the remodel.
            num_images: Number of designs to generate (1-4).
            scale_factor: Resolution multiplier (1-4).

        Returns:
            API response with remodeled kitchen images.
        """
        payload = self._build_payload(
            required={
                'input_image_url': input_image_url,
                'design_style': design_style,
            },
            optional={
                'num_images': num_images if num_images != 1 else None,
                'scale_factor': scale_factor,
            }
        )
        return self._post_json('/remodel_kitchen', payload)

    def remodel_bathroom(
        self,
        input_image_url: str,
        design_style: str,
        num_images: int = 1,
        scale_factor: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate bathroom remodel designs.

        Args:
            input_image_url: URL of the current bathroom image.
            design_style: Design aesthetic for the remodel.
            num_images: Number of designs to generate (1-4).
            scale_factor: Resolution multiplier (1-4).

        Returns:
            API response with remodeled bathroom images.
        """
        payload = self._build_payload(
            required={
                'input_image_url': input_image_url,
                'design_style': design_style,
            },
            optional={
                'num_images': num_images if num_images != 1 else None,
                'scale_factor': scale_factor,
            }
        )
        return self._post_json('/remodel_bathroom', payload)

    # -------------------------------------------------------------------------
    # Exterior & Landscaping
    # -------------------------------------------------------------------------

    def replace_sky_behind_house(self, input_image_url: str, sky_type: str) -> Dict[str, Any]:
        """Replace the sky in an exterior property photo.

        Args:
            input_image_url: URL of the exterior image.
            sky_type: Type of sky ('day', 'dusk', or 'night').

        Returns:
            API response with sky-replaced image.
        """
        return self._post_json('/replace_sky_behind_house', {
            'input_image_url': input_image_url,
            'sky_type': sky_type,
        })

    def generate_landscaping_designs(
        self,
        input_image_url: str,
        yard_type: str,
        garden_style: str,
        num_images: int = 1,
    ) -> Dict[str, Any]:
        """Generate landscaping designs for a yard (Beta).

        Args:
            input_image_url: URL of the yard image.
            yard_type: Type of yard ('Front Yard', 'Backyard', or 'Side Yard').
            garden_style: Garden design style (e.g., 'japanese_zen', 'mediterranean').
            num_images: Number of designs to generate (1-4).

        Returns:
            API response with landscaped yard images.
        """
        payload = self._build_payload(
            required={
                'input_image_url': input_image_url,
                'yard_type': yard_type,
                'garden_style': garden_style,
            },
            optional={
                'num_images': num_images if num_images != 1 else None,
            }
        )
        return self._post_json('/generate_landscaping_designs', payload)

    # -------------------------------------------------------------------------
    # Image Processing
    # -------------------------------------------------------------------------

    def remove_objects_from_room(
        self,
        input_image_url: str,
        mask_image_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Remove objects/furniture from a room image.

        Args:
            input_image_url: URL of the room image.
            mask_image_url: Optional black/white mask specifying areas to remove.

        Returns:
            API response with cleaned room image.
        """
        payload = {'input_image_url': input_image_url}
        if mask_image_url:
            payload['mask_image_url'] = mask_image_url
        return self._post_json('/remove_objects_from_room', payload)

    def upscale_image(
        self,
        input_image: Union[str, bytes],
        scale_factor: int = 2
    ) -> Dict[str, Any]:
        """Upscale an image to higher resolution.

        Args:
            input_image: File path, URL, or bytes of input image (max 4MB).
            scale_factor: Resolution multiplier (1-8).

        Returns:
            API response with base64-encoded upscaled image.
        """
        image_bytes = _load_image_bytes(input_image)
        files = {'input_image': ('input_image.jpg', image_bytes)}
        data = {'scale_factor': scale_factor}
        return self._post_multipart('/upscale_image', files, data)

    # -------------------------------------------------------------------------
    # 3D & Rendering
    # -------------------------------------------------------------------------

    def sketch_to_3d_render(
        self,
        input_image_url: str,
        design_style: str,
        num_images: int = 1,
        scale_factor: Optional[int] = None,
        render_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convert a sketch or floor plan to a 3D rendered image.

        Args:
            input_image_url: URL of the sketch/floor plan image.
            design_style: Design aesthetic for the render.
            num_images: Number of renders to generate (1-4).
            scale_factor: Resolution multiplier (1-8).
            render_type: Render perspective ('perspective' or 'isometric').

        Returns:
            API response with 3D rendered images.
        """
        payload = self._build_payload(
            required={
                'input_image_url': input_image_url,
                'design_style': design_style,
            },
            optional={
                'num_images': num_images if num_images != 1 else None,
                'scale_factor': scale_factor,
                'render_type': render_type,
            }
        )
        return self._post_json('/sketch_to_3d_render', payload)


# =============================================================================
# Module-level functions for backward compatibility
# =============================================================================

# Module-level client instance (lazy-loaded)
_default_client: Optional[Decor8AI] = None


def _get_default_client() -> Decor8AI:
    """Get or create the default client instance."""
    global _default_client
    if _default_client is None:
        _default_client = Decor8AI()
    return _default_client


def prime_the_room_walls(input_image: Union[str, bytes]) -> Dict[str, Any]:
    """Prime room walls using file upload. See Decor8AI.prime_the_room_walls()."""
    return _get_default_client().prime_the_room_walls(input_image)


def prime_walls_for_room(input_image_url: str) -> Dict[str, Any]:
    """Prime room walls from URL. See Decor8AI.prime_walls_for_room()."""
    return _get_default_client().prime_walls_for_room(input_image_url)


def replace_sky_behind_house(input_image_url: str, sky_type: str) -> Dict[str, Any]:
    """Replace sky in exterior photo. See Decor8AI.replace_sky_behind_house()."""
    return _get_default_client().replace_sky_behind_house(input_image_url, sky_type)


def generate_designs(
    input_image: Union[str, bytes],
    room_type: str = None,
    design_style: str = None,
    num_captions: int = None,
    num_images: int = 1,
    keep_original_dimensions: bool = False,
    color_scheme: str = None,
    speciality_decor: str = None,
    prompt: str = None,
    prompt_prefix: str = None,
    prompt_suffix: str = None,
    negative_prompt: str = None,
    seed: int = None,
    guidance_scale: float = None,
    num_inference_steps: int = None,
) -> Dict[str, Any]:
    """Generate designs from file upload. See Decor8AI.generate_designs()."""
    return _get_default_client().generate_designs(
        input_image=input_image,
        room_type=room_type,
        design_style=design_style,
        num_images=num_images,
        num_captions=num_captions,
        keep_original_dimensions=keep_original_dimensions,
        color_scheme=color_scheme,
        speciality_decor=speciality_decor,
        prompt=prompt,
        seed=seed,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
    )


def generate_designs_for_room(
    input_image_url: str,
    mask_info: str = None,
    room_type: str = None,
    design_style: str = None,
    num_images: int = 1,
    color_scheme: str = None,
    speciality_decor: str = None,
    keep_original_floor: bool = False,
    prompt: str = None,
    prompt_prefix: str = None,
    prompt_suffix: str = None,
    negative_prompt: str = None,
    seed: int = None,
    guidance_scale: float = None,
    num_inference_steps: int = None,
) -> Dict[str, Any]:
    """Generate designs from URL. See Decor8AI.generate_designs_for_room()."""
    return _get_default_client().generate_designs_for_room(
        input_image_url=input_image_url,
        room_type=room_type,
        design_style=design_style,
        num_images=num_images,
        mask_info=mask_info,
        color_scheme=color_scheme,
        speciality_decor=speciality_decor,
        prompt=prompt,
        seed=seed,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
    )


def generate_inspirational_designs(
    room_type: str = None,
    design_style: str = None,
    num_images: int = 1,
    color_scheme: str = None,
    speciality_decor: str = None,
    prompt: str = None,
    prompt_prefix: str = None,
    prompt_suffix: str = None,
    negative_prompt: str = None,
    seed: int = None,
    guidance_scale: float = None,
    num_inference_steps: int = None,
) -> Dict[str, Any]:
    """Generate inspirational designs. See Decor8AI.generate_inspirational_designs()."""
    return _get_default_client().generate_inspirational_designs(
        room_type=room_type,
        design_style=design_style,
        num_images=num_images,
        color_scheme=color_scheme,
        speciality_decor=speciality_decor,
        prompt=prompt,
        seed=seed,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
    )


def generate_image_captions(design_style: str, room_type: str, num_captions: int) -> Dict[str, Any]:
    """Generate image captions (deprecated - verify API support)."""
    client = _get_default_client()
    return client._post_json('/generate_image_captions', {
        'room_type': room_type,
        'design_style': design_style,
        'num_captions': num_captions,
    })


def upscale_image(input_image: Union[str, bytes], scale_factor: int = 2) -> Dict[str, Any]:
    """Upscale an image. See Decor8AI.upscale_image()."""
    return _get_default_client().upscale_image(input_image, scale_factor)


def remove_objects_from_room(input_image_url: str, mask_image_url: str = None) -> Dict[str, Any]:
    """Remove objects from room. See Decor8AI.remove_objects_from_room()."""
    return _get_default_client().remove_objects_from_room(input_image_url, mask_image_url)


def change_wall_color(input_image_url: str, wall_color_hex_code: str) -> Dict[str, Any]:
    """Change wall color. See Decor8AI.change_wall_color()."""
    return _get_default_client().change_wall_color(input_image_url, wall_color_hex_code)


def change_kitchen_cabinets_color(input_image_url: str, cabinet_color_hex_code: str) -> Dict[str, Any]:
    """Change kitchen cabinet color. See Decor8AI.change_kitchen_cabinets_color()."""
    return _get_default_client().change_kitchen_cabinets_color(input_image_url, cabinet_color_hex_code)


def generate_landscaping_designs(
    input_image_url: str,
    yard_type: str,
    garden_style: str,
    num_images: int = 1,
) -> Dict[str, Any]:
    """Generate landscaping designs. See Decor8AI.generate_landscaping_designs()."""
    return _get_default_client().generate_landscaping_designs(
        input_image_url, yard_type, garden_style, num_images
    )


def remodel_kitchen(
    input_image_url: str,
    design_style: str,
    num_images: int = 1,
    scale_factor: int = None,
) -> Dict[str, Any]:
    """Remodel kitchen. See Decor8AI.remodel_kitchen()."""
    return _get_default_client().remodel_kitchen(
        input_image_url, design_style, num_images, scale_factor
    )


def remodel_bathroom(
    input_image_url: str,
    design_style: str,
    num_images: int = 1,
    scale_factor: int = None,
) -> Dict[str, Any]:
    """Remodel bathroom. See Decor8AI.remodel_bathroom()."""
    return _get_default_client().remodel_bathroom(
        input_image_url, design_style, num_images, scale_factor
    )


def sketch_to_3d_render(
    input_image_url: str,
    design_style: str,
    num_images: int = 1,
    scale_factor: int = None,
    render_type: str = None,
) -> Dict[str, Any]:
    """Convert sketch to 3D render. See Decor8AI.sketch_to_3d_render()."""
    return _get_default_client().sketch_to_3d_render(
        input_image_url, design_style, num_images, scale_factor, render_type
    )
