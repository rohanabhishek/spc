<?php
session_start();
include('config.php');
include('validations.php');
$ip = "192.168.0.103";
?>

<html>
<head>
<title>Register Page</title>
</head>
<body>
<?php
$username="";$email="";$conf_pass_error="";
if(isset($_POST['submit']))
{
$username=secure($_POST['username']);
$password=secure($_POST['password']);
$conf_password=secure($_POST['confirm_password']);
$email=secure($_POST['email']);
if(!$username || !$password || !$email)
{
echo "All fields are required to be filled!";
}
else
{
 $result=mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."'");
 $num=mysqli_num_rows($result);
 if($num>0)
{
  echo "This username is already used. Look for another one.";
}
else
{
$result=mysqli_query($connection,"SELECT * FROM spcTable WHERE email='".$email."'");
 $num=mysqli_num_rows($result);
 if($num>0)
{
  $email_error="Email already registered";
}
else
{
if(check_name($username) & check_pass($password) & check_email($email))
{
if($password!=$conf_password)
{
  $conf_pass_error="The password does not match to previous one";
}
else
{
	// echo $password;
	// $password=md5($password);
	// echo $password;
$query=mysqli_query($connection,"INSERT INTO spcTable (username,password,email,sync,`time`) VALUES ('".$username."','".$password."','".$email."',0,NOW())");
if($query)
{
	$q = mysqli_query($connection,
	"CREATE TABLE ".$username."(`id` Int Unsigned Not Null Auto_Increment,
	                            `name` VarChar(255) Not Null Default 'Untitled.txt',
                                `mime` VarChar(50) Not Null Default 'text/plain',
                                `size` BigInt Unsigned Not Null Default 0,
                                `data` LongBlob Not Null,
                                `created` DateTime Not Null,
                                `md5sum` VarChar(40) Not Null,
                                PRIMARY KEY (`id`) );");
	// $q1 = mysqli_query($connection,
	// "CREATE TABLE ".$username."Chat(`id` Int Unsigned Not Null Auto_Increment,
 //    							`name` varchar(40) not null,
 //    							`status` int not null,
 //    							`time` datetime not null,
 //    							`message` varchar(255) not null,
 //    							primary key (`id`) );");

	if($q){
		header('Location: http://'.$ip.':8000/login.php');
		echo "You have registered successfully. Log in with the registered credentials.";
		$username = "";
		$email = "";
	}
	else{
		echo "Error while registering";
	}
}
else
{
echo "Some error occured here";
}}}}}}}
?>
<h1><b>Create an account</b></h1>
<FORM name="login_form" action="register.php" method="post">
<b>Username:</b> <br /> <input type="text" name="username" value="<?php echo $username ?>"> <?php echo $name_error ?>
<br />
<b>Password:</b> <br /> <input type="password" name="password" value=""> <br /> <?php echo $pass_error ?>
<b>Confirm_password:</b> <br /> <input type="password" name="confirm_password" value=""> <?php echo $conf_pass_error ?>
<br />
<b>Email:</b> <br /> <input type="text" name="email" value="<?php echo $email ?>"> <?php echo $email_error ?>
<br /><br />
<input type="submit" name="submit" value="Register">
<br /><br />
By creating an account you agree to our <a href="terms_and_conds.php">Terms & Privacy</a>.<br /><br />
Already Registered? <a href="login.php"><b>Sign in</b></a>
</FORM>


