=== Decor8 AI Virtual Staging ===
Contributors: decor8ai
Tags: virtual staging, real estate, interior design, ai staging, property photos
Requires at least: 5.8
Tested up to: 6.4
Requires PHP: 7.4
Stable tag: 1.0.2
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Transform empty rooms into beautifully staged spaces using AI-powered virtual staging technology.

== Description ==

Decor8 AI Virtual Staging brings professional-grade virtual staging capabilities to your WordPress website. Using advanced AI technology, transform empty or outdated room photos into beautifully staged spaces in seconds.

= Key Features =

* **One-Click Staging**: Upload a photo and get virtually staged results in seconds
* **Multiple Room Types**: Support for living rooms, bedrooms, kitchens, bathrooms, and more
* **Diverse Design Styles**: Choose from 30+ design styles including Modern, Minimalist, Industrial, and more
* **High-Resolution Output**: Get high-quality staged images suitable for marketing materials
* **User-Friendly Interface**: Simple drag-and-drop upload and intuitive controls
* **Before/After Comparison**: Easy visualization of the transformation
* **Instant Download**: Download staged images immediately after processing

= Supported Room Types =

* Living Room
* Kitchen
* Dining Room
* Bedroom
* Bathroom
* Home Office
* Kids Room
* Family Room
* Sunroom
* Walk-in Closet
* And many more...

= Available Design Styles =

* Minimalist
* Scandinavian
* Industrial
* Modern
* Contemporary
* Mid-Century Modern
* Traditional
* Farmhouse
* Coastal
* Bohemian
* And many more...

= Perfect For =

* Real Estate Agents
* Property Photographers
* Interior Designers
* Property Managers
* Home Stagers
* Property Developers

= Technical Requirements =

* Maximum image size: 10MB
* Supported formats: JPG, PNG
* Recommended resolution: 2000x2000 pixels or higher
* Active internet connection required
* Valid Decor8 AI API key required

== Installation ==

1. Upload the plugin files to `/wp-content/plugins/decor8ai-virtual-staging` directory, or install directly through WordPress plugin installer
2. Activate the plugin through the 'Plugins' menu in WordPress
3. Go to 'Virtual Staging' in your admin menu
4. Enter your Decor8 AI API key (get one from [app.decor8.ai](https://app.decor8.ai))
5. Add the shortcode `[decor8_virtual_staging]` to any page where you want the staging interface to appear

= Manual Installation =

1. Download the plugin ZIP file
2. Log in to your WordPress admin panel
3. Go to Plugins → Add New
4. Click the 'Upload Plugin' button
5. Upload the ZIP file
6. Click 'Install Now'
7. Activate the plugin

== Frequently Asked Questions ==

= How do I get an API key? =

Visit [app.decor8.ai](https://app.decor8.ai) to create an account and obtain your API key.

= What image formats are supported? =

Currently, the plugin supports JPG and PNG formats.

= Is there a file size limit? =

Yes, the maximum file size is 10MB per image.

= How long does it take to process an image? =

Typically 30-90 seconds, depending on image size and server load.

= Can I use the staged images commercially? =

Yes, you have full commercial rights to use the staged images for your real estate marketing purposes.

= Does it work with any WordPress theme? =

Yes, the plugin is designed to work with any properly coded WordPress theme.

= Can I customize the styling? =

Yes, you can override the default styles using your theme's CSS.

== Screenshots ==

1. Virtual staging interface
2. Room type and style selection
3. Processing progress
4. Before/After comparison
5. Admin settings page

== Changelog ==

= 1.0.1 =
* Fixed admin menu registration
* Improved error logging
* Removed unnecessary test files

= 1.0.0 =
* Initial release
* Basic virtual staging functionality
* Support for multiple room types
* Various design style options
* Before/After comparison view
* Download capability

== Upgrade Notice ==

= 1.0.0 =
Initial release of Decor8 AI Virtual Staging plugin.

== Privacy Policy ==

This plugin:
* Uploads images to Decor8 AI servers for processing
* Does not collect any personal information
* Does not use cookies
* Does not track users

Visit [decor8.ai/privacy](https://decor8.ai/privacy) for our full privacy policy.

== Support ==

For technical support:
* Email: decor8@immex.tech
* Documentation: [docs.decor8.ai](https://docs.decor8.ai)
* Support Hours: Monday-Friday, 9 AM - 5 PM EST

== Credits ==

Decor8 AI Virtual Staging is developed and maintained by Decor8 AI.

== Additional Information ==

= Best Practices =

1. Use high-quality original photos
2. Ensure rooms are empty or minimally furnished
3. Take photos in good lighting conditions
4. Keep images under 10MB for optimal processing
5. Use recommended image resolution (2000x2000 pixels or higher)

= Known Limitations =

* Maximum processing time: 2 minutes
* Single image processing at a time
* Internet connection required for processing
* API key required for functionality

= Integration Examples =

Add to a page using shortcode:
`[decor8_virtual_staging]`

Add to a template file:
`<?php echo do_shortcode('[decor8_virtual_staging]'); ?>`

= Customization =

Developers can customize the plugin using these filters:

* `decor8_vs_room_types` - Modify available room types
* `decor8_vs_design_styles` - Modify available design styles
* `decor8_vs_max_file_size` - Change maximum file size
* `decor8_vs_supported_formats` - Modify supported file formats

= Troubleshooting =

Common issues and solutions:
1. Image upload fails
   * Check file size and format
   * Verify PHP upload limits
2. Processing timeout
   * Check internet connection
   * Verify API key status
3. Styling conflicts
   * Check theme compatibility
   * Review CSS customization
