<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Admin {
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
    }

    public function enqueue_admin_assets($hook) {
        // Only load on plugin's admin page
        if ('toplevel_page_decor8-virtual-staging' !== $hook) {
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
        add_menu_page(
            __('Virtual Staging', 'decor8ai-virtual-staging'),
            __('Virtual Staging', 'decor8ai-virtual-staging'),
            'manage_options',
            'decor8-virtual-staging',
            array($this, 'render_settings_page'),
            'dashicons-admin-generic'
        );
    }

    public function register_settings() {
        register_setting(
            'decor8_vs_settings',
            'decor8_vs_api_key',
            array(
                'type' => 'string',
                'sanitize_callback' => 'sanitize_text_field',
                'default' => ''
            )
        );
        
        add_settings_section(
            'decor8_vs_main_section',
            __('API Settings', 'decor8ai-virtual-staging'),
            array($this, 'render_section_info'),
            'decor8-virtual-staging'
        );

        add_settings_field(
            'decor8_vs_api_key',
            __('API Key', 'decor8ai-virtual-staging'),
            array($this, 'render_api_key_field'),
            'decor8-virtual-staging',
            'decor8_vs_main_section'
        );
    }

    public function render_section_info() {
        echo '<p>' . esc_html__('Configure your Decor8 AI Virtual Staging settings below.', 'decor8ai-virtual-staging') . '</p>';
    }

    public function render_settings_page() {
        // Check user capabilities
        if (!current_user_can('manage_options')) {
            return;
        }

        // Show success/error messages
        settings_errors('decor8_vs_messages');
        ?>
        <div class="wrap">
            <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
            
            <form action="options.php" method="post">
                <?php
                settings_fields('decor8_vs_settings');
                do_settings_sections('decor8-virtual-staging');
                submit_button();
                ?>
            </form>

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
