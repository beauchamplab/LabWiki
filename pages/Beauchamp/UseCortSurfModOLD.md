---
title: UseCortSurfModOLD
parent: Beauchamp
---
# UseCortSurfModOLD

## Automation

All of the steps below are contained in the script file
/Volumes/data9/surface/scripts/@finish

To run this command type,

```
 /Volumes/data9/surfaces/scripts/@finish ec subjname
```

Where ec is the two-letter experiment code and subjname is the subject's name in the format lastname\_firstname.
The scripts assumes that an anatomical named ec\_anatavg+orig exists in the current directory.
The script assumes that all of the steps performed the script file @prep\_dir have been performed (see Creating Cortical Surface Models page)

```
 /Volumes/data9/surfaces/scripts/@prep_dir BD doe_jane
```

A common reason for this script to fail is that you do not have permissions for the AFNI or surfaces directory (fix this with chmod).

September 2011: The new version of FreeSurfer makes different parcellation files that cause the script to choke. Until it is fixed, the commands must be run manually. (The "Align to Experiment" step is the first one that doesn't seem to work properly).

## Converting Freesurfer surfaces to SUMA Files

After creating the surface in FreeSurfer, the files must be converted to a format readable by SUMA.
From the surface directory folder (e.g. /data9/surfaces/kingon\_ashley/BI) run the following

```
 @SUMA_Make_Spec_FS -sid $ec
```

This copies an anatomical AFNI dataset and files for the surfaces into a new folder called SUMA.

## Creating Partially Inflated Surfaces

Partially inflated surfaces allow the viewer to see the cortex buried in sulci while preserving the major anatomical landmarks.
SurfSmooth will begin inflate a surface for a given number of iterations. Use the following two lines to create partially inflated surfaces.

```
SurfSmooth -spec {$ec}_lh.spec -surf_A lh.smoothwm.asc -met NN_geom -surf_out lh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
SurfSmooth -spec {$ec}_rh.spec -surf_A rh.smoothwm.asc -met NN_geom -surf_out rh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
```

Note that takes FreeSurfer .asc files as input and writes out Suma .ply files as output. For Suma to load these files correctly, the spec file must be modified to read

```
      SurfaceType = Ply
```

## Making Movies of the Inflation Process

It is easy to make movies to show the inflation process, see
[Beauchamp:InflationMovies](InflationMovies.md "Beauchamp:InflationMovies")

## Creating Modified SPEC files

SPEC files are text files which tells SUMA which surfaces to load. In the previous step, new surfaces were created so these must be added to the SPEC file.
In addition, it is convenient to create a single SPEC file with both left and right hemispheres. The easiest way is to copy a previously made SPEC file

```
 cp /Volumes/data9/surfaces/alwin_sarah/CW/SUMA/CW_both.spec ./{$ec}_both.spec
```

Alternately, a text editor can be used to combine the lh.spec and rh.spec files, and to add the following

```
NewSurface
       SurfaceFormat = ASCII
       SurfaceType = FreeSurfer
       FreeSurferSurface = lh.smoothwm.SS500.asc
       LocalDomainParent = lh.smoothwm.asc
       SurfaceState = SS500
       EmbedDimension = 3
       Anatomical = N
```

```
NewSurface
       SurfaceFormat = ASCII
       SurfaceType = FreeSurfer
       FreeSurferSurface = rh.smoothwm.SS500.asc
       LocalDomainParent = rh.smoothwm.asc
       SurfaceState = SS500
       EmbedDimension = 3
       Anatomical = N
```

## Align subject to experiment

Next, go to the surfaces directory, create a copy of the new anatomy, and align it the new data with the old surface model.

```
 3dcopy  /Volumes/data1/UT/CZ/afni/CZanatr1+orig ./CZanatr1
 @SUMA_AlignToExperiment -exp_anat CZanatr1+orig -surf_anat TA203_SurfVol+orig -prefix CZ_SurfVol_Alnd_Exp 
 mv CZ_SurfVol_Alnd_Exp+orig.* /Volumes/data1/UT/CZ/afni/
```

The purpose of @SUMA\_AlignToExperiment is to align the original anatomy and the modified FreeSurfer version of the anatomy used to make the surface. If this fails, wildly wrong results can occur when attempting to use the surface for analysis and visualization. Therefore, it is critical to load the original and SurfVol\_Alnd\_Exp anatomy in AFNI and make sure that they are aligned.
If they do not match, then the anatomies must re-aligned. A typical problem is that FreeSurfer adds a great deal of empty space around the anatomy and centers it causing the alignment process to fail because the SurfVol and the ExpAnat are too different.
This can be remedied by using the "wd" option

```
 @SUMA_AlignToExperiment -wd
```

Ziad suggests using the @Align\_Centers program to shift the ExpAnat so that it is in register with the SurfVol

```
 @Align_Centers -base SurfVol -dset ExpAnat -child AllFuncDsets
```

By default, this creates new copies of all datasets. Alternately, the "no\_cp" option can be used.

A more elegant solution would be to use this offset as a pre-processing step to @AlignToExperiment, but this would require a great deal of work by Ziad.

Optionally, you can create an @EC file that points to the appropriate directory to automate loading SUMA and AFNI:

```
 cat >> @CZ
 /Volumes/data9/surfaces/scripts/@ec  CZ /Volumes/data9/surfaces/TandonLang/TA203/SUMA
```

## Create an "@" file

Whether the surface existed already or not, because the surface directory is in a different place from the fMRI data, it is a good idea to create a script file that automatically loads both the surface and the functional data.
By convention, this is given the name @EC, where EC is the two-letter experiment code.
e.g. The contents of @CQ read

```
  #! /bin/tcsh -f
  cd afni
  suma -niml  -spec /Volumes/data9/surfaces/kingon_ashley/BI/SUMA/both.spec -sv CQ_SurfVol_Alnd_Exp+orig & 
  afni -niml &
```

A more elegant way calls an already existing script

```
 cat >> @CZ
 /Volumes/data9/surfaces/scripts/@ec  CZ /Volumes/data9/surfaces/TandonLang/TA203/SUMA
 chmod a+x ./@CZ
```

## Converting Sulc (Cortical Surface Curvature) Files for use in SUMA

Use sulc files for background in SUMA instead of the default SUMA background to better show the anatomy.
First, create them with these commands:

```
 mris_convert -c ../surf/lh.sulc ../surf/lh.smoothwm lh.sulc.asc
 mris_convert -c ../surf/rh.sulc ../surf/rh.smoothwm rh.sulc.asc
```

Then, the files can be loaded into SUMA using the Load Dataset button or with the following command line

```
 DriveSuma -com surf_cont -load_dset /Volumes/data1/UT/{$ec}/{$ec}.lh.sulc.asc \
 -I_sb 4 -surf_label lh.smoothwm.asc  -view_surf_cont y -load_cmap ~/nice.1D.cmap -Dim 0.6
```

```
 DriveSuma -com surf_cont -load_dset /Volumes/data1/UT/{$ec}/{$ec}.rh.sulc.asc  \
 -I_sb 4 -surf_label rh.smoothwm.asc -view_surf_cont y -switch_cmap nice.1D -Dim 0.6
```

```
 DriveSuma -com viewer_cont -key b
```

This will show global depth, instead of local curvature (the default), as the SUMA anatomical background.

## Importing Cortical Parcellation Data from FreeSurfer

FreeSurfer automatically determines ROIs based on two of its atlas brains. The following lines can be run to create 1D roi’s that can be overlayed on the surface in SUMA.

```
FSread_annot -input ../label/rh.aparc.a2005s.annot -col_1D rh.aparc.a2005s.1D.col -roi_1D rh.aparc.a2005s.1D.roi
FSread_annot -input ../label/lh.aparc.a2005s.annot -col_1D lh.aparc.a2005s.1D.col -roi_1D lh.aparc.a2005s.1D.roi
FSread_annot -input ../label/rh.aparc.annot -col_1D rh.aparc.1D.col -roi_1D rh.aparc.1D.roi
FSread_annot -input ../label/lh.aparc.annot -col_1D lh.aparc.1D.col -roi_1D lh.aparc.1D.roi
```

Usually we only use the ROI files, so this can be simplified to

```
FSread_annot -input ../label/rh.aparc.a2005s.annot -roi_1D rh.aparc.a2005s.1D.roi
FSread_annot -input ../label/lh.aparc.a2005s.annot  -roi_1D lh.aparc.a2005s.1D.roi
```

To find out which number corresponds to which anatomical structure, we use the command

```
 FSread_annot -show_FScmap -input ../label/rh.aparc.a2005s.annot
```

The output of this is here
[FreeSurferParcellation](../FreeSurferParcellation.md "FreeSurferParcellation")

There is also a spread sheet showing the numbering scheme relative to the actual ROI name.
This can be found on /Volumes/data9/surfaces/FS\_aparc.xls

## Viewing FreeSurfer Parcellation Data in SUMA

The 1D files produced in the previous step can be loaded into SUMA.
To do this manually, right click on the hemisphere of interest and open the surface viewer for that hemisphere. Then click "Load Dataset" and enter the parcellation file for that hemisphere. The parcellation file is different for each hemisphere, so separate surface controllers must be opened for left and right hemispheres and the correct parcellation files loaded into each one. In the Dset mapping part of the surface controller window, select sub-BRIK #1 for the Intensity (color scale). This display the second column of the parcellation file (since AFNI starts counting at 0) which contains the parcellation information. Otherwise you will simply display the first column of the parcellation file, which is the node number and is not informative. The color scale and threshold can be adjusted in SUMA in order to make a pretty picture. Select the ROI128 or ROI256 colormaps to give each parcellated region a different color. The FreeSurfer colormap may also give good results.

These steps can be automated using the DriveSuma program; for instance

```
 DriveSuma -com surf_cont -load_dset /Volumes/data9/surfaces/jagar_ashley/AZ/SUMA/AZrh.aparc.a2005s.1D.dset \
  -I_sb 1 -surf_label rh.smoothwm.asc  -view_surf_cont y
```

Right clicking on a node will move the SUMA crosshairs to that node. The surface controller window will then tell you the Value at that node (next to "Val", under "Intens") which can be compared with the parcellation file (above) to learn the identity of that node.

For finer control, the 1deval program can be used (in combination with the spreadsheet above) to create a dataset file that will display only certain ROIs. For instance, spreadsheet says that STS is ROI #80.

```
 1deval -index AZrh.aparc.a2005s.1D.dset'[0]' -b AZrh.aparc.a2005s.1D.dset'[1]' \
 -expr "equals(b,80)" > AZrh.aparc.a2005s.onlySTS.1D.dset
```

Produces a new dataset where only STS nodes have a non-zero value.

## Converting Surface Parcellation Data for use in AFNI

Use the Surf2Vol command to take the parcellation data and put it in the volume. Then it can be used, for instance, to calculate average time series.
Note that the output has 4 sub-BRIKS (values) for each voxel. Only the 0th sub-BRIK contains the parcellation information; also these values are floats (which they do not need to be) so we convert them to shorts.
Also see the next step for an alternative way of doing this.

```
 3dSurf2Vol -spec {$d}/both.spec -surf_A {$d}/rh.smoothwm.asc -surf_B {$d}/rh.pial -sv {$ec}_SurfVol_Alnd_Exp+orig. -grid_parent {$ec}EPIanatAlbl+orig\
-sdata_1D {$d}/rh.aparc.a2005s.1D.roi -map_func max -f_steps 15 -prefix {$ec}_rh_all_Surf2Vol_ROI
 3dSurf2Vol -spec {$d}/both.spec -surf_A {$d}/lh.smoothwm.asc -surf_B {$d}/lh.pial -sv {$ec}_SurfVol_Alnd_Exp+orig. -grid_parent {$ec}EPIanatAlbl+orig\
-sdata_1D {$d}/lh.aparc.a2005s.1D.roi -map_func max -f_steps 15 -prefix {$ec}_lh_all_Surf2Vol_ROI
 3dcalc -datum short -prefix {$ec}_aparc -a0 {$ec}_rh_all_Surf2Vol_ROI+orig -b0 {$ec}_lh_all_Surf2Vol_ROI+orig -expr "max(a,b)"
```

## Converting Volume Parcellation Data for use in AFNI

FreeSurfer itself creates a volume dataset that contains parcellation information. Therefore, instead of the previous step, it is also possible to use the existing volume parcellation information. This is what is done by the @finish script.

```
 @SUMA_AlignToExperiment -exp_anat {$ec}anatavg+orig -surf_anat {$ec}_SurfVol+orig -prefix {$ec}_SurfVol_Alnd_Exp \
```

-surf\_anat\_followers brainmask.auto.nii aseg.auto.nii aseg.nii aparc.a2005s+aseg.nii aparc+aseg.nii

After @SUMA\_AlignToExperiment aligns the SurfVol to the experiment anatomy, it applies the same transformation to the FreeSurfer parcellation BRIKs. Therefore, they should be in perfect alignment with the experiment anatomy. Because the FreeSurfer parcellation BRIKs have the same name for each subject, @finish renames them as follows for clarity:

```
 3drename aparc.a2005s+aseg.nii_Alnd_Exp+orig {$ec}_FS_aparc.a2005s_Alnd_Exp
 3drename aparc+aseg.nii_Alnd_Exp+orig {$ec}_FS_aparc_Alnd_Exp
 3drename brainmask.auto.nii_Alnd_Exp+orig.HEAD {$ec}_FS_brainmask.auto.nii_Alnd_Exp
 3drename aseg.nii_Alnd_Exp+orig.HEAD {$ec}_FS_aseg.nii_Alnd_Exp
 3drename aseg.auto.nii_Alnd_Exp+orig.HEAD {$ec}_FS_aseg.auto.nii_Alnd_Exp
```

Finally, @finish copies the files to the experiment directory

```
 foreach ds (*Alnd_Exp*HEAD)
 set ds2 = `echo $ds | cut -d "+" -f 1 -`
 echo copying FreeSurfer file {$ds2} to experiment directory
 3dcopy {$ds2}+orig {$p}/{$ds2}
 end
```

The way that @SUMA\_AlignToExperiment aligns the files can be seen in the @Align\_Centers script:

```
 @Align_Centers -base  EB_SurfVol+orig -dset aparc.a2005s.nii -no_cp
```

## Using Volume Parcellation Data in AFNI

The numbering scheme for the volume parcellation BRIK is slightly different than the surface ROIs decribed above.
In the file

```
 DY_FS_aparc.a2005s_Alnd_Exp+orig
```

Voxels in the right STS have value 2180
Voxels in the left STS have value 1180

## Using FreeSurfer Volume Parcellation as Masks in AFNI and DTI Query

The FreeSurfer parcellations will have the same voxel dimensions as the surface volume. To use them as masks for DTI or fMRI analysis, they must be converted to the same resolution as the DTI or fMRI data. This is done above with the 3dSurf2Vol command, but it can also be done with 3dWarp.
Tim has written a script to do this automatically, in

```
 /Volumes/data9/surfaces/scripts/@prep_aseg4afni
```

## Resampling Parcellation

Because EPI data is lower resolution than atlases, resampling must be used. It take much less space and is faster to resample the atlas to the lower resolution than the other way around.
If you will be doing the analysis in +tlrc space this is one way to do it:

```
 @auto_tlrc -base TT_N27+tlrc -no_ss -input {$ec}anatavgSS+orig.HEAD
 adwarp -apar {$ec}anatavgSS_at+tlrc -dpar  {$ec}anatavg+orig 
 3dfractionize -template {$ec}EPIanat+orig -input /Applications/AFNI/TT_N27_CA_EZ_MPM+tlrc -warp {$ec}anatavgSS_at+tlrc -vote -prefix {$ec}_CA_MPM
 3dROIstats -quiet -mask '3dcalc(-a AT_CA_MPM+orig -expr equals(a,105) )' ATv1decirfpcnt+orig
```

Another way to do it is like this:

```
 3dresample -master stats.MS+orig -prefix parc.a2009s_resample -inset aparc.a2009s+aseg_rank_Alnd_Exp+orig  -rmode NN
```

or create a mask first:

```
 3dcalc -prefix STSparc_v1 -a aparc.a2009s+aseg_rank_Alnd_Exp+orig -expr "1*step( equals(a,117) + equals(a,78) + equals(a,82)) + 2 * step(equals(a,191)+equals(a,152)+equals(a,156))"
```

and then resample it:

```
 3dresample -master stats.MS+orig -prefix STSparc_v1_resample -inset STSparc_v1+orig  -rmode NN
```
