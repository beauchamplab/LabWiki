# SUMA

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

<http://afni.nimh.nih.gov/pub/dist/doc/SUMA/SUMA_doc.htm>

The F8 key can be used to switch between perspective and orthographic projection viewing. Orthographic projection viewing should be used for looking at flat maps.

Spec files referring to flat maps should use embeddimension = 2, and embeddimension = 3 otherwise.

Suma can AFNI can sometimes stop communication with each other.
You can try to restart communication by hitting the "t" key.
The problem may also be fixed if you start suma with the following option:

```
 suma -ah localhost
```

or possibly

```
 suma -ah 127.0.0.1
```

## Volume Rendering in SUMA

Volume rendering can be performed in SUMA as follows by simply creating a displayable objects file with the name of the anatomy that you want to load:
e.g. /Volumes/data1/UT/HP/VolRend.1D.niml.do (SUMA looks for "1D" extension by default, so use that for ease of selection; .niml.do extension is mandatory)

```
 <nido_head
 coord_type = "mobile"
 />
 <3DTex
filename = "HPanatavg+orig.BRIK"
overlay0 = "Balls+tlrc.BRIK"
 />
```

(The overlay is optional). Press Ctrl-Apple-S in SUMA and load the file. Use right click to select a cutting plane, shift-Mouse Wheel to move the cutting plane. Mouse wheel alone moves the brain; this changes the image for some reason.

This can be used, for instance, to make a template for positioning NIRS probes on the head.
Load in the average anatomy. Press "F2" twice to display scale bars with numbers (works better on a black background, F6). Save image and load into Illustrator, create line in Illustrator that is e.g. 5 cm long and scale image so that scale bars (10 mm between large ticks) match this line.

Another option is to use the AFNI volume renderer

3dcalc -datum short -prefix {$ec}anatavgshort -a {$ec}anatavg+orig -expr "a"

open renderer,
Accumulate ON
Roll=270 Pitch = 90 Yaw = 0
Cutouts 1, Right of 0
Func: Use auditory T as func and thresh, color scale = 9,
ShowThru Mode, See Overlay, Cutout Overlay, Remove Small Clusters
