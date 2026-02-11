# NewEyeTrackSetup

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Notes on the SR EyeLink Eye Tracker

1. [Click here to download the PDF of the EyeLink Manual.](../../attachments/NewEyeTrackSetup/EL1000_InstallationGuide_version1.52.pdf.pdf "EL1000 InstallationGuide version1.52.pdf.pdf")

The Beauchamp Lab has two SR Eyelink systems: an Eyelink (for MRI scanner use) and an Eyelink Plus (set up in the lab).

Here are notes on setting up the EyeLink Plus:

- connections:

```
  - laptop to camera via ethernet
  - laptop to display PC via ethernet (USB ethernet port)
  - illuminator to camera
```

Ethernet connections must be in place before Host Laptop is turned on.

Display PC needs to have IP address manually set to

```
  - use any web browser to access files on Host Laptop by going to XXX  in address bar
```

To run an experiment, have the host PC (the laptop) on and have the EyeLink camera running before starting the experiment program, otherwise the program will time out.

Setting up for new monitor is simple: go to the settings on the Host PC, click the screen setup icon, and enter the measurements it asks for.

Starting the EyeLink Eyetracker System:

```
    1)	Turn on Display PC (the Mac)
    2)	Turn on Host PC (the laptop)
    3)	Select “Eyelink” operating system to initiate startup
    4)	Make sure lens cap is off of camera
    5)	On Mac, open Chrome, and go to the EyeLink bookmark
    6)	On the Mac start the experiment you want to run (should have Eye on white background as the logo)
     a.	E.g. GCWindow
    7)	Experiment program is now running
    8)	Have subject sit with chin on rest, with forehead against bubblewrap, and look forward.
    9)	Start calibration (shortcut is ‘c’) from Host PC
     a.	Hit enter when subject’s gaze is correct. The calibration will advance automatically.
               If it doesn’t, hit ‘a’ to toggle the auto calibrate trigger. Hitting ‘enter’ will accept a point manually.
     b.	If there is a problem with saturation of the image, click ‘autocontrast’ (‘a’ shortcut’)
   10)	After calibration, you can validate the calibration if desired (‘v’ shortcut)
   11)	Start recording the experiment (‘o’ shortcut)
```

Shutting down the Eyelink System:

```
    1)	Close the experiment (you can abort in the middle or save the data via a ‘save file’ UI popup if you complete it)
    2)	Click “Shutdown Host” to shutdown the Host PC
     a.	The Host PC will complete shutdown and prompt you to turn off the computer when complete
    3)	Recap the lens
    4)	Shut down the Mac (if desired)
```

Dongle is required to use the Experiment Builder or Data Viewer programs from EyeLink.

Ricky's Notes on Scanner Eyetracking

1. Camera sensors: We currently have 2 camera sensors: the Eyelink SR 1000 and 1000 Plus.
a. Eyelink 1000 Plus

```
                                                              i.      Has laptop
                                                            ii.      Has Camera sensor built into (non-MR compatible)
                                                           iii.      It is best to use this setup with the laptop outside of the scanner completely.
                                                          iv.      This might be a good setup for remote use (e.g., Bill in the OR)
```

b. Eyelink 1000

```
                                                              i.      We have two desktops that work only for Eyelink 1000
                                                            ii.      I moved one desktop to live in Scanner 5 and full set it up
                                                           iii.      The other desktop, I think we should set this one up in S104X and replace the Eyelink 1000 Plus
                                                          iv.      The idea then would be that we could just take off the camera sensor and move it in the behavioral lab or the scanner, whichever one is being used. And if this works well, we could then just buy another sensor and keep each setup permanent.
                                                            v.      For the scanner, we would not gain any benefit from using an Eyelink 1000 Plus because the sensor is not MR-compatible.
                                                          vi.      We are missing a Desktop stand + illuminator and power cable. Marcus can send us a new power cable for free, but a new desktop stand + illuminator would cost ~$3,000. But, he says we should very likely have the stand somewhere, but we did not immediately find it here at BCM. We might do some more digging when you are back.
```

2. Scanner Mount:
a. The wooden mount that made worked out perfectly. We un-mounted the BOLD screen from the trolley and actually just slid the mount over the trolley for the 32” BOLD Screen. The camera and illumination can be some just barely at the bottom of the screen, not a huge obstruction.
b. We found a very good convergence between the illumination and camera/lens. These should not really need to be adjusted. We want to keep the camera and the illumination source maximally separated for best results.
c. When re-attaching the arm, only the ball on pivot should be adjusted to simultaneously point both at the subject’s right eye. There should not be any need to adjust horizontal position or angle of either the illuminator or the camera lens. We should be able to just point both and focus the camera lens.
3. Adjusting the camera focus and pupil detection:
a. How to focus the eyes

```
                                                              i.      First, use the broad view to make sure the camera is pointed to the eyes. (Press the left arrow to jump between zoom view and broad view).
                                                            ii.      Second, click on the area where the pupil is. This will only look for the pupil within the vicinity of the mouse click.
                                                           iii.      Third, focus the camera lens
```

1. This requires some twiddling but the idea of the camera focus is to adjust it until the corneal reflection is minimized
b. For each subject, there will need to be some manual adjustment of the image intensity segmentation on the Eyelink Computer. The idea is as follows:

```
                                                              i.      Up Arrow and Down Arrow: Adjust these until the pupil is maximally filled with no black border around it. This should be an intensity level between 75 and 135 out of 255 pixel intensity values
                                                            ii.      +/- keys: Adjust the corneal reflection. Adjust to minimize the size and eliminate the white border around the glint.
```

c. Drift check

```
                                                              i.      Marcus recommends running a Drift check between scanning runs. If the drift check is off, then it might be necessary to rerun the calibration. This sometimes is necessary as subject and/or camera may have moved.
```

4. DOS commands:
a. t – starts tracking
b. edit calibr.ini – edit calibration. Better not to actually edit things here, but just note the default values. Override them in the final.ini file or with MATLAB commands.
c. edit physical.ini – only edit this when things like the screen size or distance from the camera are changed
d. edit final.ini – edit this file to override anything in all other .ini scripts. But MATLAB commands will override even anything in here. Make sure that there are a few break lines at the end of this script though!

**Johannes Notes** 
Must install the Eyelink library for software to work on the Mac.

## troubleshooting notes from Marcus Johnson of SR Research

Here are instructions for the best eye tracker positioning for use with a 32 channel head coil. You can use this same setup for the 12 channel head coil, so I might recommend just keeping things set up as they are currently (which is the setup described below).
First, for the 32 channel head coil, the ideal position is to have the camera offset by a few cm (5-10) from the central position towards the side of the eye being tracked. In other words, if you are behind the eye tracker in the scanning room, you want the camera slightly off to the side of the eye being tracked. You then want to have the illuminator positioned as further peripherally as it can go (to make it further out from center from the camera). For the right eye, you can put the camera on the left side of the mounting bar and slide it as far right as it can go. Then put the illuminator on the right side of the mounting bar and position it at the right-most edge of the post (as far as it can go without coming back off the bar). Then position the entire mount so that the camera is 5-10cm to the right of center. If the illuminator is blocked by the bore wall at that position then you might have to move it back in (back towards the center of the bar) a little so that it isn’t blocked. We have to use this kind of positioning because the mask can on the front of the head coil will cause shadows in other configurations. We have tested lots of different positioning schemes/orientations, and this one is the most effective, even for most skinny-headed people. For the left eye, just reverse the above (keeping camera near center and illuminator off to the left as much as possible).

The following are instructions for making sure that the system will work properly after positioning things based on the basic setup described above. You might also want to check out chapter "7. Long Range Mount Installation" of the EyeLink 1000 Installation Guide (see link above).

and section "3.2.7 Long Range Mount Participant Setup, Monocular or Binocular" of the EyeLink 1000 User Manual, which you can get at the following page (see link above).

1a) Make sure that you are using the front surfaced head-coil mirror that we provided (or one that you provide) and not a rear surfaced mirror. When you use rear-surfaced mirrors (where the reflective part is behind glass), there are two problems you are introducing: 1) You can get extra reflections that can block the pupil. Sending the light through the glass before it gets reflected back to the camera (and back through on its way back) disrupts the light. The front-surfaced mirror has the reflective part on the front of the mirror and does not suffer from this problem. 2) Some mirrors that reflect visible light fine do not reflect infrared light as well. The mirrors we provide are constructed to as to be highly reflective in the part of the spectrum of infrared light that the system uses. Please note, front surfaced mirrors scratch very easily, so please avoid any contact with the mirror unless absolutely necessary.

2a) Make sure to maintain some separation between the camera and illuminator. If the camera and illuminator are right next to one another this proximity will result in the bright pupil (i.e., red-eye) effect. Our system is a dark-pupil eye tracker, and it depends on the pupil looking dark in the camera image. If the light is too close the the camera like that then you will reduce the contrast that the system needs to detect the pupil.

3a) Be careful in positioning the subject so that the top of the subject’s head is touching the innermost (i.e., head-side-most) part of the head coil and so that their head is elevated with padding to make it as high as it can be (without the subject feeling uncomfortable) . As the subject moves lower (so that the top of their head is not touching the innermost part of the head coil) the eyes move to a position that is more likely to be blocked by the face mask of the head coil. The face mask gets wider as it goes lower on the mask (i.e., more foot-side on the mask), so the lower the subject, the more likely that the eye will be blocked. Similarly, if the back of the head is too low (because not enough padding is used under the head) then the eyes will be further back in any shadows that are caused by the head coil. So, you want to keep the head as far back and high as possible.

4a) Make sure to point the camera and illuminator properly. The system’s illuminator can be pointed in a manner that is somewhat independent of the camera, so we want to make sure that the light is pointed at the camera image. Here is how you can do it: First, point the camera using the overall mounting bar’s ball and socket so that the eye that you are going to track is in the center of the camera image. Then, use the triangular knob on the bottom of the illuminator to change the horizontal pointing of the illuminator. As you did so, watch the global view of the camera (you can transfer the image to the Display PC when in Camera Setup mode using the Enter key or by clicking on Image -> Display PC on the Host PC; you can switch between which image is being transferred by using the left and right arrows -- both keyboards work the same in Camera Setup Mode). Make sure it is positioned so that the cyan color is maximized in the camera image, especially at the center, where the eye is (cyan is the CR color, and the CR is on the bright end of the grayscale of the camera image, so brighter parts of the image are colored cyan). Then use the round knob that holds the illuminator to the mounting bar to adjust the vertical positioning of the camera (again to maximize the cyan in the camera image). Another strategy is to ask the person being scanned to look at the illuminator as you do this and tell you when the LEDs are brightest (they will glow red to the subject).

After doing this, please follow the steps in sections 1b to 6b) below. Then, once you have set the thresholds for the pupil and CR so that they look right, check the threshold values of the pupil. If the value is below 70 then you don't have enough IR light. If this is the case then double-check the pointing of the illuminator. If the pointing is good, then use the two screws on the bottom-front of the illuminator to bring the illuminator's focusing lens out a bit. If the value is above 135 then you have too much light. You can use the two screws on the bottom-front of the illuminator's focusing lens in a bit. The focusing lens, has a little scale on it -- the lens should be positioned so that the point on the scale matches the eye-to-camera distance, but I've found that if you have the lens a little further out than the eye to camera distance it might work better.

The above are basically one-time setup things. Once you have the setup right, you can do the following for each subject to maximize the performance of the system:

1b) Bring in the test subject. Point the eye tracker so that only the eye you are tracking is in the global view of the system. If you would like to see the camera image on the Display PC monitor then press Enter on either keyboard (or click Image -> Display PC on the Host PC). You can use the Left/Right arrow on either keyboard to switch between camera image views (Global View, Zoomed Views).

2b) If the Search Limits are on (if they are on then you will see a red ellipse for each eye being tracked) then use the Global View to make sure they are centered on the eye. You can do so by clicking on the pupil on either the Host PC or the Display PC. You can adjust the size of the Search Limits by using Alt and the arrow keys. The system will only search for the eye inside the Search Limits if they are on. It’s a good idea to keep them on to potentially exclude false alarm detections of eyes.

3b) If crosshairs appear on the eye (you might have to do a little rough focusing to make them appear) that means you have acquired the eye -- now you are done needing to use the Global View and can switch to focusing on the Zoomed View. You can use the Left/Right arrows on either keyboard to switch which view is being displayed on the Display PC.

4b) Using the Zoomed View, focus the camera so that the corneal reflection (CR) is as small as possible. Don't pay attention to any part of the image besides the CR when focusing the camera. You turn the physical camera lens on the eye tracker to focus the image (the part of the lens that you turn will be the part with the little brass screws sticking out of it). There will be a sweet spot in the focusing for which the CR is as small as possible. If you turn the lens in either direction (clockwise, counter-clockwise) from this sweet spot, then the CR will become larger. Again, try to make the CR as small as possible.

5b) If the subject has droopy eyelids or some other physical characteristic is blocking the camera's view of part of the pupil you can consider changing the Pupil Tracking mode from Centroid to Ellipse. Ellipse is noisier than Centroid in general, but it is more robust in the face of partial pupil occlusion (i.e., it will be less likely to result in tracking loss when the subject's pupil is being partially blocked by things like eyelids). You can do so via the buttons on the left side of the Host PC monitor when in Camera Setup mode.

6b) Press A for auto-threshold. You can then use the up/down arrows on either keyboard or the Pupil threshold buttons on the Host PC to adjust the pupil threshold. Bring the pupil threshold up if needed to fill in any black ring around the pupil. Make sure you are not in danger of any peripheral blue merging with the pupil blue. You can have the subject look at the four corners of the screen to check if this may happen. It's not a problem if there is blue in the periphery (like on the eyelashes) as long as it doesn't merge with the actual pupil blue as the subject looks around. Then adjust the CR threshold. Bring the CR threshold down if needed to make sure no white pixels remain in the CR. You might get a lot of cyan in the periphery when it's properly set -- again this is not a problem if it doesn't run the risk of merging with the actual CR cyan (which it usually won't for the CR). If you see a secondary reflection at the bottom of the eye have the subject look at the four corners. If the crosshairs jump to the secondary reflection you can try raising the threshold back up to get them to stop jumping. If you've followed the steps in the Quick Start Guide box 6, though, you really shouldn't ever see this happening.

7b) Calibrate/Validate -- we recommend after validating that you get .5 degrees of less average error and 1.0 degrees or less maximum error.

Important note for calibration/validation -- you can press the Backspace key to go back and repeat points if the subject looks away before the point moves (subjects often make these anticipatory eye movements). Pressing Backspace more than once will go back even further in the calibration routine. For particularly difficult subjects you can also press the Spacebar again after starting a calibration to put the system in Manual mode. This will require you to then press the Spacebar to accept fixation for each calibration point. To set it so that the calibrations/validations begin in manual mode you can select Force Manual Accept from the Set Options screen on the Host PC. Manual mode is useful when a subject has a strong tendency to move his/her eyes before the target moves to its next location (i.e., when the subject makes anticipatory eye movements).
