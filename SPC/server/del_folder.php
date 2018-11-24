<?php
// Make sure an ID was passed
session_start();
include('config.php');
$username = $_SESSION['username'];
if($username==""){
    echo "Cannot delete file";
}
else{
    // echo $_GET['name'];
if(isset($_GET['name'])) {
// Get the ID
    $name = $_GET['name'];
    // echo $name;
 
    // Make sure the ID is in fact a valid ID
    if($name == "") {
        echo $name;
        die('The NAME is invalid!');
    }
    else {
        // Connect to the database
        $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
        if(mysqli_connect_errno()) {
            die("MySQL connection failed: ". mysqli_connect_error());
        }
 
        // Fetch the file information
        $query = "
            DELETE FROM $username
            WHERE `name` LIKE '{$name}%'";
        // echo $query."<br/>";
        $result = $dbLink->query($query);
 
        if($result) {
            // Make sure the result is valid
            // if($result->num_rows == 1) {
            // // Get the row
            //     $row = mysqli_fetch_assoc($result);
 
            //     // Print headers
            //     $name = $row['name'];
            //     if (strpos($name, '/') !== false) {
            //         $name = substr(strrchr($row['name'], "/"), 1);
            //     }
            //     header("Content-Type: ". $row['mime']);
            //     header("Content-Length: ". $row['size']);
            //     header("Content-Disposition: attachment; filename=".$name);
            //     // Print data
            //     // echo "Hello";
            //     echo $row['data'];
                echo "The folder has been deleted successfully";
            // }
            // else {
                // echo 'Error! No file exists with that NAME.';
            // }
 
            // Free the mysqli resources
            @mysqli_free_result($result);
        }
        else {
            echo "Error! Query failed: <pre>{$dbLink->error}</pre>";
        }
        @mysqli_close($dbLink);
    }
}
else {
    echo 'Error! No FILE was passed.';
}
echo '<p>Go to <a href="up.php">upload</a> page</p>';
}

?>
