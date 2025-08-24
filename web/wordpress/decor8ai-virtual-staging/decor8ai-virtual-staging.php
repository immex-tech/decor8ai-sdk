<?php
/**
 * Plugin Name: Decor8 AI Virtual Staging
 * Plugin URI: https://decor8.ai
 * Description: Add AI-powered virtual staging capabilities to your real estate website
 * Version: 1.0.1
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * Author: Decor8 AI
 * Author URI: https://decor8.ai
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: decor8ai-virtual-staging
 * Domain Path: /languages
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Write to plugin's debug log
 *
 * @param string $message The message to log
 * @param string $type Optional. The type of message (info, error, debug). Default 'info'.
 */
function decor8_log($message, $type = 'info') {
    $timestamp = date('Y-m-d H:i:s');
    $formatted_message = sprintf("[%s] [%s] %s\n", $timestamp, strtoupper($type), $message);
    file_put_contents(WP_CONTENT_DIR . '/debug.log', $formatted_message, FILE_APPEND);
}

// Define plugin constants
define('DECOR8_VS_VERSION', '1.0.1');
define('DECOR8_VS_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('DECOR8_VS_PLUGIN_URL', plugin_dir_url(__FILE__));
define('DECOR8_VS_PLUGIN_BASENAME', plugin_basename(__FILE__));

// Autoloader for plugin classes
spl_autoload_register(function ($class) {
    $prefix = 'Decor8_VS_';
    $base_dir = DECOR8_VS_PLUGIN_DIR . 'includes/';

    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }

    $relative_class = substr($class, $len);
    $file = $base_dir . 'class-' . strtolower(str_replace('_', '-', $relative_class)) . '.php';

    if (file_exists($file)) {
        require $file;
    }
});

class Decor8_Virtual_Staging {
    private static $instance = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->init_hooks();
    }

    private function init_hooks() {
        // Load text domain for translations
        add_action('plugins_loaded', array($this, 'load_textdomain'));

        // Initialize components
        add_action('init', array($this, 'init'));
        // Initialize admin functionality
        $admin = new Decor8_VS_Admin();
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        
        // Add settings link on plugin page
        add_filter('plugin_action_links_' . DECOR8_VS_PLUGIN_BASENAME, array($this, 'add_settings_link'));
        
        // Register shortcode
        add_shortcode('decor8_virtual_staging', array($this, 'render_staging_interface'));
    }

    public function load_textdomain() {
        load_plugin_textdomain(
            'decor8ai-virtual-staging',
            false,
            dirname(DECOR8_VS_PLUGIN_BASENAME) . '/languages/'
        );
    }

    public function init() {
        // Initialize error handler first
        Decor8_VS_Error_Handler::get_instance();
        
        // Initialize security
        Decor8_VS_Security::get_instance();
        
        // Initialize cache
        Decor8_VS_Cache::get_instance();
        
        // Initialize bulk processor
        Decor8_VS_Bulk_Processor::get_instance();
        
        // Initialize frontend functionality
        new Decor8_VS_Frontend();
        
        // Initialize API handler
        new Decor8_VS_API();
        
        // Set up error handling for uncaught exceptions
        set_exception_handler(function($exception) {
            Decor8_VS_Error_Handler::get_instance()->log_error(
                $exception->getMessage(),
                array(
                    'severity' => 'critical',
                    'file' => $exception->getFile(),
                    'line' => $exception->getLine(),
                    'trace' => $exception->getTraceAsString()
                )
            );
        });
    }

    public function admin_init() {
        // Initialize admin functionality
        new Decor8_VS_Admin();
    }

    public function enqueue_scripts() {
        // Enqueue frontend assets
        wp_enqueue_style(
            'decor8-vs-style',
            DECOR8_VS_PLUGIN_URL . 'assets/css/style.css',
            array(),
            DECOR8_VS_VERSION
        );

        wp_enqueue_script(
            'decor8-vs-script',
            DECOR8_VS_PLUGIN_URL . 'assets/js/virtual-stager.js',
            array('jquery'),
            DECOR8_VS_VERSION,
            true
        );

        // Localize script with necessary data
        wp_localize_script('decor8-vs-script', 'decor8VS', array(
            'ajaxurl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('decor8_vs_nonce'),
            'i18n' => array(
                'uploading' => __('Uploading...', 'decor8ai-virtual-staging'),
                'processing' => __('Processing...', 'decor8ai-virtual-staging'),
                'error' => __('Error occurred. Please try again.', 'decor8ai-virtual-staging'),
                'success' => __('Virtual staging completed!', 'decor8ai-virtual-staging')
            )
        ));
    }

    public function render_staging_interface($atts) {
        // Check if API key is set
        if (!get_option('decor8_vs_api_key')) {
            return sprintf(
                /* translators: %s: URL to plugin settings page */
                __('Please <a href="%s">configure your API key</a> to use virtual staging.', 'decor8ai-virtual-staging'),
                admin_url('admin.php?page=decor8ai-virtual-staging')
            );
        }

        ob_start();
        include DECOR8_VS_PLUGIN_DIR . 'templates/virtual-staging.php';
        return ob_get_clean();
    }

    public function add_settings_link($links) {
        $settings_link = sprintf(
            '<a href="%s">%s</a>',
            admin_url('admin.php?page=decor8ai-virtual-staging'),
            __('Settings', 'decor8ai-virtual-staging')
        );
        array_unshift($links, $settings_link);
        return $links;
    }

    // Activation hook
    public static function activate() {
        // Add default options
        add_option('decor8_vs_api_key', '');
        
        // Set version
        add_option('decor8_vs_version', DECOR8_VS_VERSION);
        
        // Clear permalinks
        flush_rewrite_rules();
    }

    // Deactivation hook
    public static function deactivate() {
        // Clear any scheduled hooks, temporary data, etc.
        flush_rewrite_rules();
    }
}

// Initialize the plugin
function decor8_virtual_staging() {
    return Decor8_Virtual_Staging::get_instance();
}

// Hooks for activation and deactivation
register_activation_hook(__FILE__, array('Decor8_Virtual_Staging', 'activate'));
register_deactivation_hook(__FILE__, array('Decor8_Virtual_Staging', 'deactivate'));

// Start the plugin
add_action('plugins_loaded', function() {
    error_log('Initializing Decor8 Virtual Staging plugin');
    decor8_virtual_staging();
});
