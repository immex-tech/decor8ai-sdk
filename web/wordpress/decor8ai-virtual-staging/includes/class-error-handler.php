<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Error_Handler {
    private static $instance = null;
    private $error_option = 'decor8_vs_errors';
    private $max_errors = 100;
    private $error_lifetime = 604800; // 1 week

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        decor8_log("Initializing Error Handler", 'debug', __FILE__, __LINE__);
        add_action('admin_init', array($this, 'schedule_cleanup'));
        add_action('decor8_vs_error_cleanup', array($this, 'cleanup_errors'));
        add_action('admin_notices', array($this, 'display_admin_notices'));
    }

    public function schedule_cleanup() {
        if (!wp_next_scheduled('decor8_vs_error_cleanup')) {
            wp_schedule_event(time(), 'daily', 'decor8_vs_error_cleanup');
        }
    }

    public function log_error($error, $context = array()) {
        $start_time = microtime(true);
        
        if (empty($error)) {
            decor8_log("Attempted to log empty error message", 'warning', __FILE__, __LINE__);
            return false;
        }

        $errors = $this->get_errors();
        $severity = isset($context['severity']) ? $context['severity'] : 'error';
        
        // Add new error
        $error_entry = array(
            'message' => $error,
            'context' => $context,
            'time' => current_time('timestamp'),
            'user_id' => get_current_user_id(),
            'ip' => $this->get_client_ip(),
            'url' => isset($_SERVER['REQUEST_URI']) ? esc_url_raw(wp_unslash($_SERVER['REQUEST_URI'])) : '',
            'severity' => $severity
        );
        
        $errors[] = $error_entry;
        
        // Keep only recent errors
        $errors = array_slice($errors, -$this->max_errors);
        
        // Log to debug log based on severity
        decor8_log(
            sprintf(
                "Error logged [%s]: %s",
                strtoupper($severity),
                $error
            ),
            $severity,
            __FILE__,
            __LINE__
        );

        $result = update_option($this->error_option, $errors);
        
        if (!$result) {
            decor8_log("Failed to save error to database", 'error', __FILE__, __LINE__);
        }
        
        decor8_log_performance('Error logging operation', $start_time);
        
        return $result;
    }

    public function get_errors($limit = null, $severity = null) {
        $errors = get_option($this->error_option, array());

        if ($severity) {
            $errors = array_filter($errors, function($error) use ($severity) {
                return $error['severity'] === $severity;
            });
        }

        if ($limit) {
            $errors = array_slice($errors, -$limit);
        }

        return $errors;
    }

    public function cleanup_errors() {
        $start_time = microtime(true);
        decor8_log("Starting error cleanup process", 'debug', __FILE__, __LINE__);
        
        $errors = $this->get_errors();
        $initial_count = count($errors);
        $current_time = current_time('timestamp');

        // Remove old errors
        $errors = array_filter($errors, function($error) use ($current_time) {
            return ($current_time - $error['time']) < $this->error_lifetime;
        });
        
        $removed_count = $initial_count - count($errors);
        
        $result = update_option($this->error_option, $errors);
        
        if ($result) {
            decor8_log(
                sprintf("Cleaned up %d old error entries", $removed_count),
                'info',
                __FILE__,
                __LINE__
            );
        } else {
            decor8_log("Failed to update errors during cleanup", 'error', __FILE__, __LINE__);
        }
        
        decor8_log_performance('Error cleanup operation', $start_time);
    }

    public function clear_errors() {
        decor8_log("Clearing all error entries", 'info', __FILE__, __LINE__);
        $result = delete_option($this->error_option);
        
        if ($result) {
            decor8_log("Successfully cleared all error entries", 'info', __FILE__, __LINE__);
        } else {
            decor8_log("Failed to clear error entries", 'error', __FILE__, __LINE__);
        }
        
        return $result;
    }

    public function display_admin_notices() {
        $screen = get_current_screen();
        if (!$screen || !in_array($screen->id, array('toplevel_page_decor8ai-virtual-staging'))) {
            return;
        }

        $errors = $this->get_errors(5);
        if (empty($errors)) {
            return;
        }

        foreach ($errors as $error) {
            $class = 'notice notice-' . esc_attr($error['severity']);
            $message = esc_html($error['message']);
            
            printf(
                '<div class="%1$s"><p>%2$s</p></div>',
                $class,
                $message
            );
        }
    }

    public function get_error_count($severity = null) {
        $errors = $this->get_errors();
        
        if ($severity) {
            $errors = array_filter($errors, function($error) use ($severity) {
                return $error['severity'] === $severity;
            });
        }

        return count($errors);
    }

    private function get_client_ip() {
        $ip = '';
        
        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ip = sanitize_text_field(wp_unslash($_SERVER['HTTP_CLIENT_IP']));
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ip = sanitize_text_field(wp_unslash($_SERVER['HTTP_X_FORWARDED_FOR']));
        } elseif (!empty($_SERVER['REMOTE_ADDR'])) {
            $ip = sanitize_text_field(wp_unslash($_SERVER['REMOTE_ADDR']));
        }

        return $ip;
    }

    public function format_error($error) {
        $output = sprintf(
            '[%s] %s',
            date('Y-m-d H:i:s', $error['time']),
            $error['message']
        );

        if (!empty($error['context'])) {
            $output .= "\nContext: " . print_r($error['context'], true);
        }

        return $output;
    }

    public function export_errors() {
        $errors = $this->get_errors();
        $output = '';

        foreach ($errors as $error) {
            $output .= $this->format_error($error) . "\n\n";
        }

        return $output;
    }

    public function has_critical_errors() {
        $count = $this->get_error_count('critical');
        if ($count > 0) {
            decor8_log(
                sprintf("Found %d critical error(s)", $count),
                'warning',
                __FILE__,
                __LINE__
            );
        }
        return $count > 0;
    }

    public function get_last_error() {
        $errors = $this->get_errors(1);
        return !empty($errors) ? $errors[0] : null;
    }
}