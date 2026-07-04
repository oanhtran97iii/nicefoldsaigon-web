<?php
header("Content-Type: text/plain; charset=utf-8");
$log_file = __DIR__ . "/email_log.txt";

if (!file_exists($log_file)) {
    echo "Log file email_log.txt not found in this directory.\n";
    exit();
}

$lines = file($log_file);
$last_lines = array_slice($lines, -50);

echo "Last 50 lines of email_log.txt:\n";
echo "================================\n";
foreach ($last_lines as $line) {
    echo $line;
}
