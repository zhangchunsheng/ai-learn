<?php
if(count($argv) < 2) {
    echo "usage: php text_to_image.php path\n";
    exit();
}
$path = $argv[1];

$trainPath = $path . "/train";
$testPath = $path . "/test";

$file = fopen("chn_sim.txt", "r");

$strs = "";
while (!feof($file)) {
    $line = fgets($file);
    if (!empty($line)) {
        $strs .= $line;
    }
}

$strs = str_split_unicode($strs);
foreach($strs as $str) {
    drawTrainText($str);

    $random = mt_rand(1, 10);
    if($random < 2) {
        drawTestText($str);
    }
}

fclose($file);

function str_split_unicode($str, $l = 0) {
    if ($l > 0) {
        $ret = array();
        $len = mb_strlen($str, "UTF-8");
        for ($i = 0; $i < $len; $i += $l) {
            $ret[] = mb_substr($str, $i, $l, "UTF-8");
        }
        return $ret;
    }
    return preg_split("//u", $str, -1, PREG_SPLIT_NO_EMPTY);
}

function drawTrainText($character) {
    global $trainPath;

    drawText($trainPath, $character);
}

function drawTestText($character) {
    global $testPath;

    drawText($testPath, $character);
}

function makeDir($path) {
    if (!is_dir($path)) {
        if(!makeDir(dirname($path))) {
            return false;
        }
        if(!mkdir($path, 0777)) {
            return false;
        } else {
            chmod($path, 0777);
        }
    }
    return true;
}

function drawText($path, $character) {
    $path = $path . "/$character";
    makeDir($path);

    $count = 0;

    // get ttf
    $fontPath = 'font-type';
    $fonts = array();
    if(is_dir($fontPath)) {
        $current_dir = opendir($fontPath);    //opendir()返回一个目录句柄,失败返回false
        while(($file = readdir($current_dir)) !== false) {    //readdir()返回打开目录句柄中的一个条目
            $sub_dir = $fontPath . DIRECTORY_SEPARATOR . $file;    //构建子目录路径
            if($file == '.' || $file == '..') {
                continue;
            } elseif(substr($file, stripos($file, ".") + 1) == "ttf") {    //如果是目录,进行递归
                $fonts[] = "$fontPath/" . $file;
            }
        }
    }

    foreach($fonts as $font) {
        $file = $path . "/" . str_pad($count, 3, "0", STR_PAD_LEFT) . ".png";

        $width = 60;
        $height = 60;

        // Create the image
        $im = imagecreatetruecolor($width, $height);

        // Create some colors
        $white = imagecolorallocate($im, 255, 255, 255);
        $grey = imagecolorallocate($im, 128, 128, 128);
        $black = imagecolorallocate($im, 0, 0, 0);

        $left = 0;
        $right = 0;
        imagefilledrectangle($im, $left, $right, $width, $height, $white);

        // The text to draw
        $text = "$character";

        $size = 40;
        $angle = 0;
        $fontfile = $font;
        $bbox = imagettfbbox($size, $angle, $fontfile, $text);

        $dx = abs($bbox[2] - $bbox[0]);
        $dy = abs($bbox[5] - $bbox[3]);

        $px = abs($width / 2) - abs($dx / 2);
        $py = abs($dy - (abs($height - $dy)) / 2);

        $py = $size + ($height - $size) / 2;

        // Add the text
        imagettftext($im, $size, $angle, $px, $py, $black, $fontfile, $text);

        // Using imagepng() results in clearer text compared with imagejpeg()
        imagepng($im, $file);
        imagedestroy($im);

        $count++;
    }
}