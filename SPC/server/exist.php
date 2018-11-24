<?php
session_start();
$ip = getHostByName(getHostName());
$username = $_SESSION['username'];
include('config.php');
function secure($value){
	$value=trim(strip_tags(addslashes($value)));
	return $value;
  }
?>
<html>
<body>
<?php
$username="";
if(isset($_POST['submit'])){
  $username=secure($_POST['username']);
  $password=secure($_POST['password']);

if(!$username || !$password){
  echo "You need to fill both username and password!";
}
else{
  $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username ='".$username."'");
  $num = mysqli_num_rows($res);
  if($num==0){
    echo "The username you have provided does not exist";
  }
  else{
    $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."' AND password='".$password."'");
    $num = mysqli_num_rows($res);
    if($num==0){
      echo "Incorrect Password!";
    }
    else{
      $row=mysqli_fetch_assoc($res);
      $_SESSION['username']=$username;
      echo "True";
    }
  }
}
}
?>
<html>
<FORM action="exist.php" method="post" id="form">
<h3 class="opt">Username:</h3><input type="text" name="username" value="" class="inp">
<h3 class="opt">Password:</h3><input type="password" name="password" value="" class="inp"><br /><br />
<div>    <input type="submit" name="submit" value="Login" class="sub"> 
</FORM>
</html>