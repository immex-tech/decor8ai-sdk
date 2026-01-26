const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

/**
 * Decor8 AI SDK Client for Node.js
 *
 * @example
 * const Decor8AI = require('decor8ai');
 * const client = new Decor8AI(); // Uses DECOR8AI_API_KEY env var
 * const result = await client.generateDesignsForRoom({
 *     inputImageUrl: 'https://example.com/room.jpg',
 *     roomType: 'livingroom',
 *     designStyle: 'modern'
 * });
 */
class Decor8AI {
    /**
     * Create a Decor8AI client
     * @param {string} [baseUrl='https://api.decor8.ai'] - API base URL
     * @throws {Error} If DECOR8AI_API_KEY is not set
     */
    constructor(baseUrl = 'https://api.decor8.ai') {
        this.apiKey = process.env.DECOR8AI_API_KEY;
        if (!this.apiKey) {
            throw new Error("DECOR8AI_API_KEY environment variable is not set.");
        }
        this.baseUrl = baseUrl.replace(/\/$/, '');
    }

    /**
     * Create form data from image input
     * @private
     */
    async createFormData(inputImage) {
        let formData = new FormData();
        if (typeof inputImage === 'string') {
            if (inputImage.startsWith('http')) {
                const response = await axios.get(inputImage, { responseType: 'arraybuffer' });
                const buffer = Buffer.from(response.data, 'binary');
                formData.append('input_image', buffer, 'input_image.jpg');
            } else {
                formData.append('input_image', fs.createReadStream(inputImage), 'input_image.jpg');
            }
        } else if (Buffer.isBuffer(inputImage)) {
            formData.append('input_image', inputImage, 'input_image.jpg');
        }
        return formData;
    }

    /**
     * Make a POST request with JSON payload
     * @private
     */
    async postJson(endpoint, data) {
        const response = await axios.post(`${this.baseUrl}${endpoint}`, data, {
            headers: {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    }

    /**
     * Make a POST request with multipart form data
     * @private
     */
    async postMultipart(endpoint, formData, extraData = {}) {
        for (const [key, value] of Object.entries(extraData)) {
            if (value !== null && value !== undefined) {
                formData.append(key, String(value));
            }
        }
        const response = await axios.post(`${this.baseUrl}${endpoint}`, formData, {
            headers: {
                Authorization: `Bearer ${this.apiKey}`,
                ...formData.getHeaders()
            }
        });
        return response.data;
    }

    // =========================================================================
    // Virtual Staging & Design Generation
    // =========================================================================

    /**
     * Generate virtual staging designs for a room image
     * @param {Object} options
     * @param {string} options.inputImageUrl - URL of the input room image
     * @param {string} options.roomType - Type of room (e.g., 'livingroom', 'bedroom')
     * @param {string} options.designStyle - Design aesthetic (e.g., 'modern', 'scandinavian')
     * @param {number} [options.numImages=1] - Number of designs to generate (1-4)
     * @param {number} [options.scaleFactor] - Resolution multiplier (1-8)
     * @param {string} [options.colorScheme] - Predefined color palette
     * @param {string} [options.specialityDecor] - Seasonal/thematic decor
     * @param {string} [options.maskInfo] - Masking data from previous requests
     * @param {string} [options.prompt] - Custom text generation directive
     * @param {number} [options.seed] - Random seed for reproducibility
     * @param {number} [options.guidanceScale] - Prompt adherence (1-20, default 15)
     * @param {number} [options.numInferenceSteps] - Quality/speed balance (1-75, default 50)
     * @param {string} [options.designStyleImageUrl] - Style reference image URL
     * @param {number} [options.designStyleImageStrength] - Style influence (0-1, default 0.82)
     * @param {number} [options.designCreativity] - Creative alterations level (0-1, default 0.39)
     * @param {string} [options.webhooksData] - Async callback configuration
     * @param {string} [options.decorItems] - JSON string specifying furniture/accessories
     * @returns {Promise<Object>} API response with generated images
     */
    async generateDesignsForRoom(options) {
        const {
            inputImageUrl, roomType, designStyle, numImages = 1,
            scaleFactor, colorScheme, specialityDecor, maskInfo,
            prompt, seed, guidanceScale, numInferenceSteps,
            designStyleImageUrl, designStyleImageStrength, designCreativity,
            webhooksData, decorItems
        } = options;

        const payload = {
            input_image_url: inputImageUrl,
            room_type: roomType,
            design_style: designStyle,
            num_images: numImages
        };

        if (scaleFactor) payload.scale_factor = scaleFactor;
        if (colorScheme) payload.color_scheme = colorScheme;
        if (specialityDecor) payload.speciality_decor = specialityDecor;
        if (maskInfo) payload.mask_info = maskInfo;
        if (prompt) payload.prompt = prompt;
        if (seed !== undefined && seed !== null) payload.seed = seed;
        if (guidanceScale) payload.guidance_scale = guidanceScale;
        if (numInferenceSteps) payload.num_inference_steps = numInferenceSteps;
        if (designStyleImageUrl) payload.design_style_image_url = designStyleImageUrl;
        if (designStyleImageStrength) payload.design_style_image_strength = designStyleImageStrength;
        if (designCreativity) payload.design_creativity = designCreativity;
        if (webhooksData) payload.webhooks_data = webhooksData;
        if (decorItems) payload.decor_items = decorItems;

        return this.postJson('/generate_designs_for_room', payload);
    }

    /**
     * Generate inspirational room designs without an input image
     * @param {Object} options
     * @param {string} options.roomType - Type of room
     * @param {string} options.designStyle - Design aesthetic
     * @param {number} [options.numImages=1] - Number of designs to generate (1-4)
     * @param {string} [options.colorScheme] - Predefined color palette
     * @param {string} [options.specialityDecor] - Seasonal/thematic decor
     * @param {string} [options.prompt] - Custom text generation directive
     * @param {number} [options.seed] - Random seed for reproducibility
     * @param {number} [options.guidanceScale] - Prompt adherence (1-20, default 15)
     * @param {number} [options.numInferenceSteps] - Quality/speed balance (1-75, default 35)
     * @returns {Promise<Object>} API response with generated images
     */
    async generateInspirationalDesigns(options) {
        const {
            roomType, designStyle, numImages = 1,
            colorScheme, specialityDecor, prompt,
            seed, guidanceScale, numInferenceSteps
        } = options;

        const payload = {
            room_type: roomType,
            design_style: designStyle,
            num_images: numImages
        };

        if (colorScheme) payload.color_scheme = colorScheme;
        if (specialityDecor) payload.speciality_decor = specialityDecor;
        if (prompt) payload.prompt = prompt;
        if (seed !== undefined && seed !== null) payload.seed = seed;
        if (guidanceScale) payload.guidance_scale = guidanceScale;
        if (numInferenceSteps) payload.num_inference_steps = numInferenceSteps;

        return this.postJson('/generate_inspirational_designs', payload);
    }

    /**
     * Generate designs using multipart file upload (legacy method)
     * @param {string|Buffer} inputImage - File path, URL, or Buffer
     * @param {string} roomType - Type of room
     * @param {string} designStyle - Design aesthetic
     * @param {Object} [options] - Additional options
     * @returns {Promise<Object>} API response with generated images
     */
    async generateDesigns(inputImage, roomType, designStyle, options = {}) {
        const formData = await this.createFormData(inputImage);
        const data = {
            room_type: roomType,
            design_style: designStyle,
            num_images: options.numImages || 1,
            ...options.numCaptions && { num_captions: options.numCaptions },
            ...options.colorScheme && { color_scheme: options.colorScheme },
            ...options.specialityDecor && { speciality_decor: options.specialityDecor },
            ...options.prompt && { prompt: options.prompt },
            ...(options.seed !== undefined) && { seed: options.seed },
            ...options.guidanceScale && { guidance_scale: options.guidanceScale },
            ...options.numInferenceSteps && { num_inference_steps: options.numInferenceSteps }
        };
        return this.postMultipart('/generate_designs', formData, data);
    }

    // =========================================================================
    // Wall & Surface Modifications
    // =========================================================================

    /**
     * Prime room walls for virtual staging from URL
     * @param {string} inputImageUrl - URL of the room image
     * @returns {Promise<Object>} API response with primed image URL
     */
    async primeWallsForRoom(inputImageUrl) {
        return this.postJson('/prime_walls_for_room', { input_image_url: inputImageUrl });
    }

    /**
     * Prime room walls using file upload (legacy method)
     * @param {string|Buffer} inputImage - File path, URL, or Buffer
     * @returns {Promise<Object>} API response with primed image
     */
    async primeTheRoomWalls(inputImage) {
        const formData = await this.createFormData(inputImage);
        return this.postMultipart('/prime_the_room_walls', formData);
    }

    /**
     * Change the wall color in a room image
     * @param {string} inputImageUrl - URL of the room image
     * @param {string} wallColorHexCode - Desired wall color in hex format (e.g., '#FF5733')
     * @returns {Promise<Object>} API response with recolored image
     */
    async changeWallColor(inputImageUrl, wallColorHexCode) {
        return this.postJson('/change_wall_color', {
            input_image_url: inputImageUrl,
            wall_color_hex_code: wallColorHexCode
        });
    }

    /**
     * Change kitchen cabinet colors in an image
     * @param {string} inputImageUrl - URL of the kitchen image
     * @param {string} cabinetColorHexCode - Desired cabinet color in hex format
     * @returns {Promise<Object>} API response with recolored cabinet image
     */
    async changeKitchenCabinetsColor(inputImageUrl, cabinetColorHexCode) {
        return this.postJson('/change_kitchen_cabinets_color', {
            input_image_url: inputImageUrl,
            cabinet_color_hex_code: cabinetColorHexCode
        });
    }

    // =========================================================================
    // Remodeling
    // =========================================================================

    /**
     * Generate kitchen remodel designs
     * @param {string} inputImageUrl - URL of the current kitchen image
     * @param {string} designStyle - Design aesthetic for the remodel
     * @param {Object} [options]
     * @param {number} [options.numImages=1] - Number of designs to generate (1-4)
     * @param {number} [options.scaleFactor] - Resolution multiplier (1-4)
     * @returns {Promise<Object>} API response with remodeled kitchen images
     */
    async remodelKitchen(inputImageUrl, designStyle, options = {}) {
        const payload = {
            input_image_url: inputImageUrl,
            design_style: designStyle
        };
        if (options.numImages && options.numImages > 1) payload.num_images = options.numImages;
        if (options.scaleFactor) payload.scale_factor = options.scaleFactor;
        return this.postJson('/remodel_kitchen', payload);
    }

    /**
     * Generate bathroom remodel designs
     * @param {string} inputImageUrl - URL of the current bathroom image
     * @param {string} designStyle - Design aesthetic for the remodel
     * @param {Object} [options]
     * @param {number} [options.numImages=1] - Number of designs to generate (1-4)
     * @param {number} [options.scaleFactor] - Resolution multiplier (1-4)
     * @returns {Promise<Object>} API response with remodeled bathroom images
     */
    async remodelBathroom(inputImageUrl, designStyle, options = {}) {
        const payload = {
            input_image_url: inputImageUrl,
            design_style: designStyle
        };
        if (options.numImages && options.numImages > 1) payload.num_images = options.numImages;
        if (options.scaleFactor) payload.scale_factor = options.scaleFactor;
        return this.postJson('/remodel_bathroom', payload);
    }

    // =========================================================================
    // Exterior & Landscaping
    // =========================================================================

    /**
     * Replace the sky in an exterior property photo
     * @param {string} inputImageUrl - URL of the exterior image
     * @param {string} skyType - Type of sky ('day', 'dusk', or 'night')
     * @returns {Promise<Object>} API response with sky-replaced image
     */
    async replaceSkyBehindHouse(inputImageUrl, skyType) {
        return this.postJson('/replace_sky_behind_house', {
            input_image_url: inputImageUrl,
            sky_type: skyType
        });
    }

    /**
     * Generate landscaping designs for a yard (Beta)
     * @param {string} inputImageUrl - URL of the yard image
     * @param {string} yardType - Type of yard ('Front Yard', 'Backyard', or 'Side Yard')
     * @param {string} gardenStyle - Garden design style (e.g., 'japanese_zen')
     * @param {Object} [options]
     * @param {number} [options.numImages=1] - Number of designs to generate (1-4)
     * @returns {Promise<Object>} API response with landscaped yard images
     */
    async generateLandscapingDesigns(inputImageUrl, yardType, gardenStyle, options = {}) {
        const payload = {
            input_image_url: inputImageUrl,
            yard_type: yardType,
            garden_style: gardenStyle
        };
        if (options.numImages && options.numImages > 1) payload.num_images = options.numImages;
        return this.postJson('/generate_landscaping_designs', payload);
    }

    // =========================================================================
    // Image Processing
    // =========================================================================

    /**
     * Remove objects/furniture from a room image
     * @param {string} inputImageUrl - URL of the room image
     * @param {string} [maskImageUrl] - Optional black/white mask specifying areas to remove
     * @returns {Promise<Object>} API response with cleaned room image
     */
    async removeObjectsFromRoom(inputImageUrl, maskImageUrl = null) {
        const payload = { input_image_url: inputImageUrl };
        if (maskImageUrl) payload.mask_image_url = maskImageUrl;
        return this.postJson('/remove_objects_from_room', payload);
    }

    /**
     * Upscale an image to higher resolution
     * @param {string|Buffer} inputImage - File path, URL, or Buffer (max 4MB)
     * @param {number} [scaleFactor=2] - Resolution multiplier (1-8)
     * @returns {Promise<Object>} API response with base64-encoded upscaled image
     */
    async upscaleImage(inputImage, scaleFactor = 2) {
        const formData = await this.createFormData(inputImage);
        return this.postMultipart('/upscale_image', formData, { scale_factor: scaleFactor });
    }

    // =========================================================================
    // 3D & Rendering
    // =========================================================================

    /**
     * Convert a sketch or floor plan to a 3D rendered image
     * @param {string} inputImageUrl - URL of the sketch/floor plan image
     * @param {string} designStyle - Design aesthetic for the render
     * @param {Object} [options]
     * @param {number} [options.numImages=1] - Number of renders to generate (1-4)
     * @param {number} [options.scaleFactor] - Resolution multiplier (1-8)
     * @param {string} [options.renderType] - Render perspective ('perspective' or 'isometric')
     * @returns {Promise<Object>} API response with 3D rendered images
     */
    async sketchTo3dRender(inputImageUrl, designStyle, options = {}) {
        const payload = {
            input_image_url: inputImageUrl,
            design_style: designStyle
        };
        if (options.numImages && options.numImages > 1) payload.num_images = options.numImages;
        if (options.scaleFactor) payload.scale_factor = options.scaleFactor;
        if (options.renderType) payload.render_type = options.renderType;
        return this.postJson('/sketch_to_3d_render', payload);
    }

    // =========================================================================
    // Utility (deprecated/legacy)
    // =========================================================================

    /**
     * Generate image captions (verify API support)
     * @param {string} roomType - Type of room
     * @param {string} designStyle - Design style
     * @param {number} [numCaptions=1] - Number of captions
     * @returns {Promise<Object>} API response with captions
     */
    async generateImageCaptions(roomType, designStyle, numCaptions = 1) {
        return this.postJson('/generate_image_captions', {
            room_type: roomType,
            design_style: designStyle,
            num_captions: numCaptions
        });
    }
}

module.exports = Decor8AI;
