<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="styles.css">
    <title>SECURE STORE</title>
</head>

<body>
    <h1> WELCOME TO MY STORE </h1>
    <div class="title-div">
        <img src="cereals.jpg">
        <form method="post">
            Search items <input type="text" name="input">
            <button type="button" >submit</button>
        </form>

<p hidden>?file=</p>
<p hidden>SSBsZWZ0IGEgcGllY2Ugb2YgY29kZSBpbiBhIGZpbGUgY2FsbGVkIHNvdXJjZSAsIEkgYmV0IHlvdSBjYW4ndCByZWFjaCBpdA==</p>
</body>
<!--?file-->
<?php
error_reporting(E_ERROR | E_PARSE);

function includeFile($file) {
    $blacklist = ['self', 'proc','env','environ','printenv'];
    try {
        if (empty($file)) {
            throw new Exception("");
        }
        foreach ($blacklist as $word) {
            if (strpos($file, $word) !== false) {
                throw new Exception("File access blocked ");
            }
        }
        if (!file_exists($file)) {
            throw new Exception("File not found");
        }

      
       $content = file_get_contents($file);
       echo $content;
    }
     catch (Exception $e) {
        echo "" . $e->getMessage();
    }
}

$file = $_GET['file'];
includeFile($file);
$FLAG = getenv('FLAG');

class Admin
{
    public $is_admin = "";
    public $your_secret = "";
    public $my_secret = "";
    public function __construct($in, $ysecret, $msecret)
    {
        $this->is_admin = md5($in);
        $this->your_secret = $ysecret;
        $this->my_secret = $msecret;
    }
    public function __toString()
    {
        return $this->is_admin;
    }
}

if (isset($_COOKIE['can_you_get_me'])) {
    try {
        $f = base64_decode($_COOKIE['can_you_get_me']);
        if (!$f) {
            throw new Exception("");
        }
        $unout = unserialize($f);
        if (!$unout) {
            throw new Exception("\n wrong cookie");
        }
       
        $unout->my_secret = $FLAG;
        if ($unout->is_admin == 0 && $unout->your_secret === $unout->my_secret) {
            echo "Okay here is your flag:", $FLAG;
        } else
            echo "no ";
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
}




?>

</html>
