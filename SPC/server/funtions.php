<?php
  function secure($value){
	$value=trim(strip_tags(addslashes($value)));
	return $value;
  }
?>