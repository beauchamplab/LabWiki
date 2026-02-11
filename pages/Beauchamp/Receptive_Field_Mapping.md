---
layout: default
title: "Receptive Field Mapping"
parent: Beauchamp
---
# Receptive Field Mapping


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

**Receptive Field Mapping**  
1. Select "HumanLetterDetection" from available KNOT plugins.  
2. On toolbar, open Channel Settings, Stimulus Settings and Behavior Settings windows.  
3. Enter the names of all Channels.  
4. Check to see that the following fields in Stimulus Settings have default values specified below:

:   a. Stimulation: Eccentricity
:   b. Azimuths/Eccentricities: 4
:   c. Elevations/Radii: 16
:   d. Stimulation Rate (Hz): 4
:   e. Stimulation Duty (%): 50

Values in other fields will not matter for fMRI-inspired wedge RF mapping.  
5. Check to see that the following fields in Behavior Settings have default values specified below:

:   a. Blocks: 20 (A block is the number of times the totality of the visual stimuli have been shown.)
:   b. Response Time (ms): 500 ms (Response time pads the end of the continuous trial, so that the LFP from the last stimulation will be captured in the data file.)
:   c. Fix Spot Radius (deg): 0.30
:   d. Sensitivity: 5000.00
:   e. Check "One trial only in Eccentricity." Note that once "Run" is selected in this mode, the continuous "trial" runs its course (whether that is 20 blocks or 500) and cannot be stopped without Force Quitting.
:   f. Uncheck "Lever Required."

Values in other fields will not matter for fMRI-inspired wedge RF mapping.  
6. Instruct the subject to fixate on the central dot. Eyes will be tracked and data discarded posthoc if fixation is poor.  
7. On toolbar, select File: Record Data to File to record data. Press Run. 20 blocks should take about 5-6 minutes. If there is concern that this is too long for the patient to maintain fixation, run in shorter chunks of time and combine data across files.

Back to [Setup Apparatus](Setup_Apparatus.md "Beauchamp:Setup Apparatus").  
On to [Electrical Stimulation](Electrical_Stimulation.md "Beauchamp:Electrical Stimulation").
