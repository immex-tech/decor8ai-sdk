<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Admin {
    private $error_messages = array();
    private $debug_log_file;

    private function debug_log($message) {
        if (empty($this->debug_log_file)) {
            $this->debug_log_file = WP_CONTENT_DIR . '/debug.log';
        }
        $timestamp = date('Y-m-d H:i:s');
        file_put_contents($this->debug_log_file, "[{$timestamp}] DECOR8: {$message}\n", FILE_APPEND);
    }

    public function __construct() {
        $this->debug_log("=== DECOR8 ADMIN INIT ===");
        $this->debug_log('User is admin: ' . (current_user_can('manage_options') ? 'yes' : 'no'));
        add_action('admin_menu', array($this, 'add_admin_menu'), 9);
        add_action('admin_init', array($this, 'register_settings'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
        
        // Debug hook registration
        add_action('admin_notices', function() {
            if (isset($_GET['page']) && $_GET['page'] === 'decor8ai-virtual-staging') {
                error_log('Current screen: ' . get_current_screen()->id);
                error_log('Current user: ' . wp_get_current_user()->user_login);
                error_log('Current page: ' . $_GET['page']);
            }
        });
    }

    public function enqueue_admin_assets($hook) {
        // Only load on plugin's admin page
        if ('toplevel_page_decor8ai-virtual-staging' !== $hook) {
            return;
        }

        wp_enqueue_style(
            'decor8-vs-admin',
            DECOR8_VS_PLUGIN_URL . 'assets/css/admin.css',
            array(),
            DECOR8_VS_VERSION
        );

        wp_enqueue_script(
            'decor8-vs-admin',
            DECOR8_VS_PLUGIN_URL . 'assets/js/admin.js',
            array('jquery'),
            DECOR8_VS_VERSION,
            true
        );
    }

    public function add_admin_menu() {
        $this->debug_log("=== DECOR8 MENU REGISTRATION ===");
        $this->debug_log('Before adding menu - Current user can manage_options: ' . (current_user_can('manage_options') ? 'yes' : 'no'));
        
        try {
            $page = add_menu_page(
                __('Decor8 Virtual Staging', 'decor8ai-virtual-staging'),
                __('Virtual Staging', 'decor8ai-virtual-staging'),
                'manage_options', // Restrict to administrators
                'decor8ai-virtual-staging',
                array($this, 'render_settings_page'),
                'dashicons-admin-customizer',
                30
            );
            
            error_log('Menu page added successfully. Hook: ' . $page);
            error_log('Menu slug: decor8ai-virtual-staging');
            error_log('Callback type: ' . gettype(array($this, 'render_settings_page')));
            
            // Debug menu registration
            global $menu, $submenu;
            error_log('Current admin menu: ' . print_r($menu, true));
            error_log('Current admin submenu: ' . print_r($submenu, true));
            
        } catch (Exception $e) {
            error_log('Error adding menu page: ' . $e->getMessage());
        }
    }

    private function add_error($message, $type = 'error') {
        add_settings_error(
            'decor8_vs_messages',
            'decor8_vs_error',
            $message,
            $type
        );
    }

    public function register_settings() {
        register_setting(
            'decor8_vs_settings',
            'decor8_vs_api_key',
            array(
                'type' => 'string',
                'sanitize_callback' => array($this, 'validate_api_key'),
                'default' => ''
            )
        );
        
        add_settings_section(
            'decor8_vs_main_section',
            __('API Settings', 'decor8ai-virtual-staging'),
            array($this, 'render_section_info'),
            'decor8ai-virtual-staging'
        );

        add_settings_field(
            'decor8_vs_api_key',
            __('API Key', 'decor8ai-virtual-staging'),
            array($this, 'render_api_key_field'),
            'decor8ai-virtual-staging',
            'decor8_vs_main_section'
        );
    }

    public function render_section_info() {
        echo '<p>' . esc_html__('Configure your Decor8 AI Virtual Staging settings below.', 'decor8ai-virtual-staging') . '</p>';
    }

    public function render_settings_page() {
        global $pagenow;
        $this->debug_log("=== DECOR8 SETTINGS PAGE ACCESS ATTEMPT ===");
        $this->debug_log('Current page: ' . $pagenow);
        $this->debug_log('GET params: ' . print_r($_GET, true));
        
        // Debug user capabilities
        $user = wp_get_current_user();
        $this->debug_log('User ID: ' . $user->ID);
        $this->debug_log('User Login: ' . $user->user_login);
        $this->debug_log('User Roles: ' . implode(', ', $user->roles));
        $this->debug_log('User Caps: ' . print_r($user->allcaps, true));
        $this->debug_log('Can manage options: ' . (current_user_can('manage_options') ? 'yes' : 'no'));
        $this->debug_log('Current screen: ' . print_r(get_current_screen(), true));
        
        // Check user capabilities
        if (!current_user_can('manage_options')) {
            error_log('Access denied: User lacks manage_options capability');
            wp_die(
                esc_html__('You do not have sufficient permissions to access this page. You need administrator privileges.', 'decor8ai-virtual-staging'),
                403
            );
        }
        error_log('Access granted: User has manage_options capability');
        
        // Only administrators can modify API settings
        $can_modify_settings = current_user_can('manage_options');

        // Show success/error messages
        settings_errors('decor8_vs_messages');
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <?php if ($can_modify_settings): ?>
                <form action="options.php" method="post">
                    <?php
                    settings_fields('decor8_vs_settings');
                    do_settings_sections('decor8ai-virtual-staging');
                    submit_button();
                    ?>
                </form>
            <?php else: ?>
                <div class="notice notice-info">
                    <p>
                        <?php esc_html_e('Only administrators can modify API settings. Please contact your site administrator for changes.', 'decor8ai-virtual-staging'); ?>
                    </p>
                </div>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row"><?php esc_html_e('API Status', 'decor8ai-virtual-staging'); ?></th>
                        <td>
                            <?php
                            $api_key = get_option('decor8_vs_api_key');
                            if ($api_key) {
                                echo '<span class="dashicons dashicons-yes-alt" style="color: green;"></span> ' . 
                                     esc_html__('API key is configured', 'decor8ai-virtual-staging');
                            } else {
                                echo '<span class="dashicons dashicons-warning" style="color: red;"></span> ' . 
                                     esc_html__('API key is not configured. Please contact your administrator.', 'decor8ai-virtual-staging');
                            }
                            ?>
                        </td>
                    </tr>
                </table>
            <?php endif; ?>

            <div class="decor8-vs-usage">
                <h2><?php esc_html_e('Usage Instructions', 'decor8ai-virtual-staging'); ?></h2>
                
                <div class="decor8-vs-shortcode-info">
                    <h3><?php esc_html_e('Shortcode', 'decor8ai-virtual-staging'); ?></h3>
                    <p><?php esc_html_e('Use this shortcode to add the virtual staging interface to any page:', 'decor8ai-virtual-staging'); ?></p>
                    <code>[decor8_virtual_staging]</code>
                </div>

                <div class="decor8-vs-requirements">
                    <h3><?php esc_html_e('Requirements', 'decor8ai-virtual-staging'); ?></h3>
                    <ul>
                        <li><?php esc_html_e('Maximum image size: 10MB', 'decor8ai-virtual-staging'); ?></li>
                        <li><?php esc_html_e('Supported formats: JPG, PNG', 'decor8ai-virtual-staging'); ?></li>
                        <li><?php esc_html_e('Recommended resolution: 2000x2000 pixels or higher', 'decor8ai-virtual-staging'); ?></li>
                    </ul>
                </div>

                <div class="decor8-vs-support">
                    <h3><?php esc_html_e('Support', 'decor8ai-virtual-staging'); ?></h3>
                    <p>
                        <?php
                        printf(
                            /* translators: %s: Decor8 AI support email */
                            esc_html__('For support, please contact us at %s', 'decor8ai-virtual-staging'),
                            '<a href="mailto:decor8@immex.tech">decor8@immex.tech</a>'
                        );
                        ?>
                    </p>
                </div>
            </div>
        </div>
        <?php
    }

    public function validate_api_key($value) {
        $value = sanitize_text_field($value);
        
        if (empty($value)) {
            $this->add_error(
                __('API key cannot be empty.', 'decor8ai-virtual-staging'),
                'error'
            );
            return '';
        }

        // Basic format validation (you may want to adjust this based on your API key format)
        if (strlen($value) < 32) {
            $this->add_error(
                __('Invalid API key format. Please check your API key.', 'decor8ai-virtual-staging'),
                'error'
            );
            return get_option('decor8_vs_api_key', ''); // Keep the old value
        }

        $this->add_error(
            __('API key saved successfully.', 'decor8ai-virtual-staging'),
            'success'
        );

        return $value;
    }

    public function render_api_key_field() {
        $api_key = get_option('decor8_vs_api_key');
        ?>
        <input type="text" 
               name="decor8_vs_api_key" 
               value="<?php echo esc_attr($api_key); ?>" 
               class="regular-text"
               autocomplete="off"
               placeholder="<?php esc_attr_e('Enter your API key', 'decor8ai-virtual-staging'); ?>">
        <p class="description">
            <?php
            printf(
                /* translators: %s: URL to Decor8 AI dashboard */
                esc_html__('Get your API key from %s', 'decor8ai-virtual-staging'),
                '<a href="https://app.decor8.ai" target="_blank">Decor8 AI Dashboard</a>'
            );
            ?>
        </p>
        <?php
    }
}
