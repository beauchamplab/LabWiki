# BrainPix

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

# Introduction

Sometimes, participants want pictures of their brain. This page describes one way to make these pictures. There are many ways to do this, but in general, whatever images you give your participants should probably not have their research identifier on them, and it's good practice to avoid giving the participant any image that shows a (real or perceived) incidental finding. Keep in mind that not everyone is familiar with the way brains look, so you should attempt to make a “pretty” picture that does not give the impression that there’s, say, a missing chunk of brain because of the way the slice cuts through. A second pair of eyes can be very useful for this. Also keep in mind who you're giving these images to. The considerations that are necessary for a healthy control undergraduate majoring in neuroscience (for instance) are different than a patient being treated for anxiety.

If you are giving images to patients, you should (subtly) find out from them if they want them for their own personal use (e.g. Facebook profile picture) or to give to their doctor. In most cases, research images are not designed to be used for medical purposes, and you should discuss with the participant that this is the case prior to giving them the images. This particular consideration is part of why the following method of making participant brain pictures is my preferred method. If the participant intends to use it as 'the coolest possible picture of my brain,' these images will (hopefully) make them happy. However, they are less likely to take colorized images to their doctor, which will potentially avoid headaches for you, the researcher, down the line.

# Pictures

First, do your normal setup (get raw data, convert to .nii or .BRIK/.HEAD).

Then, open the anatomical (probably T1) in afni.

Set the anatomical image as both overlay and underlay.

[![](../../attachments/BrainPix/PrettyPix_1.png)](../../attachments/BrainPix/PrettyPix_1.png)

Right click the color bar, and a menu will pop up. Choose the option 'Choose Colorscale.' This will open up a new menu, choose 'Spectrum:yellow\_to\_cyan+gap.' (Of course, many of these will make cool images, this is just an example of \*my\* go-to brain picture strategy.)

[![](../../attachments/BrainPix/PrettyPix_2.png)](../../attachments/BrainPix/PrettyPix_2.png)

The display will now look something like this:

[![](../../attachments/BrainPix/PrettyPix_3.png)](../../attachments/BrainPix/PrettyPix_3.png)

Check the box for "Pos?" so that 0 is at the bottom of this colorscale, rather than the middle.

[![](../../attachments/BrainPix/PrettyPix_4.png)](../../attachments/BrainPix/PrettyPix_4.png)
[![](../../attachments/BrainPix/PrettyPix_5.png)](../../attachments/BrainPix/PrettyPix_5.png)

And now tweak the top of the range until it looks cool. Obviously, this is a pretty subjective point, but I try to make the brain all one color and the not-brain next to it a different color.

[![](../../attachments/BrainPix/PrettyPix_6.png)](../../attachments/BrainPix/PrettyPix_6.png)
[![](../../attachments/BrainPix/PrettyPix_7.png)](../../attachments/BrainPix/PrettyPix_7.png)

Navigate to a slice in each view that is pretty. Again, pretty subjective, but it should look like a brain, be as symmetric-looking as possible, and not appear to have a chunk missing. Try your best not to make it look like there's something deathly wrong with their brain. I find that a point in the thalamus a few slices away from the midline tends to make a nice brain picture in all three views. Now, save the images. You can choose the format by right-clicking on the "Sav1.<ext>" button at the bottom of each of the display windows. The default on the version I have installed is .jpg, and that's what I like to use. Left-click this button, and a new window will appear where you can choose the name of the image you want to save. Do this for all three views.

[![](../../attachments/BrainPix/PrettyPix_8.png)](../../attachments/BrainPix/PrettyPix_8.png)

# Video

You can also make a flythrough video, which is pretty cool, too. Take the open windows you have from the pictures, and turn off the overlay.

[![](../../attachments/BrainPix/PrettyPix_9.png)](../../attachments/BrainPix/PrettyPix_9.png)

On the sagittal view, use the same button that you used to choose the format of your picture, and this time pick .mpg. Left-click, and you'll be given the option to name the video, as well as choose the start and stop slice (you don't have to change "blowup"). You could leave these at 0 and the max, and it would be fine. You could also scroll through the image (before you click this button) to find the first image on each end with enough ear that the background looks dark. That's pretty optional, but it does make for nicer videos.

Hit "Set" to make the video, and send it off to your adoring research participant.
