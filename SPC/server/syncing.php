<?php

session_start();

$username = $_SESSION['username'];

$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
if(mysqli_connect_errno()) {
    die("MySQL connection failed: ". mysqli_connect_error());
}

$query = "SELECT sync FROM spcTable WHERE `username`='{$username}'";

$result = $dbLink->query($query);

$res = $result->fetch_assoc();
if($res['sync']==0){
	echo "False";
}
else{
	echo "True";
}

?>