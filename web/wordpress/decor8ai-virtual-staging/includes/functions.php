<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Write to plugin's debug log
 *
 * @param string $message The message to log
 * @param string $type Optional. The type of message (info, error, debug). Default 'info'.
 * @param string|null $file Optional. The file where the log was triggered
 * @param int|null $line Optional. The line number where the log was triggered
 */
function decor8_log($message, $type = 'info', $file = null, $line = null) {
    $timestamp = date('Y-m-d H:i:s');
    $location = '';
    
    if ($file && $line) {
        $file = basename($file);
        $location = " [$file:$line]";
    }
    
    $formatted_message = sprintf(
        "[%s] [%s]%s %s\n", 
        $timestamp, 
        strtoupper($type),
        $location,
        $message
    );
    
    // Log to WordPress debug.log if WP_DEBUG_LOG is enabled
    if (defined('WP_DEBUG_LOG') && WP_DEBUG_LOG) {
        error_log($formatted_message);
    }
    
    // Also log to our plugin's log file
    $log_file = WP_CONTENT_DIR . '/decor8-virtual-staging-debug.log';
    file_put_contents($log_file, $formatted_message, FILE_APPEND);
}

/**
 * Get current memory usage in a human-readable format
 * 
 * @return string Memory usage (e.g., "1.2 MB")
 */
function decor8_get_memory_usage() {
    $mem_usage = memory_get_usage(true);
    
    if ($mem_usage < 1024) {
        return $mem_usage . " bytes";
    } elseif ($mem_usage < 1048576) {
        return round($mem_usage/1024, 2) . " KB";
    } else {
        return round($mem_usage/1048576, 2) . " MB";
    }
}

/**
 * Log performance metrics
 * 
 * @param string $operation The operation being measured
 * @param float $start_time The start time from microtime(true)
 */
function decor8_log_performance($operation, $start_time) {
    $end_time = microtime(true);
    $execution_time = round(($end_time - $start_time) * 1000, 2); // Convert to milliseconds
    $memory = decor8_get_memory_usage();
    
    decor8_log(
        sprintf(
            "Performance - %s: %sms, Memory: %s",
            $operation,
            $execution_time,
            $memory
        ),
        'debug'
    );
}