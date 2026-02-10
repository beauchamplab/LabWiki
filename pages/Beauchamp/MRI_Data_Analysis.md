# MRI Data Analysis

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## MRI

1. [Motion and Distortion Correction](MotionCorrection.md "Beauchamp:MotionCorrection")
2. [Autism Data](Autism.md "Beauchamp:Autism")
3. [Group analysis with Matlab ANOVAN](anovan.md)

## Notes on creating regressor files in Excel

Regressor files can be created in Excel. Each regressor should be a separate column of numbers, with the number of rows equal to the number of time points in the 3d+time dataset. The columns must be exported using the correct sequence of steps so that they are usable in AFNI. First, create a new workbook. Copy the desired column or columns of numbers to the new workbook. Then, File/Save as a Windows Formatted Text file (.txt). Check the resulting text file using cat, 3dtranspose or 1dplot.

## Analyzing Stability Data

Every week, the scanner technologist scans a phantom using the same pulse sequence that we use to collect fMRI data from volunteers.
By analyzing the phantom data and plotting it over time, we can make sure that nothing is wrong with the scanner.
Vips put the stability data in a folder called "stability"; e.g.

```
 /Volumes/data2/raw/2008_data/stability_2008/stability_010308
```

The first step in analyzing this data is to create an AFNI BRIK from the raw DICOM images. (If they have been saved at the scanner to a Nifti .nii format this step is unnecessary).
The AFNI program to do this is called to3d.
After a BRIK file is created, 3dTstat can be used to find the coefficient of variation of every voxel.

```
 3dTstat -cvarNOD -prefix junk  ppm_fMRI_SSh_SENSE_7_1.nii
```

We use no detrending because we want to measure ALL variance.
Next we need to make a mask of all of the voxels in the phantom.
The simplest to do this is with the 3dcalc command: (The command line version for testing is ccalc).
First, calculate the mean with 3dTstat.

```
 3dcalc -a mean+orig -prefix junkmask -expr "step(a-794.2)"
```

Another way to do this would be an AFNI program like 3dAutomask.
The final step is to calculate the average CV across all voxels in the mask.
One program that can do that is 3dROIstats

```
 3dROIstats  -mask_f2short -mask junkmask+orig junk+orig
```

outputs

```
 File    Sub-brick       Mean_1  
 junk+orig       0[Coef Var(]    0.002460
```

## MVPA

We can use the program 3dsvm to classify stimuli given activation patterns.
To perform MVPA analysis on rapid event related designs, it is necessary to first extract estimates of the response to each stimulus.
This can be done by selecting the MR data point at the peak of the HRF e.g. 2 or 3 time points after stim onset.
Alternately, it may be possible to use 3dDeconvolve with the -stim\_times\_IM option.
e.g.
@3dAXtest1

This fails, tar up the input files and send to Bob.

## Creating Average Time Series

There are three basic steps:

1) Create a mask file

2) Using an AND operation, combine the activation map with the mask file to select only active voxels within the mask

3) Apply the final mask to the deconvolved impulse response function to create time series for each ROI in a subject

4) Move the time series into Excel (or Matlab) to calculate mean and statistics across subjects

In more detail:
1) Create a mask file
This can be done in an automated way using pre-defined anatomical ROIs, such as the Zilles Anatomy Toolbox atlas that is included with AFNI or the FreeSurfer parcellation included with SUMA.
Manual mask creation can be done with 3dclust (or 3dmerge -1clust\_order) to find clusters of active voxels.
Or, ROIs can be manually drawn using the Draw Dataset plug-in in AFNI or the Draw ROI tool in SUMA.

To use the drawing tool in SUMA, select Tools, Draw ROI.
Click on the Right Mouse Button to draw an outline.
When done, click the Join button. The outline will change color.
Click the right mouse button in the middle of the ROI to fill it in. The inside of the ROI should change color. Click the Undo button if something goes wrong. If something goes really wrong, just quit the window or SUMA and try again.
Once you are happy with the ROI, click Finish. The outline should get thinner.

Draw another ROI and hit Join to close. Then change the number in the Value window, perhaps to the next highest number (e.g. from 1 to 2, from 2 to 3) to differentiate the new ROI from the old ROI. (The label value is optional but it may be useful in switching between ROIs).

When finished drawing All ROIs and you wish to save them, change the "THIS" button to "ALL" to save ALL ROIs.
Use the appropriate format (1D or NIML).

The ROIs should be drawn separately for each hemisphere, and then converted to the volume:

3dSurf2Vol -spec /Volumes/data9/surfaces/barker\_kathryn/AX/SUMA/both.spec -surf\_A rh.smoothwm.asc -grid\_parent AXv6dec+orig -sv AX\_SurfVol\_Alnd\_Exp+orig -map\_func max -prefix S1lhROIv5 -sdata\_1D S1ROIRH.1D.roi

3dSurf2Vol -spec /Volumes/data9/surfaces/barker\_kathryn/AX/SUMA/both.spec -surf\_A lh.smoothwm.asc -grid\_parent AXv6dec+orig -sv AX\_SurfVol\_Alnd\_Exp+orig -map\_func max -prefix S1lhROIv6 -sdata\_1D S1LH.1D.roi

These volumes are usually combined with the functional dataset so that only active voxels within the drawn ROI are considered.

3dcalc -prefix AXS1 -a S1lhROIv5+orig -b S1lhROIv6+orig -c82 AXv6dec+orig -d109 AXv6dec+orig \
-expr "step(a+b)\*step(c-8.4)\*(1\*step(d-2) + 2\*step(-2-d))"

This dataset can then be used to create average timeseries.

Manual mask

[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]==MEG and MRI==
Download and install MNE
Go to <http://www.nmr.mgh.harvard.edu/martinos/userinfo/data/MNE_register/index.php>
and register. After registering you will be emailed a login password. The webpage makes it
seem that an email is sent immediately, but in my experience it took over an hour. After you
receive your password login and download the software, also available is the manual and installation
instructions. Following steps C.1 - C.2.3 should do it, unless your computer doesn't already have fink
on it, in which case follow the instructions available on the internal wiki to install fink. One step you'll
have to change, C.1.2 instructs you to type "tar zxvf <filename>", however they seem to longer be
using gzip format files, so instead change that to "tar -xvf <filename>".

Run MNE GUI (mne\_analyze)

Save a label file
format for label file is like this

```
 # Label from mne_analyze
 2358
 16 -39.8716 -10.9534 17.9286 0
 62 -40.1451 7.47006 5.60055 0
 etc.
```

Try to create a similar label file in SUMA

two ways:
1) Manually drawing an ROI (ctrl-d in SUMA)

2) 3dVol2Surf

Both MNE and AFNI analysis will need to use the EXACT SAME surface because otherwise the node numbering will be different and the ROIs will not correspond.

Here is a possible way to do this, according to Ziad Saad.

Manually drew an ROI in SUMA, wrote it out to test.1D.roi

```
 ROI2dataset -prefix test2 -of 1D -input test.1D.roi
```

This creates a SPARSE dataset where there are only values for some nodes.
To create a FULL dataset more similar to a FreeSurfer label file, we must first determine how many nodes are in the original surface
e.g.

```
 more lh.pial.asc
```

133265 266526

Then, we use the command

```
 ROI2dataset -prefix test3 -pad_to_node 133264 -input test.1D.roi
```

This creates a file with one column, zeros for most nodes and a value for the nodes that were drawn on.

However, a label file is in this format:

1. !ascii label , from subject

124029
0 -8.057 -103.564 3.861 0.000000
1 -8.412 -103.675 3.858 0.000000

1) Create an ROI containing all nodes
using 3dVol2Surf -oob or -oob
OR draw an ROI, use ROI2dataset to convert to a file with all nodes

2) cat or 1dcat this file with the original surface file (containing the x,y,z co-ordinates of the nodes)

3) Use convertdset to select only those nodes with a value at the nodes

May also have to use SurfToSurf to convert from the fMRI surface (where the label file was created on) to the MEG surface (created separately so it has a different number of nodes).

SurfToSurf -i MEGSurface.asc -i fMRISurface.asc -output\_params Data -data LeftMT.ROI.1D

**Interpolate ROI file onto another surface file and save as a freesurfer label file**

1) Copy the .roi file along with the suface of the hemisphere for that subject into your working folder.

-The original surface file should use the following naming convention: *[hemishpere].inflated-MRI.asc*

ex: **lh.inflated-MRI.asc**

*NOTE: See [Beauchamp:FreeSurfer](FreeSurfer.md) about converting a surface file to a .asc file*

2) Make sure that new surface file for that hemisphere also exists in that folder in the proper freesurfer format (lh.inflated.asc)

3) Set your environment by defining the following 3 variables in the command line where hem is either lh or rh, area is the area of interest, and roi is the name of the .roi file:

```
setenv hem lh
setenv area mt
setenv roi Left_MT.1D.roi
```

4) Run the following commands from a command line in the proper working directory:

```
SurfToSurf -i $hem.inflated-MRI.asc -i $hem.inflated.asc  -prefix $area -node_indices "$roi"'[0]' -output_params NearestNode
1dcat $area.1D'[1]' $area.1D'[1]' $area.1D'[1]' $area.1D'[1]' $area.1D'[1]' > $area-$hem
wc $area-$hem > temp_node
echo "#! " $area > temp_1
echo `1dcat temp_node'[0]'` > temp_2
cat  temp_1 temp_2 $area-$hem > $area-$hem.label
rm -f temp_node
rm -f temp_1
rm -f temp_2
rm -f $area.1D
rm -f $area-$hem
```

or you can also save the above commands as a file with *#!/bin/csh* at the very top of the file (save as "batch") and call all of the commands using a single command: *csh batch*
