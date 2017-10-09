#!/usr/bin/perl

# script to extract a polygon file's bbox
# output is in a form suitable for the Mapsforge map-writer "bbox" option

# written by Frederik Ramm <frederik@remote.org>, public domain
# adapted by devemux86

$maxx = -360;
$maxy = -360;
$minx = 360;
$miny = 360;

while(<>)
{
   if (/^\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s*$/)
   {
       my ($x, $y) = ($1, $2);
       $maxx = $x if ($x>$maxx);
       $maxy = $y if ($y>$maxy);
       $minx = $x if ($x<$minx);
       $miny = $y if ($y<$miny);
   }
}

$buffer = 0.1;
printf "%f,%f,%f,%f\n", $miny - $buffer, $minx - $buffer, $maxy + $buffer, $maxx + $buffer;
