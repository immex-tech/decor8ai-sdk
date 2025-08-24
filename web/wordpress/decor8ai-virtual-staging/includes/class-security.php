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
        // Verify nonce
        if (!isset($_REQUEST['_wpnonce']) || !wp_verify_nonce($_REQUEST['_wpnonce'], 'decor8_vs_' . $context)) {
            return false;
        }

        // Check user capabilities
        if (!current_user_can('upload_files')) {
            return false;
        }

        // Check rate limiting
        if (!$this->check_rate_limit()) {
            return false;
        }

        return true;
    }

    private function check_rate_limit() {
        $user_id = get_current_user_id();
        $transient_key = $this->rate_limit_transient_prefix . $user_id;
        
        $current_count = get_transient($transient_key);
        
        if (false === $current_count) {
            set_transient($transient_key, 1, $this->rate_limit_time_window);
            return true;
        }
        
        if ($current_count >= $this->rate_limit_max_requests) {
            return false;
        }
        
        set_transient($transient_key, $current_count + 1, $this->rate_limit_time_window);
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
        $image_types = array(
            IMAGETYPE_JPEG,
            IMAGETYPE_PNG
        );

        // Check file size (10MB limit)
        if ($file['size'] > 10 * 1024 * 1024) {
            $file['error'] = sprintf(
                __('File size must be less than %s', 'decor8ai-virtual-staging'),
                size_format(10 * 1024 * 1024)
            );
            return $file;
        }

        // Verify image dimensions
        $image_info = getimagesize($file['tmp_name']);
        if (!$image_info || !in_array($image_info[2], $image_types)) {
            $file['error'] = __('Invalid image format. Only JPG and PNG are allowed.', 'decor8ai-virtual-staging');
            return $file;
        }

        // Check minimum dimensions
        if ($image_info[0] < 800 || $image_info[1] < 800) {
            $file['error'] = __('Image dimensions must be at least 800x800 pixels.', 'decor8ai-virtual-staging');
            return $file;
        }

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