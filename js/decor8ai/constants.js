/**
 * Constants and enums for Decor8 AI SDK.
 */

// Room types supported by the API
const ROOM_TYPES = [
    "livingroom", "kitchen", "diningroom", "bedroom", "bathroom",
    "kidsroom", "familyroom", "readingnook", "sunroom", "walkincloset",
    "mudroom", "toyroom", "office", "foyer", "powderroom", "laundryroom",
    "gym", "basement", "garage", "balcony", "cafe", "homebar",
    "study_room", "front_porch", "back_porch", "back_patio", "openplan",
    "boardroom", "meetingroom", "openworkspace", "privateoffice"
];

// Design styles supported by the API
const DESIGN_STYLES = [
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
];

// Color schemes (predefined palettes)
const COLOR_SCHEMES = Array.from({ length: 21 }, (_, i) => `COLOR_SCHEME_${i}`);

// Specialty decor options (seasonal/thematic)
const SPECIALITY_DECORS = Array.from({ length: 8 }, (_, i) => `SPECIALITY_DECOR_${i}`);

// Sky types for sky replacement
const SKY_TYPES = ["day", "dusk", "night"];

// Yard types for landscaping
const YARD_TYPES = ["Front Yard", "Backyard", "Side Yard"];

// Garden styles for landscaping
const GARDEN_STYLES = [
    "japanese_zen", "mediterranean", "english_cottage", "tropical", "desert",
    "modern_minimalist", "french_formal", "coastal", "woodland", "prairie",
    "rock_garden", "water_garden", "herb_garden", "cutting_garden", "pollinator",
    "xeriscape", "edible_landscape", "moon_garden", "rain_garden", "sensory",
    "native_plant", "cottage_style", "formal_parterre", "naturalistic",
    "contemporary", "asian_fusion", "rustic_farmhouse", "urban_modern",
    "sustainable", "wildlife_habitat", "four_season"
];

// Render types for sketch to 3D
const RENDER_TYPES = ["perspective", "isometric"];

module.exports = {
    ROOM_TYPES,
    DESIGN_STYLES,
    COLOR_SCHEMES,
    SPECIALITY_DECORS,
    SKY_TYPES,
    YARD_TYPES,
    GARDEN_STYLES,
    RENDER_TYPES
};
