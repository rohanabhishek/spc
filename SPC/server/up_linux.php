<?php
// Check if a file has been uploaded
session_start();
$username = $_SESSION['username'];
// echo $_POST['md5sum'];
// echo $username;


$mime_types = array(
            0 => 'text/plain',
            '' => 'text/plain',
            'txt' => 'text/plain',
            'htm' => 'text/html',
            'html' => 'text/html',
            'php' => 'text/html',
            'css' => 'text/css',
            'js' => 'application/javascript',
            'json' => 'application/json',
            'xml' => 'application/xml',
            'swf' => 'application/x-shockwave-flash',
            'flv' => 'video/x-flv',
            'py' => 'text/plain',
            'java' => 'text/plain',
            'sh' => 'text/plain',

            // images
            'png' => 'image/png',
            'jpe' => 'image/jpeg',
            'jpeg' => 'image/jpeg',
            'jpg' => 'image/jpeg',
            'gif' => 'image/gif',
            'bmp' => 'image/bmp',
            'ico' => 'image/vnd.microsoft.icon',
            'tiff' => 'image/tiff',
            'tif' => 'image/tiff',
            'svg' => 'image/svg+xml',
            'svgz' => 'image/svg+xml',

            // archives
            'zip' => 'application/zip',
            'rar' => 'application/x-rar-compressed',
            'exe' => 'application/x-msdownload',
            'msi' => 'application/x-msdownload',
            'cab' => 'application/vnd.ms-cab-compressed',

            // audio/video
            'mp3' => 'audio/mpeg',
            'mp4' => 'video/mp4',
            'mkv' => 'video/quicktime',
            'qt' => 'video/quicktime',
            'mov' => 'video/quicktime',

            // adobe
            'pdf' => 'application/pdf',
            'psd' => 'image/vnd.adobe.photoshop',
            'ai' => 'application/postscript',
            'eps' => 'application/postscript',
            'ps' => 'application/postscript',

            // ms office
            'doc' => 'application/msword',
            'rtf' => 'application/rtf',
            'xls' => 'application/vnd.ms-excel',
            'ppt' => 'application/vnd.ms-powerpoint',

            // open office
            'odt' => 'application/vnd.oasis.opendocument.text',
            'ods' => 'application/vnd.oasis.opendocument.spreadsheet',
        );


if(isset($_FILES['uploaded_file'])) {
    // echo "Yes";
    // Make sure the file was sent without errors
    if($_FILES['uploaded_file']['error'] == 0) {
        // Connect to the database
        $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
        if(mysqli_connect_errno()) {
            die("MySQL connection failed: ". mysqli_connect_error());
        }
        // Gather all required data
        $name = $dbLink->real_escape_string($_POST['path']);
        $mime = $mime_types[substr(strrchr($name, "."), 1)];
        $data = $dbLink->real_escape_string(file_get_contents($_FILES['uploaded_file']['tmp_name']));
        $size = intval($_FILES['uploaded_file']['size']);
        $myhash = $dbLink->real_escape_string($_POST['md5sum']);
        $verify = md5_file($_FILES['uploaded_file']['tmp_name']);
        // print_r($_FILES);
        // echo $_FILES['uploaded_file']['type'];
        // echo $mime;
        // echo $name;
        // echo $myhash;
        // echo "Hi";
        // echo $_POST['md5sum'];
        // Create the SQL query
        $r = mysqli_query($dbLink,"SELECT name FROM ".$username." WHERE name='".$name."'");
        $n = mysqli_num_rows($r);
        if($n!=0){
            // echo "Found";
            $query = "UPDATE ".$username." SET `data`='{$data}',`size`='{$size}',`mime`='{$mime}',`md5sum`='{$myhash}',`created`=NOW()
             WHERE `name`='{$name}'";
             // echo "Found".$mime;
             // $result = $dbLink->query($query);
        }
        else{
            // echo "Not found".$mime;
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
            // echo 'Success! Your file was successfully added!';
            // echo $name;
            echo $verify;
        }
        else {
            // echo $myhash;
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
else{
    echo "No";
    $dbLink = new mysqli('localhost', 'root', 'password', 'spcUsers');
    if(mysqli_connect_errno()) {
       die("MySQL connection failed: ". mysqli_connect_error());
    }
    $name = $dbLink->real_escape_string($_POST['path']);
    $r = mysqli_query($dbLink,"SELECT name FROM ".$username." WHERE name='".$name."'");
    $n = mysqli_num_rows($r);
    if($n==0){
        $query = "
            INSERT INTO $username (
                `name`, `mime`, `size`, `data`, `created`, `md5sum`
            )
            VALUES (
                '{$name}','',0,'', NOW(),'')";
        $result = $dbLink->query($query);
    }
    // echo "Empty";
}
?>

<html>
<FORM action="up_linux.php" method="post">
<input type="file" name="uploaded_file">
<input type='text' name='path'>
<input type='text' name='md5sum'>
<input type="submit" name="submit" value="Upload"> 
</FORM>
</html>