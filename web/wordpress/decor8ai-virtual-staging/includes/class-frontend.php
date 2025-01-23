<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Frontend {
    public function __construct() {
        // Add any necessary frontend hooks
        add_action('wp_enqueue_scripts', array($this, 'enqueue_frontend_assets'));
    }

    /**
     * Enqueue frontend assets
     */
    public function enqueue_frontend_assets() {
        // Only load assets when shortcode is present
        global $post;
        if (is_a($post, 'WP_Post') && has_shortcode($post->post_content, 'decor8_virtual_staging')) {
            wp_enqueue_style('decor8-vs-style');
            wp_enqueue_script('decor8-vs-script');
        }
    }

    /**
     * Get room types for dropdown
     */
    public static function get_room_types() {
        return array(
            'LIVINGROOM' => __('Living Room', 'decor8ai-virtual-staging'),
            'KITCHEN' => __('Kitchen', 'decor8ai-virtual-staging'),
            'DININGROOM' => __('Dining Room', 'decor8ai-virtual-staging'),
            'BEDROOM' => __('Bedroom', 'decor8ai-virtual-staging'),
            'BATHROOM' => __('Bathroom', 'decor8ai-virtual-staging'),
            'KIDSROOM' => __('Kids Room', 'decor8ai-virtual-staging'),
            'FAMILYROOM' => __('Family Room', 'decor8ai-virtual-staging'),
            'READINGNOOK' => __('Reading Nook', 'decor8ai-virtual-staging'),
            'SUNROOM' => __('Sunroom', 'decor8ai-virtual-staging'),
            'WALKINCLOSET' => __('Walk-In Closet', 'decor8ai-virtual-staging'),
            'MUDROOM' => __('Mud Room', 'decor8ai-virtual-staging'),
            'TOYROOM' => __('Toy Room', 'decor8ai-virtual-staging'),
            'OFFICE' => __('Home Office', 'decor8ai-virtual-staging'),
            'FOYER' => __('Foyer', 'decor8ai-virtual-staging'),
            'POWDERROOM' => __('Powder Room', 'decor8ai-virtual-staging'),
            'LAUNDRYROOM' => __('Laundry Room', 'decor8ai-virtual-staging'),
            'GYM' => __('Home Gym', 'decor8ai-virtual-staging'),
            'BASEMENT' => __('Basement', 'decor8ai-virtual-staging'),
            'GARAGE' => __('Garage', 'decor8ai-virtual-staging'),
            'BALCONY' => __('Balcony', 'decor8ai-virtual-staging'),
            'CAFE' => __('Urban Cafe', 'decor8ai-virtual-staging'),
            'HOMEBAR' => __('Home Bar', 'decor8ai-virtual-staging'),
            'STUDY_ROOM' => __('Study Room', 'decor8ai-virtual-staging'),
            'FRONT_PORCH' => __('Front Porch', 'decor8ai-virtual-staging'),
            'BACK_PORCH' => __('Back Porch', 'decor8ai-virtual-staging'),
            'BACK_PATIO' => __('Back Patio', 'decor8ai-virtual-staging')
        );
    }

    /**
     * Get design styles for dropdown
     */
    public static function get_design_styles() {
        return array(
            'MINIMALIST' => __('Minimalist', 'decor8ai-virtual-staging'),
            'SCANDINAVIAN' => __('Scandinavian', 'decor8ai-virtual-staging'),
            'INDUSTRIAL' => __('Industrial', 'decor8ai-virtual-staging'),
            'BOHO' => __('Boho', 'decor8ai-virtual-staging'),
            'TRADITIONAL' => __('Traditional', 'decor8ai-virtual-staging'),
            'ARTDECO' => __('Art Deco', 'decor8ai-virtual-staging'),
            'MIDCENTURYMODERN' => __('Mid-Century Modern', 'decor8ai-virtual-staging'),
            'COASTAL' => __('Coastal', 'decor8ai-virtual-staging'),
            'TROPICAL' => __('Tropical', 'decor8ai-virtual-staging'),
            'ECLECTIC' => __('Eclectic', 'decor8ai-virtual-staging'),
            'CONTEMPORARY' => __('Contemporary', 'decor8ai-virtual-staging'),
            'FRENCHCOUNTRY' => __('French Country', 'decor8ai-virtual-staging'),
            'RUSTIC' => __('Rustic', 'decor8ai-virtual-staging'),
            'SHABBYCHIC' => __('Shabby Chic', 'decor8ai-virtual-staging'),
            'VINTAGE' => __('Vintage', 'decor8ai-virtual-staging'),
            'COUNTRY' => __('Country', 'decor8ai-virtual-staging'),
            'MODERN' => __('Modern', 'decor8ai-virtual-staging'),
            'IKEA' => __('IKEA', 'decor8ai-virtual-staging'),
            'POTTERYBARN' => __('Pottery Barn', 'decor8ai-virtual-staging'),
            'WESTELMMODERN' => __('West Elm Modern', 'decor8ai-virtual-staging'),
            'ASIAN_ZEN' => __('Asian Zen', 'decor8ai-virtual-staging'),
            'HOLLYWOODREGENCY' => __('Hollywood Regency', 'decor8ai-virtual-staging'),
            'BAUHAUS' => __('Bauhaus', 'decor8ai-virtual-staging'),
            'MEDITERRANEAN' => __('Mediterranean', 'decor8ai-virtual-staging'),
            'FARMHOUSE' => __('Farmhouse', 'decor8ai-virtual-staging'),
            'VICTORIAN' => __('Victorian', 'decor8ai-virtual-staging'),
            'GOTHIC' => __('Gothic', 'decor8ai-virtual-staging'),
            'MOROCCAN' => __('Moroccan', 'decor8ai-virtual-staging'),
            'SOUTHWESTERN' => __('Southwestern', 'decor8ai-virtual-staging'),
            'TRANSITIONAL' => __('Transitional', 'decor8ai-virtual-staging'),
            'MAXIMALIST' => __('Maximalist', 'decor8ai-virtual-staging'),
            'ARABIC' => __('Arabic', 'decor8ai-virtual-staging'),
            'JAPANDI' => __('Japandi', 'decor8ai-virtual-staging')
        );
    }

    /**
     * Render room type dropdown
     */
    public static function render_room_type_dropdown() {
        $room_types = self::get_room_types();
        ?>
        <select id="decor8-room-type" name="room_type" required>
            <option value=""><?php esc_html_e('Select Room Type', 'decor8ai-virtual-staging'); ?></option>
            <?php foreach ($room_types as $value => $label) : ?>
                <option value="<?php echo esc_attr($value); ?>">
                    <?php echo esc_html($label); ?>
                </option>
            <?php endforeach; ?>
        </select>
        <?php
    }

    /**
     * Render design style dropdown
     */
    public static function render_design_style_dropdown() {
        $design_styles = self::get_design_styles();
        ?>
        <select id="decor8-design-style" name="design_style" required>
            <option value=""><?php esc_html_e('Select Design Style', 'decor8ai-virtual-staging'); ?></option>
            <?php foreach ($design_styles as $value => $label) : ?>
                <option value="<?php echo esc_attr($value); ?>">
                    <?php echo esc_html($label); ?>
                </option>
            <?php endforeach; ?>
        </select>
        <?php
    }
}
