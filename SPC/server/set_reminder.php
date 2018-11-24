<?php
session_start();
$ip = "192.168.43.198";
$username = $_SESSION['username'];
if($username==""){
  header('Location: http://'.$ip.':8000/up.php');
}

include('config.php');
function secure($value){
	$value=trim(strip_tags(addslashes($value)));
	return $value;
  }
// include('website.php');
// $website="";
// $username="";
if(isset($_POST['submit'])){
  	$email=secure($_POST['email']);
  	$x=secure($_POST['x']);

	if(!$email || !$x){
  		echo "<center>You need to fill in an <b>Email</b> and a <b>Day</b> of the week!</center>";
	}
	else{
		// echo $email.$username.$x;
	    $res = mysqli_query($connection,"SELECT * FROM spcTable WHERE username='".$username."' AND email='".$email."'");
	  	$num = mysqli_num_rows($res);
	  	if($num==0){
	    	echo "The email you have provided is not yours!";
	  	}
  		else{
  			// echo $email.$username.$x;
  			$x = intval($x);
  			$x = $x -1;
  			$x = strval($x);
  			// echo 'python reminder.py '.$email.' '.$x;
  			shell_exec('python reminder.py '.$email.' '.$x);
  		}
	}
}
?>
<html>
<h1 id="head">Login Page</h1>
<FORM action="set_reminder.php" method="post" id="form">
<h3 class="opt">Email for reminder:</h3><input type="text" name="email" value="<?php echo $email ?>" class="inp">
<h3 class="opt">Day of the week:</h3>
	<input type="radio" name="x" value="1" class="inp" checked>Monday<br />
	<input type="radio" name="x" value="2" class="inp">Tuesday<br />
	<input type="radio" name="x" value="3" class="inp">Wednesday<br />
	<input type="radio" name="x" value="4" class="inp">Thursday<br />
	<input type="radio" name="x" value="5" class="inp">Friday<br />
	<input type="radio" name="x" value="6" class="inp">Saturday<br />
	<input type="radio" name="x" value="7" class="inp">Sunday<br />
	<br />
<input type="submit" name="submit" value="Submit" class="sub"> 
</FORM>
</html>