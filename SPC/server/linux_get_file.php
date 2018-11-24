<?php 
session_start();
include('config.php');
$username = $_SESSION['username'];

// function decrypt($str, $key){ 
//     $str = base64_decode($str);
//     $str = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $str, MCRYPT_MODE_ECB);
//     $block = mcrypt_get_block_size('rijndael_128', 'ecb');
//     $pad = ord($str[($len = strlen($str)) - 1]);
//     $len = strlen($str);
//     $pad = ord($str[$len-1]);
//     return substr($str, 0, strlen($str) - $pad);
// }

if($username==""){
    echo "Cannot view file. You are not logged in...";
}
else{
    if(!isset($_GET['id'])){
        echo "Error! No id was passed";
    }
    else{
        $id = intval($_GET['id']);
        if($id <= 0) {
            die('The ID is invalid!');
        }
        else {
            // Connect to the database
            $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
            if(mysqli_connect_errno()) {
                die("MySQL connection failed: ". mysqli_connect_error());
            }
     
            $query = "SELECT `mime`, `name`, `size`, `data`, `md5sum` FROM $username WHERE `id` = {$id}";
            $result = $dbLink->query($query);
            if($result) {
                // Make sure the result is valid
                if($result->num_rows == 1) {
                // Get the row
                    $row = mysqli_fetch_assoc($result);
     
                    // Print headers
                    $name = $row['name'];
                    if (strpos($name, '/') !== false) {
                        $name = substr(strrchr($row['name'], "/"), 1);
                    }
                    $enc = $row['data'];
                    // $dec = decrypt($enc,$key);
                    // header("Content-Type: text/plain");
                    header("Content-Disposition: inline; filename=".$name);
                    header("Content-Type: ". $row['mime']);
                    echo $enc;
                }
                else {
                    echo 'Error! No file exists with that ID.';
                }
                @mysqli_free_result($result);
            }
            else {
                echo "Error! Query failed: <pre>{$dbLink->error}</pre>";
            }
            @mysqli_close($dbLink);
        }
    }
}

?>