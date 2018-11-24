<?php
// Check if a file has been uploaded
session_start();
$username = $_SESSION['username'];
if(isset($_FILES['uploaded_file'])) {
    // Make sure the file was sent without errors
    if($_FILES['uploaded_file']['error'] == 0) {
        // Connect to the database
        $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
        if(mysqli_connect_errno()) {
            die("MySQL connection failed: ". mysqli_connect_error());
        }
 
        // Gather all required data
        $name = $dbLink->real_escape_string($_FILES['uploaded_file']['name']);
        $mime = $dbLink->real_escape_string($_FILES['uploaded_file']['type']);
        $data = $dbLink->real_escape_string(file_get_contents($_FILES['uploaded_file']['tmp_name']));
        $size = intval($_FILES['uploaded_file']['size']);
        $myhash = md5_file($_FILES['uploaded_file']['tmp_name']);
 		// echo "SELECT name FROM $username WHERE name=$name";
        $r = mysqli_query($dbLink,"SELECT name FROM ".$username." WHERE name='".$name."'");
        $n = mysqli_num_rows($r);
        if($n!=0){
            // echo "Found";
            $query = "UPDATE ".$username." SET `data`='{$data}',`size`='{$size}',`md5sum`='{$myhash}',`mime`='{$mime}',`created`=NOW() WHERE `name`='{$name}'";
        }
        else{
            // echo "Not found";
            $query = "
            INSERT INTO $username (
                `name`, `mime`, `size`, `data`, `created`, `md5sum`
            )
            VALUES (
                '{$name}', '{$mime}', '{$size}', '{$data}', NOW(), '{$myhash}'
            )";
        }
        // Execute the query
        $result = $dbLink->query($query);
 
        // Check if it was successfull
        if($result) {
            echo 'Success! Your file was successfully added!';
            // echo $mime;
        }
        else {
        	echo $myhash;
            echo '<br/>Error! Failed to insert the file'
               . "<pre>{$dbLink->error}</pre>";
        }
    }
    else {
        echo 'An error accured while the file was being uploaded. '
           . 'Error code: '. intval($_FILES['uploaded_file']['error']);
    }
 
    // Close the mysql connection
    $dbLink->close();
}
else {
    echo 'Error! A file was not sent!';
}
 
// Echo a link back to the main page
echo '<p>Click <a href="up.php">here</a> to go back</p>';
?>
