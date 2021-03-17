<?php
//WRITE SETTING DATA TO web_com.json

$data = $_REQUEST;
$param = $data['parameter'];
$val = $data['value'];

$info_filename = "sets/web_com.json";

$info = json_decode(file_get_contents($info_filename), true);

//set parameter
if ($param == 'set_T'){
  //  make a float
  $val = floatval($val);
}

$info[$param] = $val;

file_put_contents($info_filename, json_encode($info));

echo $param."=".$val;


?>
