# EditingCortSurf

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

## What if I have created a surface model and it looks bad?

Sometimes the cortical surface model created by FreeSurfer contains large errors.
For instance, in this picture, part of the pia-arachnoid-dura has been classified as part of the cortex.
[![](../../attachments/EditingCortSurf/Probe.0004.jpg)](../../attachments/EditingCortSurf/Probe.0004.jpg)
To fix this error, AFNI's "draw dataset" plug-in can be used to try and fix the problem.
Change the {$ec}\_anatavg+orig dataset directly. (If something goes wrong, a new one can be made from the original T1s).
Set the drawing value to 0 and pick a paintbrush style.
Identify the offending voxels and paint them in black. Here are before and after shots of painting. Note that all voxels in the bad part of the surface most be painted, although only one slice is shown here.
[![](../../attachments/EditingCortSurf/Beauchamp_before.jpg)](../../attachments/EditingCortSurf/Beauchamp_before.jpg)[![](../../attachments/EditingCortSurf/Beauchamp_after.jpg)](../../attachments/EditingCortSurf/Beauchamp_after.jpg)

Then, rerun the surface creation routine.

```
 mv graham_tim graham_tim_v0
 /Volumes/data9/surfaces/scripts/@prep_dir {$ec} $subj
 /Volumes/data9/surfaces/scripts/@recon {$ec} $subj
```
