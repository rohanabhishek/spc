<?php
session_start();
session_destroy();
$ip = "192.168.0.103";
header('Location: http://'.$ip.':8000/login.php');
?>