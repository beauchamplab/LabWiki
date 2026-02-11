# PrepCortSurfModels

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

## First step: creating an Anatomical BRIK

Surfaces are created from an anatomical (T1) MRI dataset.
Surface creation works best if two or more T1 datasets are acquired and averaged. Averaging can be done in AFNI (easier) or in FreeSurfer. To average anatomies using AFNI, use the following commands. Motion correction is applied before averaging in case the subject moved between anatomies. The base anatomy (that other anatomies are aligned to) should be the anatomy that the EPIs are best aligned with (usually the T1 collected closest in time to the EPIs).

```
3dAllineate -base 3DSAG_T1_2.nii -source 3DSAG_T1_1.nii -prefix ${ec}anatr1_1RegTo2 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
3dmerge -gnzmean -nscale -prefix ${ec}anatavg 3DSAG_T1_2.nii  ${ec}anatr1_1RegTo2+orig
```

or

```
 3dAllineate -base {$ec}anatr2+orig -source {$ec}anatr2+orig -prefix ${ec}anatr1_1RegTo2 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
 3dmerge -gnzmean -nscale -prefix ${ec}anatavg  {$ec}anatr2+orig  ${ec}anatr1_1RegTo2+orig
```

If there are three anatomies, extend as follows:

```
 3dAllineate -base {$ec}anatr1+orig -source {$ec}anatr2+orig -prefix ${ec}anatr2_2RegTo1 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
 3dAllineate -base {$ec}anatr1+orig -source {$ec}anatr3+orig -prefix ${ec}anatr3_3RegTo1 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr3toanatr1
 3dmerge -gnzmean -nscale -prefix ${ec}anatavg  {$ec}anatr1+orig  ${ec}anatr2_2RegTo1+orig ${ec}anatr3_3RegTo1+orig
```

## Second step: FreeSurfer preparation

Run the script file

```
 /Volumes/data/scripts/@prep_dir anat_name
```

**NB: To access this script (or anything else on data1) then data1 must be mounted on your Mac.** To run this command first change into the directory where the subject's data is stored.
e.g.

```
 cd /Volumes/data/UT/DB/afni
```

Then, type the command. e.g.

```
 /Volumes/data/scripts/@prep_dir DBanatavg+orig.BRIK
```

if you have an average anatomy or

```
/Volumes/data/scripts/@prep_dir DBanatr1+orig.BRIK
```

or

```
/Volumes/data/scripts/@prep_dir 3dsag_t1.nii
```

if you do not. Be sure to include the full file name including the .BRIK or .nii suffix. Ignore warnings issued by Freesurfer about using only one anatomical scan or incorrect group permissions.

## Next: Create the surface

[Creating Cortical Surface Models](CreateCortSurfMod.md "Beauchamp:CreateCortSurfMod")

## Location of the created surface

Creating a cortical surface model requires a lot of disk space (~1-2 GB per subject). Because disk space was historically limited, cortical surface models were created on a different disk than the fMRI data. e.g.

```
 /Volumes/data9/surfaces
```

for the surface and

```
/Volumes/data1/subjID/afni
```

for the fMRI data.
Because disk space is now inexpensive, in 2011 this practice was discontinued and now the cortical surface model is stored with the fMRI data is the "fs" (for freesurfer) directory:

```
/Volumes/data1/subjID/fs
```

e.g.

```
/Volumes/data1/DB/fs
```

For web pages describing the previous method, please see

1. [OLD version of Preparation for Creating Cortical Surface Models](PrepCortSurfModelsOLD.md)
2. [OLD version of Creating Cortical Surface Models](CreateCortSurfModOLD.md)
3. [OLD version of finishing and using Cortical Surface Models](UseCortSurfModOLD.md)

## Details of the commands

The @recon script performs the following steps automatically; they are included here for educational purposes but do not need to be performed.

## Creating FreeSurfer Directory Structures for Individual Subjects

FreeSurfer requires a specific directory structure for each subject. In addition FreeSurfer requires that subjects’ directories be listed in the $SUBJECTS\_DIR. Since this is an environment variable, it can be set at anytime:

```
set SUBJECTS_DIR = /surfaces/subject_name/
```

The program mksubjdirs constructs the directory structure automatically.

```
cd $SUBJECTS_DIR
mksubjdirs subjID
```

## Importing AFNI Files into FreeSurfer

The mri\_convert program is used to convert the BRIK/HEAD files into the mgz format (gzipped MGH file),:

```
mri_convert $SUBJECTS_DIR/afni/subjIDanatr+orig.BRIK $SUBJECTS_DIR/subjID/mri/001.mgz
```

This should be repeated for every anatomical scan with the number scheme 001.mgz, 002.mgz, 003.mgz, etc.

or

```
 mri_convert afni/CAavganat+orig.BRIK CA/mri/001.mgz
```

if the averaging is done in AFNI (recommended method). Ignore warnings issued by Freesurfer about using only one anatomical scan
