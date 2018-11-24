<?php 
include('config.php');
$ip = "192.168.0.103";

function decrypt($str, $key){ 
    $str = base64_decode($str);
    $str = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $str, MCRYPT_MODE_ECB);
    $block = mcrypt_get_block_size('rijndael_128', 'ecb');
    $pad = ord($str[($len = strlen($str)) - 1]);
    $len = strlen($str);
    $pad = ord($str[$len-1]);
    return substr($str, 0, strlen($str) - $pad);
}
if(isset($_GET['username']) && isset($_GET['password']) && isset($_GET['id']) && isset($_GET['schema']) && isset($_GET['key'])){
    $username = $_GET['username'];
    $id = intval($_GET['id']);
    $schema = $_GET['schema'];
    $key1 = $_GET['key'];
    // echo $key1;
    $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
    if(mysqli_connect_errno()) {
        die("MySQL connection failed: ". mysqli_connect_error());
    }
    $query = "SELECT `mime`, `name`, `size`, `data`, `md5sum` FROM $username WHERE `id` = {$id}";
    $result = $dbLink->query($query);
    if($result) {
        if($result->num_rows == 1) {
            $row = mysqli_fetch_assoc($result);
            $name = $row['name'];
            if (strpos($name, '/') !== false) {
                $name = substr(strrchr($row['name'], "/"), 1);
            }
            $enc = strval($row['data']);
            if($schema=="BLOWFISH"){
                $x = "x".$name;
                $fp = fopen($x,'w');
                fwrite($fp,$enc);
                fclose($fp);
                $fp = fopen('bkey.txt','w');
                fwrite($fp,$key1);
                fclose($fp);
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
                // $key1 = strval($_POST['key1']);
                $dec = decrypt($enc,$key1);
            }
            else if($schema=="DES"){
                // $key1 = strval($_POST['key1']);
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
    }
}
else{
    echo "Bye";
}

?>