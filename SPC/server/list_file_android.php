<?php
// echo $_GET['username'];
// echo $_GET['password'];
if(isset($_GET['username']) && isset($_GET['password'])) {
	$username=$_GET['username'];
	$password=$_GET['password'];
	$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
	if(mysqli_connect_errno()) {
	    die("MySQL connection failed: ". mysqli_connect_error());
	}
	$res = mysqli_query($dbLink,"SELECT * FROM spcTable WHERE username='".$username."' AND password='".$password."'");
    $num = mysqli_num_rows($res);
    if($num==0){
      echo "The password you have provided does not match the one for the username!";
    }
	else{
		$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
		if(mysqli_connect_errno()) {
		    die("MySQL connection failed: ". mysqli_connect_error());
		}
		$query = "SELECT id, name, mime FROM $username";
		$res = $dbLink->query($query);
		while($row = $res->fetch_assoc()){
			echo $row['id']." ".$row['name']." ";
		}
	}
}
else{
	echo "Bye";
}
?>