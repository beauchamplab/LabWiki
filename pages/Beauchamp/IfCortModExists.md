# IfCortModExists

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

## What if I have scanned a subject for whom a surface model already exists?

There are two procedures for this situation. The old method, developed when storage space was expensive, was to have one copy of each subject's surface model (in a /surfaces directory) and to align each new scanning session (and all its constituent data) to that surface. The new method is to create a copy of each subject's surface model in each experiment directory, so there is one surface for each scanning session. This is simpler although it uses more space.

### NEW METHOD

First, use the Experiment Summary Excel spreadsheet to find when the subject was scanned previously and a surface was created. Then, copy the surface directories to the new experiment directory

```
 cp -R /Volumes/data/OLDSUBJ/fs /Volumes/data/NEWSUBJ/
```

If you think you will need the fsaverage directory (not currently used for anything) copy it over as well

```
 cp /Volumes/data/OLDSUBJ/fs* /Volumes/data/NEWSUBJ/
```

Next, we create a version of Surface Anatomy that is registered to the Experiment Anatomy. You must run the script from the directory where Experiment Anatomy resides.

```
 @SUMA_AlignToExperiment -exp_anat anat_final.{$subj}+orig -surf_anat ../fs/SUMA/fs_SurfVol+orig -prefix fs_SurfVol_Alnd_Exp -surf_anat_followers ../fs/SUMA/aparc.a2009s+aseg_rank.nii
```

Finally, copy over the @ec script that automatically loads AFNI + SUMA

```
 cd .. 
 cp /Volumes/data/scripts/@ec .
```

Simply run this script to start AFNI and SUMA

```
 ./@ec
```

It may be desirable to do some additional steps as well (these could be automated):

```
 echo "It makes life easier if the parcellation dataset uses cardinal axes (x=LR, etc.)"
 3daxialize -prefix aparc.a2009s.rank_axialized aparc.a2009s+aseg_rank_Alnd_Exp+orig
 3drefit -labeltable ../fs/SUMA/aparc.a2009s+aseg_rank.niml.lt  aparc.a2009s.rank_axialized+orig
 3drefit -labeltable ../fs/SUMA/aparc.a2009s+aseg_rank.niml.lt  aparc.a2009s+aseg_rank_Alnd_Exp+orig
 cd {$sess}/../fs/SUMA
 mris_convert -c ../surf/lh.sulc ../surf/lh.smoothwm ./lh.sulc.asc
 mris_convert -c ../surf/rh.sulc ../surf/rh.smoothwm ./rh.sulc.asc
```

### OLD METHOD

#### Automation

All of the steps below are contained in the scripts file
/Volumes/data9/surface/scripts/@alreadymade

To run this command type,

```
 /Volumes/data9/surfaces/scripts/@alreadymade current_ec subjname original_surface_ec
```

Where current\_ec is the current two-letter experiment code
subjname is the subject's name in the format lastname\_firstname.
original\_surface\_ec is the two letter experiment code which the surface was originally constructed from
(this must be determined by looking in the surfaces directory).
Note that an anatavg must exist in the afni directory. If it doesn't create with

```
 3dcopy 3DSAG_T1.nii ${ec}anatavg
```

#### Aligning to Experiment

The scripts assumes that all of the steps performed the script file @prep\_dir have been performed (see Preparation for Creating Cortical Surface Models page)
e.g.

```
 /Volumes/data9/surfaces/scripts/@recon BD doe_jane
```

First, check to make sure that the already created surface has the necessary components created by the @finish script

```
 FSread_annot -input ../label/lh.aparc.a2005s.annot -roi_1D ./lh.aparc.a2005s.1D.roi
 FSread_annot -input ../label/rh.aparc.annot -roi_1D ./rh.aparc.1D.roi
 FSread_annot -input ../label/lh.aparc.annot -roi_1D ./lh.aparc.1D.roi
 mris_convert -c ../surf/lh.sulc ../surf/lh.smoothwm ./lh.sulc.asc
 mris_convert -c ../surf/rh.sulc ../surf/rh.smoothwm ./rh.sulc.asc
 set ec = TA203
 SurfSmooth -spec {$ec}_both.spec -surf_A lh.smoothwm.asc -met NN_geom -surf_out lh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
 SurfSmooth -spec {$ec}_both.spec -surf_A rh.smoothwm.asc -met NN_geom -surf_out rh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
 cp /Volumes/data9/surfaces/scripts/both.spec ./both.spec
```

Next, go to the surfaces directory, create a copy of the new anatomy, and align it the new data with the old surface model.

```
 3dcopy  /Volumes/data1/UT/CZ/afni/CZanatr1+orig ./CZanatr1
 @SUMA_AlignToExperiment -exp_anat CZanatr1+orig -surf_anat TA203_SurfVol+orig -prefix CZ_SurfVol_Alnd_Exp 
 mv CZ_SurfVol_Alnd_Exp+orig.* /Volumes/data1/UT/CZ/afni/
```

Next, create an @EC file that points to the appropriate directory:

```
 cat >> @CZ
 /Volumes/data9/surfaces/scripts/@ec  CZ /Volumes/data9/surfaces/TandonLang/TA203/SUMA
```
