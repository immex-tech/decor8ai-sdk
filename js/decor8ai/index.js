const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

class Decor8AI {
    constructor( baseUrl = 'https://prod-app.decor8.ai:8000') {
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

            const formData = this.createFormData(inputImage);

            const response = await axios.post(`${this.baseUrl}/prime_the_room_walls`, formData, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async generateDesigns(inputImage, roomType, designStyle, numCaptions = null, numImages = 1, keep_original_dimensions = false) {
        try {
            const headers = {
                Authorization: `Bearer ${this.apiKey}`,
                'Content-Type': 'multipart/form-data'
            };

            const formData = this.createFormData(inputImage);
            formData.append('room_type', roomType);
            formData.append('design_style', designStyle);
            formData.append('num_images', numImages);
            if (numCaptions) {
                formData.append('num_captions', numCaptions);
            }
            formData.append('keep_original_dimensions', String(keep_original_dimensions));

            const response = await axios.post(`${this.baseUrl}/generate_designs`, formData, { headers });
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

            const formData = this.createFormData(inputImage);
            formData.append('scale_factor', scaleFactor);

            const response = await axios.post(`${this.baseUrl}/upscale_image`, formData, { headers });
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    createFormData(inputImage) {
        let formData = new FormData();

        if (typeof inputImage === 'string') { // Path or URL
            if (inputImage.startsWith('http')) { // URL
                axios.get(inputImage, { responseType: 'stream' })
                    .then(response => {
                        formData.append('input_image', response.data, { filename: 'input_image.jpg' });
                    })
                    .catch(error => console.error(error));
            } else { // File Path
                formData.append('input_image', fs.createReadStream(inputImage), 'input_image.jpg');
            }
        } else if (Buffer.isBuffer(inputImage)) { // Binary Data
            formData.append('input_image', inputImage, { filename: 'input_image.jpg' });
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
}

module.exports = Decor8AI;
