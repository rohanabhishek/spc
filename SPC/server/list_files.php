<?php
// Connect to the database
session_start();
// include('config.php');
$username = $_SESSION['username'];	
// $username = "";
if($username==""){
	echo "";
}
else{
$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
if(mysqli_connect_errno()) {
    die("MySQL connection failed: ". mysqli_connect_error());
}
$sql = "SELECT id, name, mime, size, created, md5sum FROM $username";
$res = $dbLink->query($sql);
$a = array();
while($row = $res->fetch_assoc()){
	echo $row['id']."|".$row['name']."|".$row['md5sum']."|".$row['size']."|";
}
$dbLink->close();
}
?>