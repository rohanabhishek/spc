<?php
session_start();
include('config.php');
$username = $_SESSION['username'];
if($username==""){
	echo "First go to <a href='login.php'>login</a> page";
}
else{
	echo "Welcome ".$username."<br/><br/>";
    echo "IMPORTANT NOTE:-<br/> Upload with webpage only after encrypting with your corresponding schema.<br/><br/>";
	echo "<form name='f' action='add_file.php' method='post' enctype='multipart/form-data'>
        <input name='uploaded_file' type='file'><br><br/>
        <input name='submit' type='submit' value='Upload'></input>
    </form>";
    echo "<a href='logout.php'>Logout</a>";
    echo "<p>
        <a href='web_list.php?list_file='>See all files</a>
    </p>";
    echo "<a href='enc_schema.html'>Encryption Schema</a><br/><br/>";
    echo "<a href='set_reminder.php'>Set Reminder</a>";
}
?>