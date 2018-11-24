<?php 
session_start();
include('config.php');
$username = $_SESSION['username'];
$ip = "192.168.43.198";

function decrypt($str, $key){ 
    $str = base64_decode($str);
    $str = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $str, MCRYPT_MODE_ECB);
    $block = mcrypt_get_block_size('rijndael_128', 'ecb');
    $pad = ord($str[($len = strlen($str)) - 1]);
    $len = strlen($str);
    $pad = ord($str[$len-1]);
    return substr($str, 0, strlen($str) - $pad);
}

if($username==""){
    echo "Cannot view file. You are not logged in...";
}
else{
    if(!isset($_GET['id'])){
        echo "Error! No id was passed";
    }
    else{
        if(!isset($_POST['schema']) || !isset($_POST['key1'])){
            echo "Enter your schema and key<br/><br/>";
            echo "<FORM action='' method ='post'>";
            echo "Schema: <input type='text' name='schema'></input>";
            echo " Key1: <input type='text' name='key1'></input>";
            echo " <input type='submit' name='submit'></input>";
            echo "</FORM>";
        }
        else{
            $schema = $_POST['schema'];
            // $key1 = strval($_POST['key1']);
            $id = intval($_GET['id']);
            $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
            if(mysqli_connect_errno()) {
                die("MySQL connection failed: ". mysqli_connect_error());
            }

            if($id <= 0) {
                die('The ID is invalid!');
            }
            else {
                // Connect to the database
                // $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
                // if(mysqli_connect_errno()) {
                //     die("MySQL connection failed: ". mysqli_connect_error());
                // }
         
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
                        $enc = strval($row['data']);

                        
                        // $dec = decrypt($enc,$key);

                        if($schema=="BLOWFISH"){
                            ///////////////////         RSA
                            $key1 = strval($_POST['key1']);
                            // $key1 = strval($_POST['key1']);
                            $x = "x".$name;
                            $fp = fopen($x,'w');
                            fwrite($fp,$enc);
                            fclose($fp);
                            $fp = fopen('bkey.txt','w');
                            fwrite($fp,$key1);
                            fclose($fp);
                            // $dec = $enc;
                            shell_exec('javac Blowd.java');
                            shell_exec('java Blowd '.$x);
                            
                            $fp = fopen($x,'r');
                            $dec = fread($fp,filesize($x));
                            fclose($fp);

                            if (file_exists($x)) {
                                unlink($x);
                            } else {
                                echo "Cannot decrypt";
                            }
                            if (file_exists('bkey.txt')) {
                                unlink('bkey.txt');
                            } else {
                                echo "Cannot decrypt";
                            }
                        }
                        else if($schema=="AES"){
                            $key1 = strval($_POST['key1']);
                            $dec = decrypt($enc,$key1);
                        }
                        else if($schema=="DES"){
                            $key1 = strval($_POST['key1']);
                            $x = "x".$name;
                            $fp = fopen($x,'w');
                            fwrite($fp,$enc);
                            fclose($fp);
                            shell_exec('javac DESd.java');
                            $dec=shell_exec('java DESd '.$x.' '.$key1);
                            if (file_exists($x)) {
                                unlink($x);
                            } else {
                                echo "Cannot decrypt";
                            }
                        }
                        else{
                            die("Unknown schema!");
                        }
                        header("Content-Disposition: inline; filename=".$name);
                        header("Content-Type: ". $row['mime']);
                        echo $dec;
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
}

?>


<?php
// Make sure an ID was passed
// session_start();
// include('config.php');
// $username = $_SESSION['username'];

// function decrypt($str, $key){ 
//                     $str = base64_decode($str);
//                     $str = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $str, MCRYPT_MODE_ECB);
//                     $block = mcrypt_get_block_size('rijndael_128', 'ecb');
//                     $pad = ord($str[($len = strlen($str)) - 1]);
//                     $len = strlen($str);
//                     $pad = ord($str[$len-1]);
//                     return substr($str, 0, strlen($str) - $pad);
//                 }

// if($username==""){
//     echo "Cannot view file";
// }
// else{
// if(isset($_GET['id'])) {
// // Get the ID
//     $id = intval($_GET['id']);
 
//     // Make sure the ID is in fact a valid ID
//     if($id <= 0) {
//         die('The ID is invalid!');
//     }
//     else {
//         // Connect to the database
//         $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
//         if(mysqli_connect_errno()) {
//             die("MySQL connection failed: ". mysqli_connect_error());
//         }
 
//         // Fetch the file information
//         $query = "
//             SELECT `mime`, `name`, `size`, `data`, `md5sum`
//             FROM $username
//             WHERE `id` = {$id}";
//         $result = $dbLink->query($query);
 
//         if($result) {
//             // Make sure the result is valid
//             if($result->num_rows == 1) {
//             // Get the row
//                 $row = mysqli_fetch_assoc($result);
 
//                 // Print headers
//                 $name = $row['name'];
//                 if (strpos($name, '/') !== false) {
//                     $name = substr(strrchr($row['name'], "/"), 1);
//                 }
//                 $key = "This is a secret";
//                 $enc = "YmxbpgJahch4HRs+9fzYCEupeZrOGorw1I1bZlF00BA=";
//                 // echo("<script type='text/javascript'> var answer = prompt('Enter the key'); </script>");
//                 // echo("<script> document.cookie = 'answer = ' + answer </script>");
//                 // echo $key;
//                 // $x = $_COOKIE['answer'];
//                 // $x = $_COOKIE['answer'];
//                 // echo $x;
//                 // print_r($_COOKIE);
//                 // echo $key."\n";
//                 // $dec = decrypt($enc,$x);
//                 // header("Content-Type: text/plain");
//                 header("Content-Disposition: inline; filename=".$name);
//                 header("Content-Type: ". $row['mime']);
//                 // echo $key;
//                 echo $dec;
//                 // header("filename=a.txt");
//                 // header("Content-Length: ". $row['size']);
//                 // echo $name;
//                 // echo $row['data'];

//             }
//             else {
//                 echo 'Error! No file exists with that ID.';
//             }
 
//             // Free the mysqli resources
//             @mysqli_free_result($result);
//         }
//         else {
//             echo "Error! Query failed: <pre>{$dbLink->error}</pre>";
//         }
//         @mysqli_close($dbLink);
//     }
// }
// else {
//     echo 'Error! No ID was passed.';
// }
// }
?>