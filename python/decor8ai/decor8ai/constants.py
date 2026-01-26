"""Constants and enums for Decor8 AI SDK."""

# Room types supported by the API
ROOM_TYPES = [
    "livingroom", "kitchen", "diningroom", "bedroom", "bathroom",
    "kidsroom", "familyroom", "readingnook", "sunroom", "walkincloset",
    "mudroom", "toyroom", "office", "foyer", "powderroom", "laundryroom",
    "gym", "basement", "garage", "balcony", "cafe", "homebar",
    "study_room", "front_porch", "back_porch", "back_patio", "openplan",
    "boardroom", "meetingroom", "openworkspace", "privateoffice"
]

# Design styles supported by the API
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

# Color schemes (predefined palettes)
COLOR_SCHEMES = [f"COLOR_SCHEME_{i}" for i in range(21)]

# Specialty decor options (seasonal/thematic)
SPECIALITY_DECORS = [f"SPECIALITY_DECOR_{i}" for i in range(8)]

# Sky types for sky replacement
SKY_TYPES = ["day", "dusk", "night"]

# Yard types for landscaping
YARD_TYPES = ["Front Yard", "Backyard", "Side Yard"]

# Garden styles for landscaping
GARDEN_STYLES = [
    "japanese_zen", "mediterranean", "english_cottage", "tropical", "desert",
    "modern_minimalist", "french_formal", "coastal", "woodland", "prairie",
    "rock_garden", "water_garden", "herb_garden", "cutting_garden", "pollinator",
    "xeriscape", "edible_landscape", "moon_garden", "rain_garden", "sensory",
    "native_plant", "cottage_style", "formal_parterre", "naturalistic",
    "contemporary", "asian_fusion", "rustic_farmhouse", "urban_modern",
    "sustainable", "wildlife_habitat", "four_season"
]

# Render types for sketch to 3D
RENDER_TYPES = ["perspective", "isometric"]

# API endpoints
ENDPOINTS = {
    "prime_the_room_walls": "/prime_the_room_walls",
    "prime_walls_for_room": "/prime_walls_for_room",
    "generate_designs": "/generate_designs",
    "generate_designs_for_room": "/generate_designs_for_room",
    "generate_inspirational_designs": "/generate_inspirational_designs",
    "upscale_image": "/upscale_image",
    "remove_objects_from_room": "/remove_objects_from_room",
    "replace_sky_behind_house": "/replace_sky_behind_house",
    "change_wall_color": "/change_wall_color",
    "change_kitchen_cabinets_color": "/change_kitchen_cabinets_color",
    "generate_landscaping_designs": "/generate_landscaping_designs",
    "remodel_kitchen": "/remodel_kitchen",
    "remodel_bathroom": "/remodel_bathroom",
    "sketch_to_3d_render": "/sketch_to_3d_render",
}
