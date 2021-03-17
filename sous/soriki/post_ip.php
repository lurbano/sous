<?php

$data = $_REQUEST;
$datafile = "ip_log.json";

echo "Hello: ";
$data["time"] = date("Y-m-d H:i:s");

echo var_dump($data);

file_put_contents($datafile, json_encode($data));

?>
