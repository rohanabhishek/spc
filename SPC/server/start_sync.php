<?php

session_start();

$username = $_SESSION['username'];

$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
if(mysqli_connect_errno()) {
    die("MySQL connection failed: ". mysqli_connect_error());
}

$query = "UPDATE spcTable SET `sync`=1, `time`=NOW() WHERE `username`='{$username}'";

$result = $dbLink->query($query);

// header("Refresh: 10; URL=end_sync.php");

?>