---
layout: default
title: "Selectivity"
parent: Beauchamp
---
# Selectivity


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Selectivity Tasks

**"One-back" task**  
Every ~twenty trials, a random stimulus is repeated. We tell the patient to press a button every time he/she sees a repeat.  
**"Stop-Sign" Task**   
Every ~twenty trials, a random stimulus is repeated. In addition to all of the test stimuli, we introduce the stop-sign image. We tell the patient to press a button every time he/she sees the stop-sign. This removes the possible confound that the adapting signal is a consequence of the patient looking for repeats.

## Selectivity Check List

1. Select "HumanImageDetection" from available KNOT plugins.  
2. On toolbar, open Channel Settings, Stimulus Settings and Behavior Settings windows.  
3. Enter the names of all Channels.  
4. Check to see that the following fields in Stimulus Settings have default values specified below:

:   a. Min. Target Time (ms): 1000
:   b. Max. Target Time (ms): 8000
:   c. Mean. Target Time (ms): 5000
:   d. Stimulation Rate (Hz): 4
:   e. Stimulation Duty (Hz): 50%
:   f. Select "Selectivity"  

    :   i. Images Stimuli: 50 (Indicate the number of images to screen.)
    :   ii. Azimuth (deg): 0
    :   iii. Elevation (deg): 0
    :   iv. Images Targets: 4 (Indicate the number of target images.)
    :   v. Size (deg): 25
    :   Note that "Images Stimuli Loaded" is a counter as you load up to the number of images indicated in "Images Stimuli." Similarly, "Images Targets Loaded" is a counter as you load up to the number of images indicated in "Images Targets."
    :   vi. Press "Load Stimulus Images" and select all images in Desktop/Organized Images/Screen as default.
    :   vii. Press "Load Target Images" and select all images in Desktop/Organized Images/Targets as default.
    :   viii. If you want to reset the images selected but keep the traces from previously screened images visible, press "Images Reset."

5. Check to see that the following fields in Behavior Settings have default values specified below:

:   a. Blocks: 20
:   b. Pre-Interval (ms): 250
:   c. Intertrial (ms): 1500
:   d. Response Time (ms): 1500
:   e. Sensitivity: 5000
:   f. Too Fast (ms): 100
:   g. Post-Interval (ms): 50
:   h. Fix Spot Radius (deg): 0.10
:   i. Tries: 1
:   j. Check "Lever Required."
:   k. Check "Play Sounds."
:   Note that each "Selectivity" trial is a series of images being screened presented in succession. When a target appears, the subject has Response Time to push the mouse button. Only images screened prior to target onset are plotted.

Back to [Setup Apparatus](Setup_Apparatus.md "Beauchamp:Setup Apparatus").  
On to [Perceptual Biasing](Perceptual_Biasing.md "Beauchamp:Perceptual Biasing").
