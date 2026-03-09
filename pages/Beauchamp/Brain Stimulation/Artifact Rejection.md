---
layout: default
title: artifact rejection
parent: Brain Stimulation
date_created: 2026-03-06
---
# Artifact Rejection

_Date created: 2026-03-06_

> Quick Access
> - [Home](index.md "Beauchamp")
> - [Publications](pages/Beauchamp/Publications.md "Beauchamp:Publications")
> - [Resources](DataSharing.md "Beauchamp:DataSharing")

###  General Workflow

1. artifact rejection on interest channels
2. downsample channels
3. convert to .mat files
4. load into RAVE

> [!NOTE]
> Artifact rejection pipeline already involves bipolar referencing--no need to do this again in RAVE. 

### Pipeline

1. load ns5 file
2. take a look at the raw data
3. bipolar rereferencing
4. figure out timing of pulse locations -- plot sync pulse from events channel
5. clean sync pulse
6. edge, find_peaks, or first derivative method
7. extract stim onset and artifact window
8. remove a few irrecoverable samples if necessary
9. detrend to remove DC offset
10. find average to build template
11. template subtraction
12. interpolate -- take any point that is NaN and replaces it with moving mean
13. filter
14. downsample to 2K
15. convert to .mat files

### MATLAB Code

[artifact_rejection.m](artifact_rejection.m)

### Notes

- spacing on sEEG probes is 3 mm for the first two contacts and 5 mm for the rest -- keep this in mind for bipolar referencing
- the first artifact might look quite different than the rest -- may have to make a separate template
- many systems (not ours) use the recording ground as a current return -- NOT recommended
- 8 V limit on the amplifier
- neighboring channel has better recovery than the stimulating channel
- when using stimulator.play with multiple repeats in your code, keep in mind that there is a small delay between each play
- longer pulse duration = more artifact
- bipolar rereference around the stimulating electrode (contact before rereferenced to contact after)
- check for bad channels on the raw data (60 Hz noise, electrodes out of brain, etc.)
- make sure in your task code you store stim parameters for each trial so that artifact rejection is easier later on