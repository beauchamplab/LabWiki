---
title: VolAverage
parent: Beauchamp
---
# VolAverage

|  |  |
| --- | --- |
| [Brain picture](../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](index.md "Beauchamp")
- [Lab Members](Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](Lab_Alums.md)
- [Projects](Projects.md)
- [Publications](Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](Subjects.md "Beauchamp:Subjects")

- [Software Installation](Software_Installation.md)
- [Ordering](Ordering.md)
- [MRI Data Analysis](MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](TMS.md "Beauchamp:TMS")

## Creating Volume Average Datasets with AFNI

It is usually best to make a special directory to hold the average and individual subject datasets.

Start with a volume average anatomy. Usually we average the skull-stripped brain. Copy each anatomy into the group directory.

```
 foreach ec (FL FM FN FQ FS FU FW FY FZ)
 cd /Volumes/data1/UT/{$ec}/afni
 cp ??anatavgSS_at+tlrc.*  /Volumes/data1/UT/TacRelGroup/
 end
```

Make the average
3dmerge -prefix GroupSSanat ??anatavgSS\_at+tlrc.HEAD

The functional average is slightly more complex. First, we must make a +tlrc version of each subject's GLM output.

```
 foreach ec (FL FM FN FQ FS FU FW FY FZ)
 cd /Volumes/data1/UT/{$ec}/afni
 ls {$ec}v1mr_REML+orig.HEAD  {$ec}TacH_noall+orig.HEAD {$ec}TacL_noall+orig.HEAD  {$ec}anatavgSS_at+tlrc.HEAD
 foreach dset ({$ec}v1mr_REML+orig  {$ec}TacH_noall+orig {$ec}TacL_noall+orig )
 adwarp -overwrite -apar  {$ec}anatavgSS_at+tlrc -dpar $dset -dxyz 2 
 end
 end
```

Notes: we create the dataset with 2 mm resolution. The default would be 1 mm (the resolution of the anatomy) but this makes a very large file and is not more accurate because the original fMRI data has 2 - 3 mm resolution.
These datasets must then be copied to the group directory (or they could be created there in the first place).

The final step is to perform the group functional analysis. This is usually done with 3dANOVA. Because the 3dANOVA command line is so long, we often put it in a separate text file and execute it as a script.
e.g.

```
 open -e @3dAv1
 chmod a+x @3dAv1
 ./@3dAv1
```

Here are the contents of @3dAv1

```
 #!/bin/tcsh -f
 3dANOVA2 -overwrite -type 3 -alevels 4 -blevels 8 \
 -dset 1 1 FLv1mr_REML+tlrc'[2]' -dset 2 1 FLv1mr_REML+tlrc'[8]' \
 -dset 3 1 FLv1mr_REML+tlrc'[5]' -dset 4 1 FLv1mr_REML+tlrc'[11]' \
 -dset 1 2 FMv1mr_REML+tlrc'[2]' -dset 2 2 FMv1mr_REML+tlrc'[8]' \
 -dset 3 2 FMv1mr_REML+tlrc'[5]' -dset 4 2 FMv1mr_REML+tlrc'[11]' \
 -dset 1 3 FNv1mr_REML+tlrc'[2]' -dset 2 3 FNv1mr_REML+tlrc'[8]' \
 -dset 3 3 FNv1mr_REML+tlrc'[5]' -dset 4 3 FNv1mr_REML+tlrc'[11]'  \
 -dset 1 4 FQv1mr_REML+tlrc'[2]' -dset 2 4 FQv1mr_REML+tlrc'[8]' \
 -dset 3 4 FQv1mr_REML+tlrc'[14]' -dset 4 4 FQv1mr_REML+tlrc'[20]'  \
 -dset 1 5 FSv1mr_REML+tlrc'[2]' -dset 2 5 FSv1mr_REML+tlrc'[8]' \
 -dset 3 5 FSv1mr_REML+tlrc'[14]' -dset 4 5 FSv1mr_REML+tlrc'[20]'  \
 -dset 1 6 FUv1mr_REML+tlrc'[2]' -dset 2 6 FUv1mr_REML+tlrc'[8]' \
 -dset 3 6 FUv1mr_REML+tlrc'[14]' -dset 4 6 FUv1mr_REML+tlrc'[20]' \
 -dset 1 7 FYv1mr_REML+tlrc'[2]' -dset 2 7 FYv1mr_REML+tlrc'[8]' \
 -dset 3 7 FYv1mr_REML+tlrc'[14]' -dset 4 7 FYv1mr_REML+tlrc'[20]'  \
 -dset 1 8 FZv1mr_REML+tlrc'[2]' -dset 2 8 FZv1mr_REML+tlrc'[8]' \
 -dset 3 8 FZv1mr_REML+tlrc'[14]' -dset 4 8 FZv1mr_REML+tlrc'[20]'  \
 -fa Stimuli -amean 1 Vis -amean 2 Tac -amean 3 VTH -amean 4 TacPas \
 -acontr -1 -1 2 0 VTvsVisTac  -acontr 1 -1 0 0 VisVsTac -acontr 1 1 1 1  AllStim \
 -bucket 3dANOVAv2
```

Notes: you MUST make sure that the sub-BRIKS match from subject to subject. Check with 3dinfo.
blevels are the number of subjects
alevels are the number of stimulus conditions
You can perform ANOVAs on either the beta-weights or the t-statistics. It is probably good to try both.

After creating the average, it can be useful to make a table of active regions. This is best done with the Clusterize function in AFNI.

The 3dclust button within this function will write out a command line which can be copied into the Notes file.
The output can be copied into a text file and then imported into Excel or Word to make a nice table.
Typically we use the peak co-ordinates and t-statistics when reporting activations.
