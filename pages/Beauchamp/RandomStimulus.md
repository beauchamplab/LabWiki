---
layout: default
title: "RandomStimulus"
parent: Beauchamp
---
# RandomStimulus


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Random Stimulus Sequences, Part 1: optseq2

Optseq2 is a program in the FreeSurfer package for generating random stimulus sequences. In the homepage, you can download the program, view a .ppt w/ more information, and some practice exercises: <http://surfer.nmr.mgh.harvard.edu/optseq/>

Open a terminal window to run the program w/ Unix commands. Set the following parameters:

set tr = 2 (or however many seconds for each trial)

set numev = 30 (or however many trials of each stimulus you will show each run. For example, if 150 trials/run, and 4 stimuli, you could have 30 stimuli/run. numev = 30)

set numtar = 20 (however many trials of a target stimulus you want to show per trial. The target is an extra stimulus that the subject will respond to just to make sure they're paying attention. Here, there's 150-120 = 30 trials left over, so we can make 20 of those target trials. The remaining 10 trials will automatically be made into control trials.)

set out = Example (whatever you want your filename to be)

For the number of total TR's, you may want to manually add 5 NULL's to the end of an RER run to ensure that the last stimulus response has time to rise and fall. So, if you're doing a 150 TR run, you may want to set -ntp 145 and then manually add 5 NULL's to the end yourself.

Then, you'll run the program (change the 1st line if optseq2 isn't in Applications/freesurfer/bin):

/Applications/freesurfer/bin/optseq2 \

--tsearch 0.001 \

--psdwin 0 16 2 \

--nkeep 8 --o {$out} \

--ntp 150 --tr {$tr} \

--polyfit 2 --focb 1 \

--ev stimulus1 {$tr} $numev \

--ev stimulus2 {$tr} $numev \

--ev stimulus3 {$tr} $numev \

--ev stimulus4 {$tr} $numev \

--ev stimulus5 {$tr} $numev \

--ev target {$tr} $numtar

tsearch is the number of hours you want the program to run. nkeep is the number of total runs. ntp sets the number of trials/run.

Since there are 8 runs in this example, there will be 8 output files which look like Example-001.par . Each file will have 5 columns. Left-most column has the exact time (in seconds) that the stimulus is shown, 2nd column is the numerical value which corresponds to each stimulus type (in this example 0-6, 0 corresponding to control), 3rd column is number of seconds of each trial, 4th column is ????, and right-most column is whatever name you gave to each stimulus event (like "stimulus1" in this example).

## Random Stimulus Sequences, Part 2: Matlab

Optseq2 generates a list of what order to show the stimuli in, but does not tell you exactly what stimulus to show.
For instance, it might tell you to present face,face,house,face but we have multiple pictures of faces and houses.
Therefore, a second step is necessary to translate the optseq ordering into actual stimulus files.
This can be easily done in matlab.
Click here for a sample matlab program (others can be found in
/Volumes/data1/lahti0/MikeOldMac/PsychNIH/
[File:TacAMv8.m](../../attachments/RandomStimulus/TacAMv8.m)

Note (10-25-19/Yue): Psychtoolbox system requirement in the scanner room (the recommended program version for each scanner was listed below):

```
Trio scanner -- Matlab (2014b or 2016a); Psychtoolbox (3.0.13beta); GStreamer (1.0.8);
PRISMA scanner -- Matlab (2014b); Psychtoolbox (3.0.13beta); GStreamer (1.0.8).
```
