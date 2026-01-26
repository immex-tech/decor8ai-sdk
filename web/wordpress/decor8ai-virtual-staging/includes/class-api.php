<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_API {
    private $api_key;
    private $api_url = 'https://api.decor8.ai/generate_designs_for_room';

    public function __construct() {
        $this->api_key = get_option('decor8_vs_api_key');

        decor8_log("=== DECOR8 API: Registering AJAX handlers ===", 'info', __FILE__, __LINE__);

        // Register AJAX handlers
        add_action('wp_ajax_decor8_process_image', array($this, 'handle_image_processing'));
        add_action('wp_ajax_nopriv_decor8_process_image', array($this, 'handle_image_processing'));
    }

    /**
     * Handle image processing AJAX request
     */
    public function handle_image_processing() {
        decor8_log("=== API: Image processing started ===", 'debug', __FILE__, __LINE__);
        try {
            // Verify nonce
            if (!check_ajax_referer('decor8_vs_nonce', 'nonce', false)) {
                throw new Exception(__('Security check failed', 'decor8ai-virtual-staging'));
            }

            // Check if API key is configured
            if (empty($this->api_key)) {
                throw new Exception(__('API key not configured', 'decor8ai-virtual-staging'));
            }

            // Validate file upload
            if (!isset($_FILES['image'])) {
                throw new Exception(__('No image provided', 'decor8ai-virtual-staging'));
            }

            // Validate room type and design style
            $room_type = $this->validate_room_type($_POST['room_type']);
            $design_style = $this->validate_design_style($_POST['design_style']);

            // Handle file upload
            $upload = $this->handle_file_upload($_FILES['image']);

            // Process image with Decor8 AI API
            $result = $this->process_with_api($upload['url'], $room_type, $design_style);

            wp_send_json_success($result);

        } catch (Exception $e) {
            wp_send_json_error(array(
                'message' => $e->getMessage()
            ));
        }
    }

    /**
     * Validate and handle file upload
     */
    private function handle_file_upload($file) {
        // Verify file size
        if ($file['size'] > 10 * MB_IN_BYTES) {
            throw new Exception(__('Image size must be less than 10MB', 'decor8ai-virtual-staging'));
        }

        // Verify file type
        $allowed_types = array('image/jpeg', 'image/png');
        $file_type = wp_check_filetype($file['name']);

        if (!in_array($file_type['type'], $allowed_types)) {
            throw new Exception(__('Only JPG and PNG images are allowed', 'decor8ai-virtual-staging'));
        }

        // Upload file to WordPress media library
        $upload = wp_handle_upload($file, array('test_form' => false));

        if (isset($upload['error'])) {
            throw new Exception($upload['error']);
        }

        return $upload;
    }

    /**
     * Process image with Decor8 AI API
     */
    private function process_with_api($image_url, $room_type, $design_style) {
        error_log("Decor8 API Request - Image URL: " . $image_url);
        error_log("Decor8 API Request - Room Type: " . $room_type);
        error_log("Decor8 API Request - Design Style: " . $design_style);
        $body = array(
            'input_image_url' => $image_url,
            'room_type' => $room_type,
            'design_style' => $design_style,
            'num_images' => 1,
            'scale_factor' => 1
        );

        $response = wp_remote_post($this->api_url, array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->api_key,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($body),
            'timeout' => 120, // Extended timeout for image processing
            'data_format' => 'body'
        ));

        if (is_wp_error($response)) {
            $error_message = $response->get_error_message();
            decor8_log("API Error: " . $error_message, 'error');
            error_log("Decor8 API Error Details: " . print_r($response->get_error_data(), true));
            throw new Exception($error_message);
        }

        $http_code = wp_remote_retrieve_response_code($response);
        $response_body = wp_remote_retrieve_body($response);

        error_log("Decor8 API Response Code: " . $http_code);
        error_log("Decor8 API Response Body: " . $response_body);

        if ($http_code !== 200) {
            $error_message = sprintf(
                /* translators: %d: HTTP response code */
                __('API request failed with code: %d', 'decor8ai-virtual-staging'),
                $http_code
            );
            decor8_log("API Error: " . $error_message, 'error');
            throw new Exception($error_message);
        }

        $body = json_decode(wp_remote_retrieve_body($response), true);

        decor8_log("API Response Body: " . print_r($body, true), 'debug', __FILE__, __LINE__);

        // Check for API error even with 200 status
        if (!empty($body['error'])) {
            decor8_log("API Error (200 status): " . $body['error'], 'error', __FILE__, __LINE__);
            throw new Exception($body['error']);
        }

        if (!isset($body['info']['images'][0]['url'])) {
            decor8_log("API Error: Missing image URL in response", 'error', __FILE__, __LINE__);
            throw new Exception(__('Invalid API response - Missing image URL', 'decor8ai-virtual-staging'));
        }

        return array(
            'staged_image_url' => $body['info']['images'][0]['url'],
            'message' => !empty($body['message']) ? $body['message'] : __('Virtual staging completed successfully', 'decor8ai-virtual-staging')
        );
    }

    /**
     * Validate room type
     * API expects lowercase values
     */
    private function validate_room_type($room_type) {
        // Convert to lowercase for API compatibility
        $room_type_lower = strtolower($room_type);

        $valid_room_types = array(
            'livingroom', 'bedroom', 'kitchen', 'bathroom', 'diningroom',
            'office', 'kidsroom', 'familyroom', 'readingnook', 'sunroom',
            'walkincloset', 'mudroom', 'toyroom', 'foyer', 'powderroom',
            'laundryroom', 'gym', 'basement', 'garage', 'balcony',
            'cafe', 'homebar', 'study_room', 'front_porch', 'back_porch',
            'back_patio', 'openplan', 'boardroom', 'meetingroom',
            'openworkspace', 'privateoffice'
        );

        if (!in_array($room_type_lower, $valid_room_types)) {
            throw new Exception(__('Invalid room type', 'decor8ai-virtual-staging'));
        }

        return $room_type_lower;
    }

    /**
     * Validate design style
     * API expects lowercase values
     */
    private function validate_design_style($design_style) {
        // Convert to lowercase for API compatibility
        $design_style_lower = strtolower($design_style);

        $valid_styles = array(
            'minimalist', 'scandinavian', 'industrial', 'boho', 'traditional',
            'artdeco', 'midcenturymodern', 'coastal', 'tropical', 'eclectic',
            'contemporary', 'frenchcountry', 'rustic', 'shabbychic', 'vintage',
            'country', 'modern', 'asian_zen', 'hollywoodregency', 'bauhaus',
            'mediterranean', 'farmhouse', 'victorian', 'gothic', 'moroccan',
            'southwestern', 'transitional', 'maximalist', 'arabic', 'japandi',
            'retrofuturism', 'artnouveau', 'urbanmodern', 'wabi_sabi',
            'grandmillennial', 'coastalgrandmother', 'newtraditional', 'cottagecore',
            'luxemodern', 'high_tech', 'organicmodern', 'tuscan', 'cabin',
            'desertmodern', 'global', 'industrialchic', 'modernfarmhouse',
            'europeanclassic', 'neotraditional', 'warmminimalist'
        );

        if (!in_array($design_style_lower, $valid_styles)) {
            throw new Exception(__('Invalid design style', 'decor8ai-virtual-staging'));
        }

        return $design_style_lower;
    }

    /**
     * Get valid room types for frontend
     */
    public static function get_room_types() {
        return array(
            'livingroom' => __('Living Room', 'decor8ai-virtual-staging'),
            'bedroom' => __('Bedroom', 'decor8ai-virtual-staging'),
            'kitchen' => __('Kitchen', 'decor8ai-virtual-staging'),
            'bathroom' => __('Bathroom', 'decor8ai-virtual-staging'),
            'diningroom' => __('Dining Room', 'decor8ai-virtual-staging'),
            'office' => __('Office', 'decor8ai-virtual-staging'),
            'kidsroom' => __('Kids Room', 'decor8ai-virtual-staging'),
            'familyroom' => __('Family Room', 'decor8ai-virtual-staging'),
            'readingnook' => __('Reading Nook', 'decor8ai-virtual-staging'),
            'sunroom' => __('Sunroom', 'decor8ai-virtual-staging'),
            'walkincloset' => __('Walk-in Closet', 'decor8ai-virtual-staging'),
            'mudroom' => __('Mudroom', 'decor8ai-virtual-staging'),
            'toyroom' => __('Toy Room', 'decor8ai-virtual-staging'),
            'foyer' => __('Foyer', 'decor8ai-virtual-staging'),
            'powderroom' => __('Powder Room', 'decor8ai-virtual-staging'),
            'laundryroom' => __('Laundry Room', 'decor8ai-virtual-staging'),
            'gym' => __('Gym', 'decor8ai-virtual-staging'),
            'basement' => __('Basement', 'decor8ai-virtual-staging'),
            'garage' => __('Garage', 'decor8ai-virtual-staging'),
            'balcony' => __('Balcony', 'decor8ai-virtual-staging'),
            'cafe' => __('Cafe', 'decor8ai-virtual-staging'),
            'homebar' => __('Home Bar', 'decor8ai-virtual-staging'),
            'study_room' => __('Study Room', 'decor8ai-virtual-staging'),
            'front_porch' => __('Front Porch', 'decor8ai-virtual-staging'),
            'back_porch' => __('Back Porch', 'decor8ai-virtual-staging'),
            'back_patio' => __('Back Patio', 'decor8ai-virtual-staging'),
            'openplan' => __('Open Plan', 'decor8ai-virtual-staging'),
            'boardroom' => __('Boardroom', 'decor8ai-virtual-staging'),
            'meetingroom' => __('Meeting Room', 'decor8ai-virtual-staging'),
            'openworkspace' => __('Open Workspace', 'decor8ai-virtual-staging'),
            'privateoffice' => __('Private Office', 'decor8ai-virtual-staging'),
        );
    }

    /**
     * Get valid design styles for frontend
     */
    public static function get_design_styles() {
        return array(
            'minimalist' => __('Minimalist', 'decor8ai-virtual-staging'),
            'scandinavian' => __('Scandinavian', 'decor8ai-virtual-staging'),
            'industrial' => __('Industrial', 'decor8ai-virtual-staging'),
            'boho' => __('Boho', 'decor8ai-virtual-staging'),
            'traditional' => __('Traditional', 'decor8ai-virtual-staging'),
            'artdeco' => __('Art Deco', 'decor8ai-virtual-staging'),
            'midcenturymodern' => __('Mid-Century Modern', 'decor8ai-virtual-staging'),
            'coastal' => __('Coastal', 'decor8ai-virtual-staging'),
            'tropical' => __('Tropical', 'decor8ai-virtual-staging'),
            'eclectic' => __('Eclectic', 'decor8ai-virtual-staging'),
            'contemporary' => __('Contemporary', 'decor8ai-virtual-staging'),
            'frenchcountry' => __('French Country', 'decor8ai-virtual-staging'),
            'rustic' => __('Rustic', 'decor8ai-virtual-staging'),
            'shabbychic' => __('Shabby Chic', 'decor8ai-virtual-staging'),
            'vintage' => __('Vintage', 'decor8ai-virtual-staging'),
            'country' => __('Country', 'decor8ai-virtual-staging'),
            'modern' => __('Modern', 'decor8ai-virtual-staging'),
            'asian_zen' => __('Asian Zen', 'decor8ai-virtual-staging'),
            'hollywoodregency' => __('Hollywood Regency', 'decor8ai-virtual-staging'),
            'bauhaus' => __('Bauhaus', 'decor8ai-virtual-staging'),
            'mediterranean' => __('Mediterranean', 'decor8ai-virtual-staging'),
            'farmhouse' => __('Farmhouse', 'decor8ai-virtual-staging'),
            'victorian' => __('Victorian', 'decor8ai-virtual-staging'),
            'gothic' => __('Gothic', 'decor8ai-virtual-staging'),
            'moroccan' => __('Moroccan', 'decor8ai-virtual-staging'),
            'southwestern' => __('Southwestern', 'decor8ai-virtual-staging'),
            'transitional' => __('Transitional', 'decor8ai-virtual-staging'),
            'maximalist' => __('Maximalist', 'decor8ai-virtual-staging'),
            'arabic' => __('Arabic', 'decor8ai-virtual-staging'),
            'japandi' => __('Japandi', 'decor8ai-virtual-staging'),
            'retrofuturism' => __('Retro Futurism', 'decor8ai-virtual-staging'),
            'artnouveau' => __('Art Nouveau', 'decor8ai-virtual-staging'),
            'urbanmodern' => __('Urban Modern', 'decor8ai-virtual-staging'),
            'wabi_sabi' => __('Wabi Sabi', 'decor8ai-virtual-staging'),
            'grandmillennial' => __('Grandmillennial', 'decor8ai-virtual-staging'),
            'coastalgrandmother' => __('Coastal Grandmother', 'decor8ai-virtual-staging'),
            'newtraditional' => __('New Traditional', 'decor8ai-virtual-staging'),
            'cottagecore' => __('Cottagecore', 'decor8ai-virtual-staging'),
            'luxemodern' => __('Luxe Modern', 'decor8ai-virtual-staging'),
            'high_tech' => __('High Tech', 'decor8ai-virtual-staging'),
            'organicmodern' => __('Organic Modern', 'decor8ai-virtual-staging'),
            'tuscan' => __('Tuscan', 'decor8ai-virtual-staging'),
            'cabin' => __('Cabin', 'decor8ai-virtual-staging'),
            'desertmodern' => __('Desert Modern', 'decor8ai-virtual-staging'),
            'global' => __('Global', 'decor8ai-virtual-staging'),
            'industrialchic' => __('Industrial Chic', 'decor8ai-virtual-staging'),
            'modernfarmhouse' => __('Modern Farmhouse', 'decor8ai-virtual-staging'),
            'europeanclassic' => __('European Classic', 'decor8ai-virtual-staging'),
            'neotraditional' => __('Neo Traditional', 'decor8ai-virtual-staging'),
            'warmminimalist' => __('Warm Minimalist', 'decor8ai-virtual-staging'),
        );
    }
}
