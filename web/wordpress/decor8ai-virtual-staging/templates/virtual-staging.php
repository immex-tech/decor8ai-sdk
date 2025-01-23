<?php
if (!defined('ABSPATH')) {
    exit;
}
?>

<div class="decor8-virtual-staging-container">
    <!-- Header Section -->
    <div class="decor8-vs-header">
        <h2><?php esc_html_e('Virtual Staging', 'decor8ai-virtual-staging'); ?></h2>
        <p class="description">
            <?php esc_html_e('Transform empty rooms into beautifully staged spaces using AI technology.', 'decor8ai-virtual-staging'); ?>
        </p>
    </div>

    <!-- Main Form -->
    <form id="decor8-staging-form" class="decor8-vs-form" enctype="multipart/form-data">
        <!-- Image Upload Section -->
        <div class="decor8-vs-upload-section">
            <label for="decor8-image-upload" class="decor8-vs-label">
                <?php esc_html_e('Upload Room Photo', 'decor8ai-virtual-staging'); ?>
            </label>
            
            <div class="decor8-vs-upload-area" id="decor8-upload-area">
                <input type="file" 
                       id="decor8-image-upload" 
                       name="image" 
                       accept="image/jpeg,image/png"
                       required>
                <div class="decor8-vs-upload-placeholder">
                    <span class="dashicons dashicons-upload"></span>
                    <p><?php esc_html_e('Drag & drop your image here or click to browse', 'decor8ai-virtual-staging'); ?></p>
                    <small><?php esc_html_e('Supported formats: JPG, PNG (Max 10MB)', 'decor8ai-virtual-staging'); ?></small>
                </div>
                <div class="decor8-vs-preview" id="decor8-image-preview" style="display: none;">
                    <img src="" alt="<?php esc_attr_e('Preview', 'decor8ai-virtual-staging'); ?>">
                    <button type="button" class="decor8-vs-remove-image">
                        <span class="dashicons dashicons-no-alt"></span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Room Type and Style Selection -->
        <div class="decor8-vs-options-section">
            <div class="decor8-vs-option">
                <label for="decor8-room-type" class="decor8-vs-label">
                    <?php esc_html_e('Room Type', 'decor8ai-virtual-staging'); ?>
                </label>
                <?php Decor8_VS_Frontend::render_room_type_dropdown(); ?>
            </div>

            <div class="decor8-vs-option">
                <label for="decor8-design-style" class="decor8-vs-label">
                    <?php esc_html_e('Design Style', 'decor8ai-virtual-staging'); ?>
                </label>
                <?php Decor8_VS_Frontend::render_design_style_dropdown(); ?>
            </div>
        </div>

        <!-- Submit Button -->
        <div class="decor8-vs-submit-section">
            <button type="submit" class="decor8-vs-submit button button-primary">
                <?php esc_html_e('Generate Virtual Staging', 'decor8ai-virtual-staging'); ?>
            </button>
        </div>

        <!-- Progress Indicator -->
        <div class="decor8-vs-progress" style="display: none;">
            <div class="decor8-vs-progress-bar">
                <div class="decor8-vs-progress-indicator"></div>
            </div>
            <p class="decor8-vs-progress-text">
                <?php esc_html_e('Processing...', 'decor8ai-virtual-staging'); ?>
            </p>
        </div>

        <!-- Error Messages -->
        <div class="decor8-vs-error" style="display: none;">
            <p class="decor8-vs-error-message"></p>
        </div>
    </form>

    <!-- Results Section -->
    <div class="decor8-vs-results" style="display: none;">
        <h3><?php esc_html_e('Virtual Staging Result', 'decor8ai-virtual-staging'); ?></h3>
        
        <div class="decor8-vs-comparison">
            <div class="decor8-vs-original">
                <h4><?php esc_html_e('Original', 'decor8ai-virtual-staging'); ?></h4>
                <img src="" alt="<?php esc_attr_e('Original Room', 'decor8ai-virtual-staging'); ?>">
            </div>
            
            <div class="decor8-vs-staged">
                <h4><?php esc_html_e('Staged', 'decor8ai-virtual-staging'); ?></h4>
                <img src="" alt="<?php esc_attr_e('Staged Room', 'decor8ai-virtual-staging'); ?>">
                <a href="#" class="button decor8-vs-download" download>
                    <span class="dashicons dashicons-download"></span>
                    <?php esc_html_e('Download', 'decor8ai-virtual-staging'); ?>
                </a>
            </div>
        </div>

        <button type="button" class="button decor8-vs-start-new">
            <?php esc_html_e('Start New Staging', 'decor8ai-virtual-staging'); ?>
        </button>
    </div>
</div>
