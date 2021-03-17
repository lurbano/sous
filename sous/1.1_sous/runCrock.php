<?php

$data = $_REQUEST;
$l_on = intval($data['on']);
echo $l_on."|".gettype($l_on)."|";

$info_filename = "sets/web_com.json";
$info = json_decode(file_get_contents($info_filename), true);

$check_id = date("Y-m-d H:i:s");

if ($l_on == 1){
  echo "a";
  $info['runCrockpot'] = 1;
} else {
  echo "b";
  $info['runCrockpot'] = 0;
}

echo json_encode($info);

file_put_contents($info_filename, json_encode($info));

echo $check_id;


?>
