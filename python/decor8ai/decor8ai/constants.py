"""Constants and enums for Decor8 AI SDK."""

# Room types supported by the API
ROOM_TYPES = [
    "LIVINGROOM", "KITCHEN", "DININGROOM", "BEDROOM", "BATHROOM",
    "KIDSROOM", "FAMILYROOM", "READINGNOOK", "SUNROOM", "WALKINCLOSET",
    "MUDROOM", "TOYROOM", "OFFICE", "FOYER", "POWDERROOM", "LAUNDRYROOM",
    "GYM", "BASEMENT", "GARAGE", "BALCONY", "CAFE", "HOMEBAR",
    "STUDY_ROOM", "FRONT_PORCH", "BACK_PORCH", "BACK_PATIO", "OPENPLAN",
    "BOARDROOM", "MEETINGROOM", "OPENWORKSPACE", "PRIVATEOFFICE"
]

# Design styles supported by the API
DESIGN_STYLES = [
    "MINIMALIST", "SCANDINAVIAN", "INDUSTRIAL", "BOHO", "TRADITIONAL",
    "ARTDECO", "MIDCENTURYMODERN", "COASTAL", "TROPICAL", "ECLECTIC",
    "CONTEMPORARY", "FRENCHCOUNTRY", "RUSTIC", "SHABBYCHIC", "VINTAGE",
    "COUNTRY", "MODERN", "ASIAN_ZEN", "HOLLYWOODREGENCY", "BAUHAUS",
    "MEDITERRANEAN", "FARMHOUSE", "VICTORIAN", "GOTHIC", "MOROCCAN",
    "SOUTHWESTERN", "TRANSITIONAL", "MAXIMALIST", "ARABIC", "JAPANDI",
    "RETROFUTURISM", "ARTNOUVEAU", "URBANMODERN", "WABI_SABI",
    "GRANDMILLENNIAL", "COASTALGRANDMOTHER", "NEWTRADITIONAL", "COTTAGECORE",
    "LUXEMODERN", "HIGH_TECH", "ORGANICMODERN", "TUSCAN", "CABIN",
    "DESERTMODERN", "GLOBAL", "INDUSTRIALCHIC", "MODERNFARMHOUSE",
    "EUROPEANCLASSIC", "NEOTRADITIONAL", "WARMMINIMALIST"
]

# Color schemes (predefined palettes)
COLOR_SCHEMES = [f"COLOR_SCHEME_{i}" for i in range(21)]

# Specialty decor options (seasonal/thematic)
SPECIALITY_DECORS = [f"SPECIALITY_DECOR_{i}" for i in range(8)]

# Sky types for sky replacement
SKY_TYPES = ["DAY", "DUSK", "NIGHT"]

# Yard types for landscaping
YARD_TYPES = ["FRONT_YARD", "BACKYARD", "SIDE_YARD"]

# Garden styles for landscaping
GARDEN_STYLES = [
    "JAPANESE_ZEN", "MEDITERRANEAN", "ENGLISH_COTTAGE", "TROPICAL", "DESERT",
    "MODERN_MINIMALIST", "FRENCH_FORMAL", "COASTAL", "WOODLAND", "PRAIRIE",
    "ROCK_GARDEN", "WATER_GARDEN", "HERB_GARDEN", "CUTTING_GARDEN", "POLLINATOR",
    "XERISCAPE", "EDIBLE_LANDSCAPE", "MOON_GARDEN", "RAIN_GARDEN", "SENSORY",
    "NATIVE_PLANT", "COTTAGE_STYLE", "FORMAL_PARTERRE", "NATURALISTIC",
    "CONTEMPORARY", "ASIAN_FUSION", "RUSTIC_FARMHOUSE", "URBAN_MODERN",
    "SUSTAINABLE", "WILDLIFE_HABITAT", "FOUR_SEASON"
]

# Render types for sketch to 3D
RENDER_TYPES = ["PERSPECTIVE", "ISOMETRIC"]

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
