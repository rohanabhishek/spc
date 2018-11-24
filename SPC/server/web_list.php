<?php
session_start();
// include('config.php');
$username = $_SESSION['username'];
if($username==""){
	echo "First go to <a href='login.php'>login</a> page";
}
else{
$dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
if(mysqli_connect_errno()) {
    die("MySQL connection failed: ". mysqli_connect_error());
}

$expr=$_GET['list_file'];

if(strpos($expr, '/') !== false){
	$newstr = substr($expr, 0, strrpos( $expr, '/'));
	// $newstr = rtrim($newstr,":");
	// echo $expr." ".$newstr." here<br/>";
	if(strpos($newstr, '/') == false){
		$newstr="";
		// echo $expr." ".$newstr." in A<br/>";
	}
	else{
		$newstr = substr($newstr, 0, strrpos( $newstr, '/'))."/";
		// echo $expr." ".$newstr." in B<br/>";
	}
	// echo $expr." ".$newstr."<br/>";
}

// $newstr = substr($expr, 0, strpos($expr, ':', strpos($expr, ':')+1));
// echo $newstr."<br/>";

if($expr==""){}
else{
	echo "<a href=?list_file=".$newstr."><img src='dir.png'></a>";
	echo "<a href=?list_file=".$newstr."><b>..</b></a><br/>";
}

// echo "<a href=?list_file="."".">..</a><br/>";

function list_file($exp){
	global $dbLink;
	global $username;
	$exp1 = $exp."%";
	$sql1 = "SELECT id, name, mime, size, created, md5sum FROM $username WHERE name LIKE '$exp1'";
	$res = $dbLink->query($sql1);
	$a = array();
	if($res==false){
		echo "No files to display<br/>";
	}
	else{
	while($row = $res->fetch_assoc()){
		$str = $row['name'];	
		$str = substr($str, strlen($exp));
		if (strpos($str, '/') !== false) {
			$array = explode("/", $str);
			if(in_array($array[0],$a)){

			}
			else{
				$a.array_push($a,$array[0]);
			}
		}
		else{
			echo "<a href='get_file.php?id={$row['id']}'><img src='file.png'></a>";
			echo "<a href='get_file.php?id={$row['id']}'>$str {$row['md5sum']}</a>  ";
			echo "<a href='del_file.php?name={$row['name']}'>--Delete--</a><br/>";
       	}
	}
	}
	foreach($a as $row){
		echo "<a href=?list_file=".$exp.$row."/"."><img src='dir.png'></a>";
		echo "<a href=?list_file=".$exp.$row."/".">$row/</a> ";
		echo "<a href=del_folder.php?name=".$exp.$row."/".">--Delete--</a></br>";
	}
}

if (isset($_GET['list_file'])) list_file($expr);

$dbLink->close();

echo "<a href='logout.php'>Logout</a><br/>";

echo "<a href='up.php'>Upload page</a>";

}
?>