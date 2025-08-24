<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_API {
    private $api_key;
    private $api_url = 'https://api.decor8.ai/generate_designs_for_room';
    private $logger;

    public function __construct() {
        $this->api_key = get_option('decor8_vs_api_key');
        $this->logger = Decor8_VS_Logger::get_instance();
        
        decor8_log("=== DECOR8 API: Registering AJAX handlers ===");
        
        // Register AJAX handlers
        add_action('wp_ajax_decor8_process_image', array($this, 'handle_image_processing'));
        add_action('wp_ajax_nopriv_decor8_process_image', array($this, 'handle_image_processing'));
    }

    /**
     * Handle image processing AJAX request
     */
    public function handle_image_processing() {
        decor8_log("=== API: Image processing started ===", 'debug');
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
            $this->logger->log("API Error: " . $error_message, 'error');
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
            $this->logger->log("API Error: " . $error_message, 'error');
            throw new Exception($error_message);
        }

        $body = json_decode(wp_remote_retrieve_body($response), true);
        
        $this->logger->log("API Response Body: " . print_r($body, true), 'debug');
        
        // Check for API error even with 200 status
        if (!empty($body['error'])) {
            decor8_log("API Error (200 status): " . $body['error'], 'error');
            throw new Exception($body['error']);
        }
        
        if (!isset($body['info']['images'][0]['url'])) {
            decor8_log("API Error: Missing image URL in response", 'error');
            throw new Exception(__('Invalid API response - Missing image URL', 'decor8ai-virtual-staging'));
        }

        return array(
            'staged_image_url' => $body['info']['images'][0]['url'],
            'message' => !empty($body['message']) ? $body['message'] : __('Virtual staging completed successfully', 'decor8ai-virtual-staging')
        );
    }

    /**
     * Validate room type
     */
    private function validate_room_type($room_type) {
        $valid_room_types = array(
            'LIVINGROOM', 'BEDROOM', 'KITCHEN', 'BATHROOM', 'DININGROOM',
            'OFFICE', 'KIDSROOM', 'FAMILYROOM', 'READINGNOOK', 'SUNROOM',
            'WALKINCLOSET', 'MUDROOM', 'TOYROOM', 'FOYER', 'POWDERROOM',
            'LAUNDRYROOM', 'GYM', 'BASEMENT', 'GARAGE', 'BALCONY',
            'CAFE', 'HOMEBAR', 'STUDY_ROOM', 'FRONT_PORCH', 'BACK_PORCH',
            'BACK_PATIO'
        );

        if (!in_array($room_type, $valid_room_types)) {
            throw new Exception(__('Invalid room type', 'decor8ai-virtual-staging'));
        }

        return $room_type;
    }

    /**
     * Validate design style
     */
    private function validate_design_style($design_style) {
        $valid_styles = array(
            'MINIMALIST', 'SCANDINAVIAN', 'INDUSTRIAL', 'BOHO', 'TRADITIONAL',
            'ARTDECO', 'MIDCENTURYMODERN', 'COASTAL', 'TROPICAL', 'ECLECTIC',
            'CONTEMPORARY', 'FRENCHCOUNTRY', 'RUSTIC', 'SHABBYCHIC', 'VINTAGE',
            'COUNTRY', 'MODERN', 'IKEA', 'POTTERYBARN', 'WESTELMMODERN',
            'ASIAN_ZEN', 'HOLLYWOODREGENCY', 'BAUHAUS', 'MEDITERRANEAN',
            'FARMHOUSE', 'VICTORIAN', 'GOTHIC', 'MOROCCAN', 'SOUTHWESTERN',
            'TRANSITIONAL', 'MAXIMALIST', 'ARABIC', 'JAPANDI'
        );

        if (!in_array($design_style, $valid_styles)) {
            throw new Exception(__('Invalid design style', 'decor8ai-virtual-staging'));
        }

        return $design_style;
    }
}
