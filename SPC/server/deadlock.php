<?php

$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
if(mysqli_connect_errno()) {
    die("MySQL connection failed: ". mysqli_connect_error());
}

// $query = "UPDATE spcTable SET `time`=NOW()";

function time_elapsed_string($datetime, $full = false) {
    $now = new DateTime;
    $ago = new DateTime($datetime);
    $diff = $now->diff($ago);
    return $diff->i;
}

$query = "SELECT * FROM spcTable WHERE `sync`=1";
$res = $dbLink->query($query);
while($row = $res->fetch_assoc()){
	$val = intval(time_elapsed_string($row['time'], true));
	if($val >=5 ){
		$username = $row['username'];
		// echo $username.$val;
		$q = "UPDATE spcTable SET `sync`=0 WHERE `username`='".$username."'";
		$r = $dbLink->query($q);
		echo $username." Deadlock done<br/>";
	}
}
?>