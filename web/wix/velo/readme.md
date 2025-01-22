# Virtual Staging & Real Estate Photography Enhancement Guide for Wix

## Why Virtual Staging Matters for Real Estate Photographers

As a real estate photographer, you're always looking for ways to add value to your services and stay competitive in the market. Virtual staging has emerged as a game-changing solution that perfectly complements traditional real estate photography. Here's why:

- **Expand Your Service Portfolio**: Offer both traditional photography and virtual staging as a premium package
- **Increase Revenue**: Add a high-margin service without significant overhead costs
- **Meet Modern Market Demands**: Help agents and sellers showcase properties' potential in the digital age
- **Quick Turnaround**: Deliver staged photos within hours instead of days required for traditional staging
- **Cost-Effective**: Provide an affordable alternative to physical staging, saving clients thousands of dollars
- **Competitive Edge**: Stand out from competitors by offering cutting-edge AI-powered services

## Getting Started: Choose Your Path

### Path 1: Quick Start with Pre-built Template
If you're starting from scratch or want the fastest implementation:

1. Download our ready-to-use template from [here](https://www.decor8.ai/_files/archives/59378b_bb0cd6e8fa4d457e915d98b183a028e9.zip?dn=VirtualStaging-v2-template.zip)
2. Extract the ZIP file and click on "Use this template.html"
3. Sign up or log in to your Wix account when prompted
4. Accept the terms and conditions and click "Add Site"
5. The template will be added to your account as a new site
6. Customize the site according to your needs
7. Add your Decor8 AI API key (see Step 1 in Implementation Steps below)

### Path 2: Add to Your Existing Wix Website
If you already have a photography business website on Wix:

## Prerequisites

1. A Wix website with a Business & eCommerce premium plan
2. Decor8 AI API Subscription and an API key from [Decor8 AI](https://app.decor8.ai)

## Implementation Steps

### Step 1: Setting Up Virtual Staging Backend

1. In your Wix dashboard, go to `Development Tools` → `Backend` → `velo-backend`
2. Create a new file named `decor8ai.web.js` in the backend
3. Copy the provided backend code into this file
4. Replace `DECOR8AI_API_KEY` with your actual API key from Decor8 AI:
   ```javascript
   const API_KEY = "your_api_key_here"
   ```

### Step 2: Creating Your Virtual Staging Service Page

1. In the Wix Editor, add a new page named "Virtual Home Staging"
2. Add the following UI elements to your page (names must match exactly):

#### Required UI Elements for Virtual Staging

| Element Type | Element ID | Description |
|-------------|------------|-------------|
| Upload Button | `#uploadButton` | For real estate photo upload |
| Button | `#uploadTriggerButton` | Triggers the upload process |
| Text | `#uploadStatusText` | Displays upload status |
| Image | `#input-image-preview` | Shows the uploaded property photo |
| Dropdown | `#roomTypeDropdown` | Room type selection |
| Dropdown | `#designStyleDropdown` | Home staging style selection |
| Button | `#generateDesignButton` | Starts the virtual staging process |
| Progress Bar | `#progressIndicator` | Shows generation progress |
| Text | `#errorMessage` | Displays error messages |
| Image | `#outputImage` | Displays the virtually staged room |
| Image | `#downloadIcon` | Download icon for the staged image |

### Step 3: Frontend Setup for Virtual Staging

1. In the Virtual Home Staging page settings, click on `Page Code`
2. Copy the provided `virtual-stager.app.js` code into this section
3. Save and publish your changes

### Step 4: Preview and Testing Your Virtual Staging Service

1. Click the "Preview" button in the top-right corner of the Wix Editor
   - Or click "Publish" and then "View Site" to test on the live site

2. On the Virtual Home Staging page, you should see:
   - An upload button for real estate photos
   - Dropdowns for room type and staging style
   - A generate button
   - Space for the staged property image

3. Test the full virtual staging workflow:
   - Upload a real estate photo (empty room works best)
   - Select a room type (e.g., "Living Room")
   - Choose a staging style (e.g., "Modern")
   - Click "Generate Design"
   - Wait for the virtual staging process to complete (30-90 seconds)
   - The staged room image should appear below

4. If you encounter issues:
   - Open the browser's Developer Console (F12 or right-click → Inspect)
   - Look for any error messages in the Console tab
   - Verify all UI elements are named exactly as specified
   - Check that your API key is correctly set in the backend

## Best Practices for Virtual Staging Success

### Photography Tips
- Use wide-angle lenses (24-35mm) for optimal room coverage
- Ensure proper lighting and exposure
- Shoot from corner angles to maximize room visibility
- Keep the camera level to avoid distortion
- Remove all existing furniture and clutter before shooting

### Business Integration Tips
- Create service packages combining photography and virtual staging
- Offer multiple design styles for each room
- Include before/after comparisons in your portfolio
- Consider bulk pricing for multiple rooms or properties
- Educate clients on the benefits and cost savings of virtual staging

## Technical Specifications

- Maximum image size: 10MB
- Supported formats: JPG, PNG
- Processing time: 30-90 seconds per image
- System timeout: 2 minutes
- High-resolution output suitable for marketing materials

## Support

For API-related issues, contact Decor8 AI support at decor8@immex.tech