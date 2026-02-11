# FreeSurfer

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

<https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki>

Check out the manual located on /Volumes/data9/surfaces/FreeSurferManual6Oct00.pdf for instructions on how to manually segment the white matter.

Surface files can be converted using [AFNI](#)") 's ConvertSurface program or [Caret](#)") 's Import feature.

## Configuring Freesurfer

```
  source /Applications/freesurfer/SetUpFreeSurfer.csh
```

Then set the subject's directory

```
  setenv SUBJECTS_DIR /surfaces/subject_name/
```

## Creating Flat Maps

### Creating Patch

Run tksurfer to define cuts for either the right hemisphere (rh) or left hemisphere (lh):

```
  tksurfer subjID $h inflated
```

The important buttons on the TkSurfer window are shown below:

[![](../../attachments/FreeSurfer/FreeSurferTksurferMenu.jpg)](../../attachments/FreeSurfer/FreeSurferTksurferMenu.jpg)

- Show the curvature ($h.curv) by clicking on File-> Curvature->Load Curvature... It should look like this:

[![](../../attachments/FreeSurfer/FreeSurferInflatedSurf.jpg)](../../attachments/FreeSurfer/FreeSurferInflatedSurf.jpg)

- Left click points on the surface and then click the cut icon (scissors with an open triangle for a line cut). Points can be erased by right clicking on the surface twice.
- Make 1 cut down the calcarine sulcus and 3 equally spaced cuts on the medial wall. In addition, 1 sagitally oriented cut must be made around the temporal pole.
- To rotate to the temporal pole you should first change the angle of rotation.

[![](../../attachments/FreeSurfer/FreeSurferInflatedSurfCuts.jpg)](../../attachments/FreeSurfer/FreeSurferInflatedSurfCuts.jpg)

- A final cut must be made to encircle the midline region. This area includes the corpus callosum and mid-brain structures.
- Make sure the points are clicked in order around the region. Also do not click within the previous cuts (you will end up selecting points on the opposite side of the surface).
- Click the cut closed line icon to create the cut.

[![](../../attachments/FreeSurfer/FScuts.jpg)](../../attachments/FreeSurfer/FScuts.jpg)

- Click outside the midline region and click the Fill Uncut Area button.

[![](../../attachments/FreeSurfer/FSpatch.jpg)](../../attachments/FreeSurfer/FSpatch.jpg)

- Save the patch by clicking File->Patch->Save Patch As. The default names for these files are $h.full.patch.3d

<https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferOccipitalFlattenedPatch>

### Using mris\_flatten

Flat surfaces can be made from patch files using mris\_flatten on Tim's computer:

```
  mris_flatten -w 10 lh.full.patch.3d lh.full.flat.patch.3d
```

Unfolding takes a few of hours and it is advisable to have the -w 10 to check the progress of the program every 10 iterations.

<https://surfer.nmr.mgh.harvard.edu/fswiki/mris_5fflatten>

### Converting to asc Format

Use mris\_convert with the -p option:

```
  mris_convert -p lh.full.flat.patch.3d lh.full.flat.patch.3d.asc
```

The lh.orig file from the surf directory needs to be in the same directory as the 3d file.
