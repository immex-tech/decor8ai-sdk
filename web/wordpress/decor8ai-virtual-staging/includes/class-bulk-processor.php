<?php
if (!defined('ABSPATH')) {
    exit;
}

class Decor8_VS_Bulk_Processor {
    private static $instance = null;
    private $queue_option = 'decor8_vs_processing_queue';
    private $batch_size = 3;
    private $max_queue_size = 20;
    private $processing_timeout = 600; // 10 minutes

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('init', array($this, 'init_processor'));
        add_action('wp_ajax_decor8_vs_add_to_queue', array($this, 'handle_queue_addition'));
        add_action('wp_ajax_decor8_vs_get_queue_status', array($this, 'get_queue_status'));
        add_action('decor8_vs_process_queue', array($this, 'process_queue'));
    }

    public function init_processor() {
        if (!wp_next_scheduled('decor8_vs_process_queue')) {
            wp_schedule_event(time(), 'every_minute', 'decor8_vs_process_queue');
        }
    }

    public function handle_queue_addition() {
        // Verify request
        if (!apply_filters('decor8_vs_verify_request', false, 'queue_add')) {
            wp_send_json_error('Unauthorized request');
        }

        $files = $_FILES['images'];
        $room_type = sanitize_text_field($_POST['room_type']);
        $design_style = sanitize_text_field($_POST['design_style']);

        // Validate inputs
        if (empty($files)) {
            wp_send_json_error('No files uploaded');
        }

        $queue = $this->get_queue();
        $new_items = array();

        // Process each file
        foreach ($files['name'] as $key => $value) {
            if ($files['error'][$key] === 0) {
                $file = array(
                    'name' => $files['name'][$key],
                    'type' => $files['type'][$key],
                    'tmp_name' => $files['tmp_name'][$key],
                    'error' => $files['error'][$key],
                    'size' => $files['size'][$key]
                );

                // Validate file
                $file = apply_filters('wp_handle_upload_prefilter', $file);
                if (!empty($file['error'])) {
                    continue;
                }

                // Move file to uploads
                $upload = wp_handle_upload($file, array('test_form' => false));
                if (isset($upload['error'])) {
                    continue;
                }

                $new_items[] = array(
                    'file' => $upload['file'],
                    'url' => $upload['url'],
                    'room_type' => $room_type,
                    'design_style' => $design_style,
                    'status' => 'pending',
                    'added' => time(),
                    'processed' => 0,
                    'result' => null,
                    'error' => null
                );
            }
        }

        // Check queue size
        if (count($queue) + count($new_items) > $this->max_queue_size) {
            wp_send_json_error('Queue is full');
        }

        // Add new items to queue
        $queue = array_merge($queue, $new_items);
        update_option($this->queue_option, $queue);

        wp_send_json_success(array(
            'message' => sprintf(
                __('%d images added to queue', 'decor8ai-virtual-staging'),
                count($new_items)
            ),
            'queue_size' => count($queue)
        ));
    }

    public function get_queue_status() {
        // Verify request
        if (!apply_filters('decor8_vs_verify_request', false, 'queue_status')) {
            wp_send_json_error('Unauthorized request');
        }

        $queue = $this->get_queue();
        $stats = array(
            'total' => count($queue),
            'pending' => 0,
            'processing' => 0,
            'completed' => 0,
            'failed' => 0
        );

        foreach ($queue as $item) {
            $stats[$item['status']]++;
        }

        wp_send_json_success($stats);
    }

    public function process_queue() {
        $queue = $this->get_queue();
        $processed = 0;

        foreach ($queue as &$item) {
            // Skip completed or failed items
            if (in_array($item['status'], array('completed', 'failed'))) {
                continue;
            }

            // Skip items that have been processing too long
            if ($item['status'] === 'processing' && 
                (time() - $item['processed']) > $this->processing_timeout) {
                $item['status'] = 'failed';
                $item['error'] = 'Processing timeout';
                continue;
            }

            // Process pending items
            if ($item['status'] === 'pending') {
                $item['status'] = 'processing';
                $item['processed'] = time();

                try {
                    // Process the image
                    $result = apply_filters('decor8_vs_process_image', array(
                        'file' => $item['file'],
                        'room_type' => $item['room_type'],
                        'design_style' => $item['design_style']
                    ));

                    if ($result['success']) {
                        $item['status'] = 'completed';
                        $item['result'] = $result['data'];
                    } else {
                        $item['status'] = 'failed';
                        $item['error'] = $result['error'];
                    }
                } catch (Exception $e) {
                    $item['status'] = 'failed';
                    $item['error'] = $e->getMessage();
                }

                $processed++;
                if ($processed >= $this->batch_size) {
                    break;
                }
            }
        }

        // Clean up old items
        $queue = array_filter($queue, function($item) {
            return time() - $item['added'] < 86400; // Remove items older than 24 hours
        });

        update_option($this->queue_option, $queue);
    }

    private function get_queue() {
        return get_option($this->queue_option, array());
    }

    public function clear_queue() {
        update_option($this->queue_option, array());
    }

    public function get_queue_size() {
        return count($this->get_queue());
    }

    public function is_queue_full() {
        return $this->get_queue_size() >= $this->max_queue_size;
    }
}