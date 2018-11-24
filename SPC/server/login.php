<?php
session_start();
$ip = "192.168.0.103";
$username = $_SESSION['username'];
if($username!=""){
  header('Location: http://'.$ip.':8000/up.php');
}

include('config.php');
function secure($value){
	$value=trim(strip_tags(addslashes($value)));
	return $value;
  }
?>
<html>
<head>
<title>Login Portal</title>
</head>
<body>
<?php
// include('website.php');
// $website="";
$username="";
if(isset($_POST['submit'])){
  $username=secure($_POST['username']);
  $password=secure($_POST['password']);

if(!$username || !$password){
  echo "<center>You need to fill in a <b>Username</b> and a <b>Password</b>!</center>";
}
else{
  $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username ='".$username."'");
  $num = mysqli_num_rows($res);
  if($num==0){
    echo "The username you have provided does not exist";
  }
  else{
    // $password=md5($password);
    $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."' AND password='".$password."'");
    $num = mysqli_num_rows($res);
    if($num==0){
      echo "The password you have provided does not match the one for the username!";
    }
    else{
      $row=mysqli_fetch_assoc($res);
      $_SESSION['username']=$username;
      header('Location: http://'.$ip.':8000/up.php');
    }
  }
}
}
?>
<html>
<h1 id="head">Login Page</h1>
<FORM action="login.php" method="post" id="form">
<h3 class="opt">Username:</h3><input type="text" name="username" value="<?php echo $username ?>" class="inp">
<h3 class="opt">Password:</h3><input type="password" name="password" value="" class="inp"><br /><br />
<div>    <input type="submit" name="submit" value="Login" class="sub"> 
</FORM>
<a href="forgot_pass.php" class="forg">Forgot password</a><br/><br />
Not registered yet? <a href="register.php" class="reg"><b>Register now!</b></a><br/><br/>
Want to change password? <a href="reset_pass.php" class="reg">Reset password</a>
</html>