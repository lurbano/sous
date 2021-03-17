<?php

$info_filename = "sets/web_com.json";

$info = json_decode(file_get_contents($info_filename), true);

$check_id = date("Y-m-d H:i:s");

$info["runCrockpot"] = false;

file_put_contents($info_filename, json_encode($info));

echo $check_id;


?>
