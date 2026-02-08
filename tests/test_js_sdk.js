#!/usr/bin/env node
/**
 * Comprehensive API Test Suite for Decor8 AI JavaScript SDK
 *
 * Run with: node test_js_sdk.js
 *
 * Requires:
 *   - DECOR8AI_API_KEY environment variable set
 *   - Node.js 14+
 */

const path = require('path');
const fs = require('fs');

// Import the SDK
const Decor8AI = require(path.join(__dirname, '../js/decor8ai'));

// Test configuration - using exact images from server tests
const CONFIG = {
    testImages: {
        room: 'https://prod-files.decor8.ai/test-images/sdk_test_image.png',
        removeObjects: 'https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_bedroom_1.jpg',
        wallColor: 'https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_bedroom_1.jpg',
        kitchenCabinets: 'https://prod-files.decor8.ai/test-images/sdk_test_change_kitchen_cabinets_color_1.jpg',
        kitchenRemodel: 'https://prod-files.decor8.ai/test-images/sdk_test_remodel_kitchen.png',
        bathroomRemodel: 'https://prod-files.decor8.ai/test-images/sdk_test_remodel_bathroom.png',
        landscaping: 'https://prod-files.decor8.ai/test-images/sdk_test_landcape_designs_front_yard.jpeg',
        skyReplacement: 'https://prod-files.decor8.ai/test-images/sdk_replace_sky_test_image.png',
        sketch: 'https://prod-files.decor8.ai/test-images/sdk_sketch_to_3d_render.png',
    },
    testParams: {
        roomType: 'livingroom',
        designStyle: 'modern',
        wallColor: '#FF5733',
        cabinetColor: '#8B4513',
        skyType: 'day',
        yardType: 'front yard',
        gardenStyle: 'california style garden',
    },
};

// Colors for terminal output
const Colors = {
    green: '\x1b[92m',
    red: '\x1b[91m',
    yellow: '\x1b[93m',
    blue: '\x1b[94m',
    bold: '\x1b[1m',
    end: '\x1b[0m',
};

function printHeader(text) {
    console.log(`\n${Colors.bold}${Colors.blue}${'='.repeat(60)}${Colors.end}`);
    console.log(`${Colors.bold}${Colors.blue}${text.padStart(30 + text.length / 2).padEnd(60)}${Colors.end}`);
    console.log(`${Colors.bold}${Colors.blue}${'='.repeat(60)}${Colors.end}\n`);
}

function printResult(name, success, duration, error = null) {
    const status = success
        ? `${Colors.green}PASS${Colors.end}`
        : `${Colors.red}FAIL${Colors.end}`;
    console.log(`  [${status}] ${name} (${duration.toFixed(2)}s)`);
    if (error) {
        console.log(`        ${Colors.red}Error: ${error}${Colors.end}`);
    }
}

async function testEndpoint(name, func) {
    const start = Date.now();
    try {
        const result = await func();
        const duration = (Date.now() - start) / 1000;

        // Check for API errors
        if (result && result.error) {
            return {
                name,
                success: false,
                duration,
                error: `${result.error}: ${result.message || ''}`,
            };
        }

        // Check for images in response
        if (result && result.info && result.info.images) {
            if (result.info.images.length === 0) {
                return {
                    name,
                    success: false,
                    duration,
                    error: 'No images returned',
                };
            }
        }

        return { name, success: true, duration, error: null };
    } catch (e) {
        const duration = (Date.now() - start) / 1000;
        return {
            name,
            success: false,
            duration,
            error: e.message || String(e),
        };
    }
}

async function runTests() {
    printHeader('JavaScript SDK Tests');

    const results = [];
    let client;

    try {
        client = new Decor8AI();
    } catch (e) {
        console.log(`${Colors.red}Failed to initialize SDK: ${e.message}${Colors.end}`);
        return [{ name: 'SDK Initialization', success: false, duration: 0, error: e.message }];
    }

    // Test 1: Generate Designs for Room
    let r = await testEndpoint('generateDesignsForRoom', () =>
        client.generateDesignsForRoom({
            inputImageUrl: CONFIG.testImages.room,
            roomType: CONFIG.testParams.roomType,
            designStyle: CONFIG.testParams.designStyle,
            numImages: 1,
        })
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 2: Generate Inspirational Designs
    r = await testEndpoint('generateInspirationalDesigns', () =>
        client.generateInspirationalDesigns({
            roomType: CONFIG.testParams.roomType,
            designStyle: CONFIG.testParams.designStyle,
            numImages: 1,
        })
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 3: Prime Walls for Room
    r = await testEndpoint('primeWallsForRoom', () =>
        client.primeWallsForRoom(CONFIG.testImages.room)
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 4: Replace Sky Behind House
    r = await testEndpoint('replaceSkyBehindHouse', () =>
        client.replaceSkyBehindHouse(CONFIG.testImages.skyReplacement, CONFIG.testParams.skyType)
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 5: Remove Objects from Room
    r = await testEndpoint('removeObjectsFromRoom', () =>
        client.removeObjectsFromRoom(CONFIG.testImages.removeObjects)
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 6: Change Wall Color
    r = await testEndpoint('changeWallColor', () =>
        client.changeWallColor(CONFIG.testImages.wallColor, CONFIG.testParams.wallColor)
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 7: Change Kitchen Cabinets Color
    r = await testEndpoint('changeKitchenCabinetsColor', () =>
        client.changeKitchenCabinetsColor(CONFIG.testImages.kitchenCabinets, CONFIG.testParams.cabinetColor)
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 8: Remodel Kitchen
    r = await testEndpoint('remodelKitchen', () =>
        client.remodelKitchen(CONFIG.testImages.kitchenRemodel, CONFIG.testParams.designStyle, { numImages: 1 })
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 9: Remodel Bathroom
    r = await testEndpoint('remodelBathroom', () =>
        client.remodelBathroom(CONFIG.testImages.bathroomRemodel, CONFIG.testParams.designStyle, { numImages: 1 })
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 10: Generate Landscaping Designs
    r = await testEndpoint('generateLandscapingDesigns', () =>
        client.generateLandscapingDesigns(
            CONFIG.testImages.landscaping,
            CONFIG.testParams.yardType,
            CONFIG.testParams.gardenStyle,
            { numImages: 1 }
        )
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    // Test 11: Sketch to 3D Render
    r = await testEndpoint('sketchTo3dRender', () =>
        client.sketchTo3dRender(CONFIG.testImages.sketch, CONFIG.testParams.designStyle, { numImages: 1 })
    );
    results.push(r);
    printResult(r.name, r.success, r.duration, r.error);

    return results;
}

function printSummary(results) {
    printHeader('Test Summary');

    const passed = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    const totalTime = results.reduce((sum, r) => sum + r.duration, 0);

    const statusColor = failed === 0 ? Colors.green : Colors.red;
    const statusText = failed === 0 ? 'ALL TESTS PASSED' : `${failed} TEST(S) FAILED`;

    console.log(`  Total Tests:    ${results.length}`);
    console.log(`  Passed:         ${Colors.green}${passed}${Colors.end}`);
    console.log(`  Failed:         ${Colors.red}${failed}${Colors.end}`);
    console.log(`  Success Rate:   ${((passed / results.length) * 100).toFixed(1)}%`);
    console.log(`  Total Duration: ${totalTime.toFixed(2)}s`);
    console.log();
    console.log(`  ${statusColor}${Colors.bold}${statusText}${Colors.end}`);
    console.log();

    // List failed tests
    const failedTests = results.filter(r => !r.success);
    if (failedTests.length > 0) {
        console.log(`  ${Colors.red}Failed Tests:${Colors.end}`);
        failedTests.forEach(test => {
            console.log(`    - ${test.name}: ${test.error}`);
        });
        console.log();
    }

    return failed === 0;
}

async function main() {
    console.log(`\n${Colors.bold}Decor8 AI JavaScript SDK - Test Suite${Colors.end}`);
    console.log(`Timestamp: ${new Date().toISOString()}`);

    // Check API key
    if (!process.env.DECOR8AI_API_KEY) {
        console.log(`\n${Colors.red}ERROR: DECOR8AI_API_KEY environment variable not set${Colors.end}`);
        console.log("Set it with: export DECOR8AI_API_KEY='your-api-key'");
        process.exit(1);
    }

    console.log(`API Key: ${'*'.repeat(20)}...${process.env.DECOR8AI_API_KEY.slice(-4)}`);

    const results = await runTests();

    // Save results
    const resultsDir = path.join(__dirname, 'results');
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, { recursive: true });
    }

    const report = {
        timestamp: new Date().toISOString(),
        sdk: 'javascript',
        results,
    };

    fs.writeFileSync(
        path.join(resultsDir, 'js_test_report.json'),
        JSON.stringify(report, null, 2)
    );

    const success = printSummary(results);
    process.exit(success ? 0 : 1);
}

main().catch(e => {
    console.error(`${Colors.red}Unexpected error: ${e.message}${Colors.end}`);
    process.exit(1);
});
