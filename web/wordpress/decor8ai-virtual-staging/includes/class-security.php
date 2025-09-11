<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Security {
    private static $instance = null;
    private $rate_limit_transient_prefix = 'decor8_vs_rate_limit_';
    private $rate_limit_max_requests = 10;
    private $rate_limit_time_window = 300; // 5 minutes

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_filter('decor8_vs_verify_request', array($this, 'verify_request'), 10, 2);
        add_filter('upload_mimes', array($this, 'restrict_upload_mimes'));
        add_filter('wp_handle_upload_prefilter', array($this, 'validate_image_upload'));
    }

    public function verify_request($is_valid, $context = '') {
        decor8_log("Verifying request for context: " . $context, 'debug', __FILE__, __LINE__);
        
        // Verify nonce
        if (!isset($_REQUEST['_wpnonce']) || !wp_verify_nonce($_REQUEST['_wpnonce'], 'decor8_vs_' . $context)) {
            decor8_log("Security check failed: Invalid nonce for context " . $context, 'error', __FILE__, __LINE__);
            return false;
        }

        // Check user capabilities
        if (!current_user_can('upload_files')) {
            decor8_log("Security check failed: User lacks upload_files capability", 'error', __FILE__, __LINE__);
            return false;
        }

        // Check rate limiting
        if (!$this->check_rate_limit()) {
            decor8_log("Security check failed: Rate limit exceeded", 'error', __FILE__, __LINE__);
            return false;
        }

        decor8_log("Request verification passed", 'debug', __FILE__, __LINE__);
        return true;
    }

    private function check_rate_limit() {
        $user_id = get_current_user_id();
        $transient_key = $this->rate_limit_transient_prefix . $user_id;
        
        $current_count = get_transient($transient_key);
        decor8_log("Rate limit check - User: $user_id, Current count: " . ($current_count === false ? 'none' : $current_count), 'debug', __FILE__, __LINE__);
        
        if (false === $current_count) {
            $result = set_transient($transient_key, 1, $this->rate_limit_time_window);
            if (!$result) {
                decor8_log("Failed to set initial rate limit transient for user: $user_id", 'error', __FILE__, __LINE__);
                return false;
            }
            decor8_log("New rate limit counter initialized for user: $user_id", 'debug', __FILE__, __LINE__);
            return true;
        }
        
        if ($current_count >= $this->rate_limit_max_requests) {
            $reset_time = get_option('_transient_timeout_' . $transient_key) - time();
            decor8_log("Rate limit exceeded for user: $user_id. Reset in {$reset_time}s", 'warning', __FILE__, __LINE__);
            return false;
        }
        
        $result = set_transient($transient_key, $current_count + 1, $this->rate_limit_time_window);
        if (!$result) {
            decor8_log("Failed to update rate limit count for user: $user_id", 'error', __FILE__, __LINE__);
            return false;
        }
        
        decor8_log("Rate limit updated - User: $user_id, New count: " . ($current_count + 1), 'debug', __FILE__, __LINE__);
        return true;
    }

    public function restrict_upload_mimes($mimes) {
        // Only apply restrictions if this is a virtual staging upload
        if (isset($_POST['action']) && $_POST['action'] === 'decor8_vs_upload') {
            return array(
                'jpg|jpeg' => 'image/jpeg',
                'png' => 'image/png'
            );
        }
        return $mimes;
    }

    public function validate_image_upload($file) {
        // Only validate if this is a virtual staging upload
        if (!isset($_POST['action']) || $_POST['action'] !== 'decor8_vs_upload') {
            return $file;
        }

        decor8_log("Validating image upload: " . $file['name'], 'debug', __FILE__, __LINE__);
        
        $image_types = array(
            IMAGETYPE_JPEG,
            IMAGETYPE_PNG
        );

        // Check file size (10MB limit)
        if ($file['size'] > 10 * 1024 * 1024) {
            $error_msg = sprintf(
                __('File size must be less than %s', 'decor8ai-virtual-staging'),
                size_format(10 * 1024 * 1024)
            );
            decor8_log("Image validation failed - Size too large: " . $file['size'] . " bytes", 'error', __FILE__, __LINE__);
            $file['error'] = $error_msg;
            return $file;
        }

        // Verify image dimensions
        $image_info = getimagesize($file['tmp_name']);
        if (!$image_info || !in_array($image_info[2], $image_types)) {
            decor8_log("Image validation failed - Invalid format: " . ($image_info ? $image_info[2] : 'unknown'), 'error', __FILE__, __LINE__);
            $file['error'] = __('Invalid image format. Only JPG and PNG are allowed.', 'decor8ai-virtual-staging');
            return $file;
        }

        // Check minimum dimensions
        if ($image_info[0] < 800 || $image_info[1] < 800) {
            decor8_log("Image validation failed - Dimensions too small: {$image_info[0]}x{$image_info[1]}", 'error', __FILE__, __LINE__);
            $file['error'] = __('Image dimensions must be at least 800x800 pixels.', 'decor8ai-virtual-staging');
            return $file;
        }

        decor8_log("Image validation passed: {$image_info[0]}x{$image_info[1]} pixels, " . size_format($file['size']), 'debug', __FILE__, __LINE__);
        return $file;
    }

    public function sanitize_room_type($room_type) {
        $allowed_types = apply_filters('decor8_vs_room_types', array(
            'living-room',
            'bedroom',
            'kitchen',
            'bathroom',
            'dining-room',
            'home-office'
        ));

        return in_array($room_type, $allowed_types) ? $room_type : 'living-room';
    }

    public function sanitize_design_style($style) {
        $allowed_styles = apply_filters('decor8_vs_design_styles', array(
            'modern',
            'minimalist',
            'traditional',
            'industrial',
            'scandinavian'
        ));

        return in_array($style, $allowed_styles) ? $style : 'modern';
    }

    public function get_rate_limit_status() {
        $user_id = get_current_user_id();
        $transient_key = $this->rate_limit_transient_prefix . $user_id;
        $current_count = get_transient($transient_key);

        return array(
            'requests_remaining' => $this->rate_limit_max_requests - ($current_count ?: 0),
            'time_window' => $this->rate_limit_time_window,
            'reset_time' => get_option('_transient_timeout_' . $transient_key)
        );
    }
}