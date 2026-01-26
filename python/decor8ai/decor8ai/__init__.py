"""Decor8 AI SDK for Python.

Example usage:
    # Class-based (recommended)
    from decor8ai import Decor8AI
    client = Decor8AI(api_key="your-key")  # or use DECOR8AI_API_KEY env var
    result = client.generate_designs_for_room(...)

    # Module-level functions (backward compatible)
    from decor8ai import generate_designs_for_room
    result = generate_designs_for_room(...)
"""

from .client import (
    # Main client class
    Decor8AI,
    # Module-level functions for backward compatibility
    prime_the_room_walls,
    prime_walls_for_room,
    generate_designs,
    generate_designs_for_room,
    generate_inspirational_designs,
    generate_image_captions,
    upscale_image,
    remove_objects_from_room,
    replace_sky_behind_house,
    # New functions
    change_wall_color,
    change_kitchen_cabinets_color,
    generate_landscaping_designs,
    remodel_kitchen,
    remodel_bathroom,
    sketch_to_3d_render,
)

from .constants import (
    ROOM_TYPES,
    DESIGN_STYLES,
    COLOR_SCHEMES,
    SPECIALITY_DECORS,
    SKY_TYPES,
    YARD_TYPES,
    GARDEN_STYLES,
    RENDER_TYPES,
)

__version__ = "0.3.0"
__all__ = [
    # Client class
    "Decor8AI",
    # Functions
    "prime_the_room_walls",
    "prime_walls_for_room",
    "generate_designs",
    "generate_designs_for_room",
    "generate_inspirational_designs",
    "generate_image_captions",
    "upscale_image",
    "remove_objects_from_room",
    "replace_sky_behind_house",
    "change_wall_color",
    "change_kitchen_cabinets_color",
    "generate_landscaping_designs",
    "remodel_kitchen",
    "remodel_bathroom",
    "sketch_to_3d_render",
    # Constants
    "ROOM_TYPES",
    "DESIGN_STYLES",
    "COLOR_SCHEMES",
    "SPECIALITY_DECORS",
    "SKY_TYPES",
    "YARD_TYPES",
    "GARDEN_STYLES",
    "RENDER_TYPES",
]
