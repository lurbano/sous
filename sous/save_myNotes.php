<?php
//WRITE SETTING DATA TO web_com.json

$data = $_REQUEST;
$val = $data['value'];

$myNotes_filename = "myNotes.json";

//set parameter

file_put_contents($myNotes_filename, json_encode($data));

echo "Notes: ".json_encode($data);


?>
