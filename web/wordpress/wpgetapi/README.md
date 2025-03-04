# Decor8 API Integration with WordPress using WPGetAPI

## Introduction
This guide provides a **comprehensive and detailed** step-by-step approach to integrating **Decor8 AI APIs** with your WordPress site using the **WPGetAPI plugin**. It serves as the **definitive source** for setting up and managing Decor8 API requests and displaying AI-generated designs dynamically.


## What is Decor8 AI?
Decor8 AI is a cutting-edge interior design app that revolutionizes your design experience. It offers a rich tapestry of customization options allowing you to visualize and craft interiors that echo your style and imagination.

You can choose from 35+ interior design styles and 20+ room types to create unique interior design styles for your space. The platform specializes in virtual staging, transforming empty spaces into vivid, attractive interiors, enhancing their appeal for better marketability.

This documentation describes how you can integrate Decor8 AI in your Wordpress site.

---

## Prerequisites

1. **WordPress Installed** (Version 5.0+ recommended)
2. **WPGetAPI Plugin Installed** ([Download Here](https://wordpress.org/plugins/wpgetapi/))
3. **Decor8AI API Subscription** (Obtain from [Decor8 AI Dashboard](https://app.decor8.ai/))
4. **Decor8 API Key** (Obtain from [Decor8 AI API Documentation](https://api-docs.decor8.ai/))

---

## Step 1: Install & Configure WPGetAPI Plugin

### Install WPGetAPI

1. Go to **WordPress Dashboard** → **Plugins** → **Add New**.
2. Search for `WPGetAPI`.
3. Click **Install Now** → **Activate**.

### Add Decor8 API Configuration

1. Navigate to **WPGetAPI** → **Settings**.
2. Click **"Add New API"** and enter the following:
   - **API Name**: `decor8ai`
   - **Base URL**: `https://api.decor8.ai`
   - **Authentication Type**: `Bearer Token`
   - **Bearer Token**: `YOUR_DECOR8AI_API_KEY`
   - **Headers**:
     ```yaml
     Authorization: Bearer YOUR_DECOR8AI_API_KEY
     Content-Type: application/json
     ```

3. **Save the API Configuration** by clicking **"Save Settings"**.

---

## Step 2: Add API Endpoint for Room Design Generation

1. Go to **WPGetAPI** → Your API (`decor8ai`).
2. Click **"Add Endpoint"** and configure as follows:
   - **Endpoint Name**: `generate_designs_for_room`
   - **Method**: `POST`
   - **Endpoint URL**: `/generate_designs_for_room`
   - **Request Format**: `JSON`
   - **Body Parameters**:
     ```json
     {
       "input_image_url": "https://prod-files.decor8.ai/test-images/sdk_test_image.png",
       "room_type": "livingroom",
       "design_style": "minimalist",
       "num_images": 1
     }
     ```

3. Click **Save Endpoint**.

---

## Step 3: Make an API Request in WordPress

### **Method 1: Using PHP Code** (Best for Themes/Plugins)

```php
<?php
// Define API request parameters
$params = [
    'input_image_url' => 'https://prod-files.decor8.ai/test-images/sdk_test_image.png',
    'room_type'       => 'livingroom',
    'design_style'    => 'minimalist',
    'num_images'      => 1
];

// Call API
$response = wpgetapi_endpoint('decor8ai', 'generate_designs_for_room', $params, 'json');

// Check for response
if (!empty($response['info']['images'][0]['url'])) {
    $image_url = esc_url($response['info']['images'][0]['url']);
    echo '<h2>Generated Design:</h2>';
    echo '<img src="' . $image_url . '" alt="Generated Room Design" style="max-width:100%; height:auto;">';
} else {
    echo '<p>Failed to generate design. Error: ' . esc_html($response['error'] ?? 'Unknown error') . '</p>';
}
?>
```

### **Method 2: Using Shortcodes (For Pages & Posts)**

Add this to `functions.php`:

```php
function decor8_generate_design_shortcode() {
    $params = [
        'input_image_url' => 'https://prod-files.decor8.ai/test-images/sdk_test_image.png',
        'room_type'       => 'livingroom',
        'design_style'    => 'minimalist',
        'num_images'      => 1
    ];

    $response = wpgetapi_endpoint('decor8ai', 'generate_designs_for_room', $params, 'json');
    
    if (!empty($response['info']['images'][0]['url'])) {
        return '<img src="' . esc_url($response['info']['images'][0]['url']) . '" style="max-width:100%; height:auto;">';
    } else {
        return '<p>Failed to generate design.</p>';
    }
}
add_shortcode('decor8_design', 'decor8_generate_design_shortcode');
```

Now, you can add `[decor8_design]` to **any page or post** to display a generated image.

---

## Troubleshooting

### 1. **Error: "Failed to generate design."**
- Ensure **API Key is correct** in WPGetAPI settings.
- Verify that **Decor8 API is reachable** by testing with a cURL request:
  ```sh
  curl -X POST "https://api.decor8.ai/generate_designs_for_room" \
       -H "Authorization: Bearer YOUR_DECOR8AI_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{"input_image_url": "https://prod-files.decor8.ai/test-images/sdk_test_image.png", "room_type": "livingroom", "design_style": "minimalist", "num_images": 1}'
  ```

### 2. **Images Not Displaying**
- Ensure `wpgetapi_endpoint` is correctly retrieving the `image_url`.
- Check **your browser console** (`F12 → Console`) for any blocked requests.
- Make sure the response contains `info.images[0].url`.

### 3. **Shortcode Not Working**
- Ensure the function is in `functions.php` and `add_shortcode` is correctly registered.

---

## Conclusion
By following this guide, you can **fully integrate Decor8 AI API into WordPress** using WPGetAPI. This allows you to dynamically generate and display AI-enhanced interior designs with minimal coding effort.

For additional support, refer to the **[Decor8 API Docs](https://api-docs.decor8.ai/)** or **[WPGetAPI Documentation](https://wpgetapi.com/docs/quick-start-guide/)** or reach out to us at decor8@imex.tech.

🚀 **Happy Designing with Decor8 AI & WordPress!**

