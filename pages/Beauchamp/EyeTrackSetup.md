---
layout: default
title: "EyeTrackSetup"
parent: Beauchamp
---
# EyeTrackSetup


The IFIS system has an external DVI connector. However, this is only compatible with true digital DVI output (as available on a Mac laptop) not with analog DVI output (as available from a VGA connector via a VGA-to-DVI adapter).

Here is a diagram made by Nancy Lin for the setup in the summer of 2006:

[![](../../attachments/EyeTrackSetup/Eyetracker_ScannerRoom.jpg)](../../attachments/EyeTrackSetup/Eyetracker_ScannerRoom.jpg)

Here is some additional info on scanner mods.
Conduit installed: Ravenscroft Betaduct 2" x 2" UPVC
(2" x 2" x 6.5', $22.95 at Ace Electronics)

12/2010: New eSys system uses DVI Dual link (LM 300W panel)
GEForce 9500 GT
2560x1600 @ 60 Hz

supposedly it can also work at 1280x800.

12/17/2010:
Worked OK at 2560x1600 (some flickering at 1280x800) with two configs, both using dual-link DVI cable:
1) older MacBook Pro with DVI output
2) newer MacBook Pro with mini-displayPort to dual-link DVI box ($99 from Apple)

the display must be mirrored in hardware or presentation
mirror\_x()
mirror\_y()
mirror\_z()
or
mirror(bool x, bool y, bool z)

<http://www.neurobs.com/chatter_box/view_thread?id=6156>

According to Gefen, they do not make a box that mirror reflects the display.
Here is their DVI-D KVM switch product:
<http://www.gefen.com/kvm/dproduct.jsp?prod_id=4511>

Also needed would be another mini-displayport to DVI-D box from Apple

optional: for testing in the lab, it would be good to have another DVI-D cable and hi-res monitor
