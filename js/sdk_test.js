const Decor8AI = require('./decor8ai/index');
const fs = require('fs');
const path = require('path');
const https = require('https');

// Make sure DECOR8AI_API_KEY is set in your environment variables before running this script
const decor8 = new Decor8AI();

const testImageUrl = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png';

// Test 1: Original parameter usage
console.log("Test 1: Testing generateDesignsForRoom with basic parameters");
decor8.generateDesignsForRoom(
    testImageUrl,
    'bedroom',
    'frenchcountry',
    null,
    null,
    1,
    false,
    'COLOR_SCHEME_0',
    'SPECIALITY_DECOR_0'
)
.then(response => {
    if (response.error) {
        console.error("Test 1 failed:", response.error);
    } else {
        console.log("Test 1 passed. Message:", response.message);
        handleDesignResponse(response);
    }
})
.catch(error => {
    console.error("Test 1 failed with error:", error);
});

// Test 2: New parameters usage
console.log("Test 2: Testing generateDesignsForRoom with advanced parameters");
decor8.generateDesignsForRoom(
    testImageUrl,
    'bedroom',
    'modern',
    null,
    null,
    2,
    false,
    null,
    null,
    null,
    'Modern minimalist room with sleek wardrobe, contemporary Table Lamps, and floating Dresser',
    'high end, professional photo',
    'clean lines, ambient lighting',
    'cluttered, traditional, ornate',
    42,
    15.0,
    50
)
.then(response => {
    if (response.error) {
        console.error("Test 2 failed:", response.error);
    } else {
        console.log("Test 2 passed. Message:", response.message);
        handleDesignResponse(response);
    }
})
.catch(error => {
    console.error("Test 2 failed with error:", error);
});

// Test 3: Custom prompt with some standard parameters
console.log("Test 3: Testing generateDesignsForRoom with custom prompt");
decor8.generateDesignsForRoom(
    testImageUrl,
    null,
    null,
    null,
    null,
    1,
    false,
    null,
    null,
    null,
    'A cozy reading nook with built-in bookshelves',
    null,
    null,
    null,
    null,
    15.0
)
.then(response => {
    if (response.error) {
        console.error("Test 3 failed:", response.error);
    } else {
        console.log("Test 3 passed. Message:", response.message);
        handleDesignResponse(response);
    }
})
.catch(error => {
    console.error("Test 3 failed with error:", error);
});

// Helper function to handle design responses
function handleDesignResponse(response) {
    const designs = response.info.images;
    designs.forEach((design, index) => {
        console.log(`Design ${index + 1}:`);
        console.log(`UUID: ${design.uuid}`);
        console.log(`Width: ${design.width}`);
        console.log(`Height: ${design.height}`);

        const outputDir = path.join(__dirname, 'output-data');
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        const filename = `design_${design.uuid}.jpg`;
        downloadAndSaveImage(design.url, outputDir, filename).catch(err => {
            console.error(err);
        });
    });
}

// Function to download an image from a URL and save it locally
function downloadAndSaveImage(url, outputDir, filename) {
    console.log(`Downloading image from ${url}`);
    const filePath = path.join(outputDir, filename);
  
    return new Promise((resolve, reject) => {
      const request = https.get(url, (response) => {
        if (response.statusCode === 200) {
          const fileStream = fs.createWriteStream(filePath);
          response.pipe(fileStream);
  
          fileStream.on('finish', () => {
            fileStream.close();
            console.log(`Image saved as ${filename}`);
            resolve();
          });
  
          fileStream.on('error', (err) => {
            console.error("An error occurred while saving the image:", err);
            fileStream.close();
            reject(err);
          });
        } else {
          reject(new Error(`Failed to get the image, status code: ${response.statusCode}`));
        }
      });
  
      request.on('error', (err) => {
        console.error("An error occurred while downloading the image:", err);
        reject(err);
      });
    });
  }

// Example using primeTheRoomWalls with a file path
// Priming operation applies white paint to the room walls. This is useful if the input image has dark walls or unfinished walls.
const input_image_path_for_priming = 'https://prod-files.decor8.ai/test-images/sdk_test_image.png';
console.log ("Priming the room walls for image at path " + input_image_path_for_priming);
decor8.primeWallsForRoom(input_image_path_for_priming)
    .then(response => {
        if (response.error) {
            console.error("An error occurred:", response.error);
        } else {
            console.log("Message:", response.message);
            const designs = response.info.images;
            designs.forEach((design, index) => {
                console.log(`Design ${index + 1}:`);
                console.log(`UUID: ${design.uuid}`);
                console.log(`Width: ${design.width}`);
                console.log(`Height: ${design.height}`);

                // If you want to save the image data as a file
                // Check if output-data directory exists, if not, create it
                const outputDir = path.join(__dirname, 'output-data');
                if (!fs.existsSync(outputDir)){
                    fs.mkdirSync(outputDir);
                }

                
                
                // Save the image data as a file in the output-data directory
                const filename = `design_${design.uuid}.jpg`;
                downloadAndSaveImage(design.url, outputDir, filename).catch(err => {
                console.error(err);
                });
            });

        }
    })
    .catch(error => {
        console.error("An error occurred while generating designs:", error);
    });


// Example using upscaleImage with a file path
const input_image_path_for_upscaling = './sdk_upscale_this_image.jpg';
const scale_factor = 2;
console.log ("Upscaling the image at path " + input_image_path_for_upscaling + " by a factor of " + scale_factor);
decor8.upscaleImage(input_image_path_for_upscaling, scale_factor)
    .then(response => {
        if (response.error) {
            console.error("An error occurred:", response.error);
        } else {
            console.log("Message:", response.message);
            const upscaled_image_data = response.info.upscaled_image;

            // If you want to save the image data as a file
            // Check if output-data directory exists, if not, create it
            const outputDir = path.join(__dirname, 'output-data');
            if (!fs.existsSync(outputDir)){
                fs.mkdirSync(outputDir);
            }
            
            // Save the image data as a file in the output-data directory
            fs.writeFileSync(path.join(outputDir, `upscaled_image.jpg`), upscaled_image_data, 'base64', (err) => {
                if (err) {
                    console.error("An error occurred while saving the image:", err);
                } else {
                    console.log(`Image saved as upscaled_image.jpg`);
                }
            });


        }
    })
    .catch(error => {
        console.error("An error occurred while generating designs:", error);
    });


// Example using generateImageCaptions
// console.log ("Generating captions for room type " + room_type + " and design style " + design_style);
decor8.generateImageCaptions('livingroom', 'modern', 2)
    .then(response => {
        if (response.error) {
            console.error("An error occurred:", response.error);
        } else {
            console.log("Message:", response.message);
            const captions = response.info.captions;
            captions.forEach((caption, index) => {
                console.log(`[${index + 1}] : ${caption}`);
            });
        }
    })
    .catch(error => {
        console.error("An error occurred while generating captions:", error);
    });

