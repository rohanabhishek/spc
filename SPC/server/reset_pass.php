<?php
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
$username="";
if(isset($_POST['submit'])){
  $username=secure($_POST['username']);
  $oldpass=secure($_POST['old_pass']);
  $newpass1=secure($_POST['new_pass1']);
  $newpass2=secure($_POST['new_pass2']);

if(!$username || !$oldpass || !$newpass1 || !$newpass2){
  echo "<center>You need to fill in all fields!</center>";
}
else{
  $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."'");
  $num = mysqli_num_rows($res);
  if($num==0){
    echo "The username you have provided does not exist";
  }
  else{
    $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."' AND password='".$oldpass."'");
    $num = mysqli_num_rows($res);
    if($num==0){
      echo "The password you have provided does not match the one for the username!";
    }
    else{
      // $row=mysqli_fetch_assoc($res);
      if($newpass1!=$newpass2){
        echo "Wrong confirm_password";
      }
      else{
        $_SESSION['username']=$username;
        // header('Location: http://10.196.2.33:8000/up.php');
        $q = mysqli_query($connection,"UPDATE spcTable SET password='".$newpass1."'WHERE username='".$username."'");
        if($q){
          echo "Password Updated -- <b>Keep it safe</b>";
        }
        else{
          echo "Something went wrong";
        }
      }
    }
  }
}
}
?>
<html>
<h1 id="head">Reset password</h1>
<FORM action="reset_pass.php" method="post" id="form">
<h3 class="opt">Username:</h3><input type="text" name="username" value="<?php echo $username ?>" class="inp">
<h3 class="opt">Old Password:</h3><input type="password" name="old_pass" value="" class="inp"><br /><br />
<h3 class="opt">New Password:</h3><input type="password" name="new_pass1" value="" class="inp"><br /><br />
<h3 class="opt">Confirm new Password:</h3><input type="password" name="new_pass2" value="" class="inp"><br /><br />
<div>    <input type="submit" name="submit" value="Reset" class="sub"> 
</FORM><br/><br/>
Want to log in? <a href='login.php'>Sign in</a><br/><br/>
Don't remember your password? <a href="forgot_pass.php" class="forg">Forgot password</a><br/><br />
Not registered yet? <a href="register.php" class="reg"><b>Register now!</b></a>
</html>