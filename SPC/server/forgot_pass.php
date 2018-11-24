<?php
session_start();
include('config.php');

// Please specify your Mail Server - Example: mail.yourdomain.com.
//ini_set("SMTP","mail.google.com");
//ini_set("SMTP","smtp.charter.net");
// Please specify an SMTP Number 25 and 8889 are valid SMTP Ports.
//ini_set("smtp_port","25");
// Please specify the return address to use
//ini_set('sendmail_from', 'suraj.y2009@gmail.com');

$email="";$email_error="";
echo "<b>An email will be sent to your registered email address containing the password.</b><br />";
if(isset($_POST['submit'])){
$email=trim(strip_tags(addslashes($_POST['email'])));
if(!$email)
{
$email_error="Email address must be filled";
}
else
{
$res=mysqli_query($connection,"SELECT * FROM spcTable WHERE email='".$email."'");
$num=mysqli_num_rows($res);
if($num==0)
{
echo "Email address you have provided is not registered. Go to register page to create an account.";
}
else if($res)
{
$row=mysqli_fetch_assoc($res);
$password=$row['password'];
$sent= mail($email,'Account Password',"Here is your password: ".$password."\n\nPlease try not to lose it again!",'From: suraj.y2009@gmail.com');
if($sent)
{
echo "Email successfully sent";
}
else
{
echo "Some error occured :-(";
}
}
else 
{
echo "Some error occured. Please try again.";
}
}
}
?>
<html>
<head>
<title>Forgot password</title>
</head>
<body>
<FORM action="forgot_pass.php" method="post">
<b>Email: </b><br /><input type="text" name="email" value="<?php echo $email; ?>"> <?php echo $email_error; ?> <br /><br />
<input type="submit" name="submit" value="Send"><br /><br />
<a href="login.php">Login</a> | <a href="register.php">Register</a>
</FORM>
</body>
</html>