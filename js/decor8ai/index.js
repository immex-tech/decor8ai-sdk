const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

class Decor8AI {
    constructor( baseUrl = 'https://api.decor8.ai') {
        this.apiKey = process.env.DECOR8AI_API_KEY;
        if (!this.apiKey) {
            throw new Error("DECOR8AI_API_KEY environment variable is not set.");
        }
        this.baseUrl = baseUrl;
    }

    async primeTheRoomWalls(inputImage) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'multipart/form-data'
            };

            const formData = await this.createFormData(inputImage);

            const response = await axios.post(`${this.baseUrl}/prime_the_room_walls`, formData, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async primeWallsForRoom(inputImageUrl) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            };

            const payload = {input_image_url: inputImageUrl}

            const response = await axios.post(`${this.baseUrl}/prime_walls_for_room`, payload, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }    

    async generateDesigns(inputImage, roomType, designStyle, numCaptions = null, numImages = 1, keep_original_dimensions = false, color_scheme = null, speciality_decor = null) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'multipart/form-data'
            };

            const formData = await this.createFormData(inputImage);
            formData.append('room_type', roomType);
            formData.append('design_style', designStyle);
            formData.append('num_images', numImages);
            if (numCaptions) {
                formData.append('num_captions', numCaptions);
            }
            if (color_scheme) {
                formData.append('color_scheme', color_scheme);
            }
            if (speciality_decor) {
                formData.append('speciality_decor', speciality_decor);
            }
            formData.append('keep_original_dimensions', String(keep_original_dimensions));

            const response = await axios.post(`${this.baseUrl}/generate_designs`, formData, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    /**
     * Generate designs for a room using an input image URL
     * @param {string} inputImageUrl - URL of the input image
     * @param {string} [roomType] - Type of room (e.g., 'bedroom', 'livingroom')
     * @param {string} [designStyle] - Design style (e.g., 'modern', 'frenchcountry')
     * @param {Object} [maskInfo=null] - Masking information for the image
     * @param {number} [numCaptions=null] - Number of captions to generate
     * @param {number} [numImages=1] - Number of images to generate
     * @param {boolean} [keep_original_dimensions=false] - Whether to keep original image dimensions
     * @param {string} [color_scheme=null] - Predefined color scheme (e.g., 'COLOR_SCHEME_0')
     * @param {string} [speciality_decor=null] - Predefined specialty decor
     * @param {number} [scale_factor=null] - Scale factor for the output image
     * @param {string} [prompt=null] - Custom prompt describing desired outcome
     * @param {string} [prompt_prefix=null] - Text to prepend to the prompt
     * @param {string} [prompt_suffix=null] - Text to append to the prompt
     * @param {string} [negative_prompt=null] - Things to avoid in generation
     * @param {number} [seed=null] - Random seed for reproducible results
     * @param {number} [guidance_scale=null] - Controls how closely to follow the prompt (default: 7.5)
     * @param {number} [num_inference_steps=null] - Number of denoising steps (default: 30)
     * @returns {Promise<Object>} API response
     */
    async generateDesignsForRoom(inputImageUrl, roomType = null, designStyle = null, maskInfo = null, numCaptions = null, numImages = 1, keep_original_dimensions = false, color_scheme = null, speciality_decor = null, scale_factor = null, prompt = null, prompt_prefix = null, prompt_suffix = null, negative_prompt = null, seed = null, guidance_scale = null, num_inference_steps = null) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
            };

            // Constructing the JSON payload with only required fields
            const payload = {
                input_image_url: inputImageUrl,
                num_images: numImages,
            };

            // Add optional parameters if they are provided
            if (roomType) payload.room_type = roomType;
            if (designStyle) payload.design_style = designStyle;
            if (scale_factor) payload.scale_factor = scale_factor;
            if (color_scheme) payload.color_scheme = color_scheme;
            if (speciality_decor) payload.speciality_decor = speciality_decor;
            if (prompt) payload.prompt = prompt;
            if (prompt_prefix) payload.prompt_prefix = prompt_prefix;
            if (prompt_suffix) payload.prompt_suffix = prompt_suffix;
            if (negative_prompt) payload.negative_prompt = negative_prompt;
            if (seed) payload.seed = seed;
            if (guidance_scale) payload.guidance_scale = guidance_scale;
            if (num_inference_steps) payload.num_inference_steps = num_inference_steps;

            const response = await axios.post(`${this.baseUrl}/generate_designs_for_room`, payload, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }    

    async upscaleImage(inputImage, scaleFactor = 2) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'multipart/form-data'
            };

            const formData = await this.createFormData(inputImage);
            formData.append('scale_factor', scaleFactor);

            const response = await axios.post(`${this.baseUrl}/upscale_image`, formData, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async createFormData(inputImage) {
        let formData = new FormData();
        if (typeof inputImage === 'string') { // Path or URL
            if (inputImage.startsWith('http')) { // URL
                try {
                    const response = await axios.get(inputImage, { responseType: 'arraybuffer' });
                    const buffer = Buffer.from(response.data, 'binary');
                    formData.append('input_image', buffer, 'input_image.jpg');
                } catch (error) {
                    console.error(error);
                    throw new Error("Failed to load image from URL");
                }
            } else { // File Path
                formData.append('input_image', fs.createReadStream(inputImage), 'input_image.jpg');
            }
        } else if (Buffer.isBuffer(inputImage)) { // Binary Data
            formData.append('input_image', inputImage, 'input_image.jpg');
        }
    
        return formData;
    }
    

    async generateImageCaptions(room_type, design_style, num_captions = 1) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            };

            const input = {
                'room_type': room_type,
                'design_style': design_style,
                'num_captions': num_captions}

            const response = await axios.post(`${this.baseUrl}/generate_image_captions`, input, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    /**
     * Generate inspirational designs without an input image
     * @param {string} [roomType] - Type of room (e.g., 'bedroom', 'livingroom')
     * @param {string} [designStyle] - Design style (e.g., 'modern', 'frenchcountry')
     * @param {number} [numImages=1] - Number of images to generate
     * @param {string} [prompt=null] - Custom prompt describing desired outcome
     * @param {string} [prompt_prefix=null] - Text to prepend to the prompt
     * @param {string} [prompt_suffix=null] - Text to append to the prompt
     * @param {string} [negative_prompt=null] - Things to avoid in generation
     * @param {number} [seed=null] - Random seed for reproducible results
     * @param {number} [guidance_scale=null] - Controls how closely to follow the prompt (default: 7.5)
     * @param {number} [num_inference_steps=null] - Number of denoising steps (default: 30)
     * @returns {Promise<Object>} API response
     */
    async generateInspirationalDesigns(roomType = null, designStyle = null, numImages = 1, prompt = null, prompt_prefix = null, prompt_suffix = null, negative_prompt = null, seed = null, guidance_scale = null, num_inference_steps = null) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            };

            // Constructing the JSON payload with only required fields
            const payload = {
                num_images: numImages,
            };

            // Add optional parameters if they are provided
            if (roomType) payload.room_type = roomType;
            if (designStyle) payload.design_style = designStyle;
            if (prompt) payload.prompt = prompt;
            if (prompt_prefix) payload.prompt_prefix = prompt_prefix;
            if (prompt_suffix) payload.prompt_suffix = prompt_suffix;
            if (negative_prompt) payload.negative_prompt = negative_prompt;
            if (seed) payload.seed = seed;
            if (guidance_scale) payload.guidance_scale = guidance_scale;
            if (num_inference_steps) payload.num_inference_steps = num_inference_steps;

            const response = await axios.post(`${this.baseUrl}/generate_inspirational_designs`, payload, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

module.exports = Decor8AI;
