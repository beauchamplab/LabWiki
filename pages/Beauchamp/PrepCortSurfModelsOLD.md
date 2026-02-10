# PrepCortSurfModelsOLD

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

## Creating an Anatomical BRIK

Surfaces are created from an anatomical (T1) MRI dataset.
Surface creation works best if two or more T1 datasets are acquired and averaged.
This can be accomplished with the following commands. Motion correction is applied before averaging in case the subject moved between anatomies.

```
3dAllineate -base 3DSAG_T1_2.nii -source 3DSAG_T1_1.nii -prefix ${ec}anatr1_1RegTo2 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
3dmerge -gnzmean -nscale -prefix ${ec}anatavg 3DSAG_T1_2.nii  ${ec}anatr1_1RegTo2+orig
```

or

```
 3dAllineate -base {$ec}anatr2+orig -source {$ec}anatr2+orig -prefix ${ec}anatr1_1RegTo2 -verb -warp shift_rotate -cost mi -automask -1Dfile ${ec}anatr2toanatr1
 3dmerge -gnzmean -nscale -prefix ${ec}anatavg  {$ec}anatr2+orig  ${ec}anatr1_1RegTo2+orig
```

If only a single T1 was acquired, then an average dataset can be faked with the command

```
 3dcopy 3DSAG_T1.nii ${ec}anatavg
```

The instructions below assume that a dataset named ECanatavg+orig has already been created.

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

## Automation

All of the steps below are contained in the scripts file

```
 /Volumes/data9/surface/scripts/@prep_dir
```

**NB: To access this script (or anything else on data9) then data9 must be mounted on your Mac.**
To run this command first change into the directory where a subject's anatomy (in AFNI format) is stored in a file name ECanatavg.
e.g.

```
 cd /Volumes/data1/UT/DB/afni
```

Then, type
 **/Volumes/data9/surfaces/scripts/@prep\_dir ec subjname**
Where ec is the two-letter experiment code and subjname is the subject's name in the format lastname\_firstname.
The scripts assumes that an anatomical named ECanatavg+orig exists in the current directory.
e.g.

```
 /Volumes/data9/surfaces/scripts/@prep_dir $ec $subj
```

```
 /Volumes/data9/surfaces/scripts/@prep_dir DB doe_jane
```

This will create surfaces in the directory doe\_jane

## Initial setup in /surfaces

Make subject directory in /Volumes/data9/surfaces

mkdir lastname\_firstname

cd into directory

mkdir afni

copy high resolution scans into afni directory

ie.

3dcopy /Volumes/data1/UT/CG/afni/CGanatr1+orig ./CGanatr1

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

if the averaging is done in AFNI (recommended method).

Ignore warnings issued by Freesurfer about using only one anatomical scan
