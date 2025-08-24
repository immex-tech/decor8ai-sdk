<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Cache {
    private static $instance = null;
    private $cache_group = 'decor8_vs_cache';
    private $cache_time = 3600; // 1 hour default
    private $image_cache_time = 86400; // 24 hours for images
    private $max_cache_size = 100 * 1024 * 1024; // 100MB limit

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('init', array($this, 'init_cache'));
        add_action('admin_init', array($this, 'schedule_cleanup'));
        add_action('decor8_vs_cache_cleanup', array($this, 'cleanup_cache'));
    }

    public function init_cache() {
        wp_cache_add_global_groups($this->cache_group);
    }

    public function schedule_cleanup() {
        if (!wp_next_scheduled('decor8_vs_cache_cleanup')) {
            wp_schedule_event(time(), 'daily', 'decor8_vs_cache_cleanup');
        }
    }

    public function get($key) {
        return wp_cache_get($key, $this->cache_group);
    }

    public function set($key, $value, $expiration = null) {
        $expiration = $expiration ?: $this->cache_time;
        return wp_cache_set($key, $value, $this->cache_group, $expiration);
    }

    public function delete($key) {
        return wp_cache_delete($key, $this->cache_group);
    }

    public function cache_image($image_url, $image_data) {
        $upload_dir = wp_upload_dir();
        $cache_dir = trailingslashit($upload_dir['basedir']) . 'decor8-vs-cache';
        
        // Create cache directory if it doesn't exist
        if (!file_exists($cache_dir)) {
            wp_mkdir_p($cache_dir);
            file_put_contents($cache_dir . '/.htaccess', 'deny from all');
        }

        // Generate cache filename
        $cache_filename = md5($image_url) . '.jpg';
        $cache_path = $cache_dir . '/' . $cache_filename;

        // Save image to cache
        file_put_contents($cache_path, $image_data);

        // Store cache metadata
        $this->set('image_' . md5($image_url), array(
            'path' => $cache_path,
            'url' => $image_url,
            'time' => time()
        ), $this->image_cache_time);

        return $cache_path;
    }

    public function get_cached_image($image_url) {
        $cache_key = 'image_' . md5($image_url);
        $cached = $this->get($cache_key);

        if (!$cached) {
            return false;
        }

        if (!file_exists($cached['path'])) {
            $this->delete($cache_key);
            return false;
        }

        return $cached['path'];
    }

    public function cleanup_cache() {
        $upload_dir = wp_upload_dir();
        $cache_dir = trailingslashit($upload_dir['basedir']) . 'decor8-vs-cache';

        if (!is_dir($cache_dir)) {
            return;
        }

        $files = glob($cache_dir . '/*');
        $now = time();
        $total_size = 0;

        // Calculate total cache size and remove expired files
        foreach ($files as $file) {
            if (is_file($file)) {
                $total_size += filesize($file);
                $cache_key = 'image_' . md5(basename($file, '.jpg'));
                $cached = $this->get($cache_key);

                // Remove if expired or no metadata
                if (!$cached || ($now - $cached['time']) > $this->image_cache_time) {
                    unlink($file);
                    if ($cached) {
                        $this->delete($cache_key);
                    }
                }
            }
        }

        // If cache is still too large, remove oldest files
        if ($total_size > $this->max_cache_size) {
            $files = glob($cache_dir . '/*');
            usort($files, function($a, $b) {
                return filemtime($a) - filemtime($b);
            });

            while ($total_size > $this->max_cache_size && !empty($files)) {
                $file = array_shift($files);
                $total_size -= filesize($file);
                unlink($file);
                $cache_key = 'image_' . md5(basename($file, '.jpg'));
                $this->delete($cache_key);
            }
        }
    }

    public function get_cache_stats() {
        $upload_dir = wp_upload_dir();
        $cache_dir = trailingslashit($upload_dir['basedir']) . 'decor8-vs-cache';
        $total_size = 0;
        $file_count = 0;

        if (is_dir($cache_dir)) {
            $files = glob($cache_dir . '/*');
            foreach ($files as $file) {
                if (is_file($file)) {
                    $total_size += filesize($file);
                    $file_count++;
                }
            }
        }

        return array(
            'total_size' => size_format($total_size),
            'file_count' => $file_count,
            'max_size' => size_format($this->max_cache_size)
        );
    }

    public function clear_all_cache() {
        $upload_dir = wp_upload_dir();
        $cache_dir = trailingslashit($upload_dir['basedir']) . 'decor8-vs-cache';

        if (is_dir($cache_dir)) {
            $files = glob($cache_dir . '/*');
            foreach ($files as $file) {
                if (is_file($file)) {
                    unlink($file);
                }
            }
        }

        wp_cache_flush();
    }
}