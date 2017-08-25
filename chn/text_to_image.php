<?php
if(count($argv) < 2) {
    echo "usage: php text_to_image.php path\n";
    exit();
}
$path = $argv[1];

$file = $path . "/train/啊.png";

// Create the image
$im = imagecreatetruecolor(60, 60);

// The text to draw
$text = '啊';
// Replace path by your own font path
$font = 'font-type/micro_yahei.ttf';

// Add the text
imagettftext($im, 40, 0, 10, 10, $black, $font, $text);

// Using imagepng() results in clearer text compared with imagejpeg()
imagepng($im, $file);
imagedestroy($im);