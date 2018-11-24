<?php
$name_error="";$pass_error="";$conf_pass_error="";$email_error="";
function check_name($value){
  $len=strlen($value);
  GLOBAL $name_error;
  $checkname="/^[[:alnum:]]+$/";
  if($len<5 || $len>15 || !preg_match($checkname,$value)){
    $name_error="Username must be 5 to 15 characters long and contain only alphabets and digits";
    return false;
  }
  else{
    return true;
  }
}
function check_pass($value){
  $len=strlen($value);
  GLOBAL $pass_error;
  $checkpass= "/(?=^.{6,12}$)(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_])^.*/";
  if(!preg_match($checkpass,$value)){
    $pass_error="Password must be 6 to 12 characters long, and must contain atleast - <li>1 uppercase alphabet </li> <li>1 lowercase alphabet </li> <li>1 digit and </li> <li>1 special character </li>";
    return false; 
  }
  else{
    return true;
  }
}
function check_email($value){
  $len=strlen($value);
  GLOBAL $email_error;
  $checkemail = "/^[a-z0-9]+([_\\.-][a-z0-9]+)*@([a-z0-9]+([\.-][a-z0-9]+)*)+\\.[a-z]{2,}$/i";
  if(!preg_match($checkemail,$value)){
    $email_error="Invalid email. Please enter valid email";
    return false;
  }
  else{
    return true;
  }
}
function secure($value){
	$value=trim(strip_tags(addslashes($value)));
	return $value;
  }
?>