# UseCortSurfMod

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

## Finishing the Surface Model

The @finish script assumes that the cortical surface model has already been constructed, see
[Creating Cortical Surface Models](CreateCortSurfMod.md "Beauchamp:CreateCortSurfMod")

To finish the surface model, first change to the AFNI directory, e.g.

```
 cd /Volumes/data1/UT/DB/afni
```

And then run the @finish script. The name of the anatomy which the surface will be registered to (probably the same anatomy used in the @prep\_dir script).

```
 /Volumes/data1/scripts/@finish DBanatavg+orig
```

The anatomyfile will be registered to the surface in the fs/SUMA directory.
A common reason for this script to fail is that you do not have permissions for the AFNI or surfaces directory (fix this with chmod).

## Automation

The first three steps below are contained in the script file /Volumes/data/scripts/@finish. The other steps are mainly obsolete but are included here for educational value.

## Converting Freesurfer surfaces to SUMA Files

After creating the surface in FreeSurfer, the files must be converted to a format readable by SUMA.
From the surface directory folder (e.g. /Volumes/data/UT/NA/fs) run the following

```
 @SUMA_Make_Spec_FS -GIFTI -sid fs
```

This copies files for the surfaces into a new folder called SUMA and converts them into AFNI/SUMA format.
If a SUMA directory already exists, it is safest to delete the SUMA folder and other associated files before running this command and the others below, i.e.

```
  rm -rf SUMA
 @SUMA_Make_Spec_FS -GIFTI -sid fs
 cd ../afni
 rm *Alnd* *aparc*
 rm NAanatavg_shft.1D
 @SUMA_AlignToExperiment -align_centers  -exp_anat NAanatavg+orig -surf_anat ../fs/SUMA/fs_SurfVol.nii -prefix fs_SurfVol_Alnd_Exp
```

## Align subject to experiment

This command aligns the Surface Volume with the Experiment Anatomy, so that the surface and the functional data are in register. The "followers" option applies the same transformation to other datasets, such as anatomical parcellation. For instance,

```
 @SUMA_AlignToExperiment -align_centers  -exp_anat $1 -surf_anat ../fs/SUMA/fs_SurfVol+orig -prefix fs_SurfVol_Alnd_Exp -surf_anat_followers ../fs/SUMA/aparc.a2009s+aseg_rank.nii
```

If @SUMA\_AlignToExperiment has already been run, 3dAllineate can be used to apply the same transformation (equivalent to surf\_anat\_followers) with the 1D file written out by @SUMA, called something like

```
 IE_SurfVol_Alnd_Exp.A2E.1D
```

like this:

```
 3dAllineate -master IEanatavg+orig -1Dmatrix_apply IE_SurfVol_Alnd_Exp.A2E.1D -input aparc.a2009s+aseg_rank.nii -prefix ./aparc.a2009s+aseg_rank_Alnd_Exp -final NN
```

It may also be necessary to manually do a few other steps that are in the new @finish script:

```
 3drefit -labeltable ./aparc.a2009s+aseg_rank.niml.lt  aparc.a2009s.rank_axialized+orig
 3drefit -labeltable ./aparc.a2009s+aseg_rank.niml.lt  aparc.a2009s+aseg_rank_Alnd_Exp+orig
```

The @finish script makes an @ec script file that points to the appropriate directory to automate loading SUMA and AFNI:

OBSOLETE (Ziad has fixed this)
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

## Create an "@" file

A handy script is useful to automatically load AFNI and SUMA. This command puts one in the current directory and can be started by typing @ec

```
 cp /Volumes/data/scripts/@ec ./
```

## FreeSurfer Parcellation Data

The @finish script automatically creates an AFNI BRIK with the FreeSurfer 2009 parcellation data,

```
 aparc.a2009s+aseg_rank.nii
```

The color scale automatically changes if this BRIK is chosen as an overlay. The anatomical region under the crosshairs is shown in the bottom right of the AFNI window. To see the correspondence between labels and numbers, type

```
 cat ../fs/SUMA/aparc.a2009s+aseg_rank.niml.lt
```

## OBSOLETE: Creating Partially Inflated Surfaces

@SUMA\_Make\_Spec\_FS now automatically creates partially inflated surfaces so everything in this step is no longer needed.
Partially inflated surfaces are good because they allow the viewer to see the cortex buried in sulci while preserving the major anatomical landmarks.
SurfSmooth will begin inflate a surface for a given number of iterations. Use the following two lines to create partially inflated surfaces.

```
SurfSmooth -spec {$ec}_lh.spec -surf_A lh.smoothwm.asc -met NN_geom -surf_out lh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
SurfSmooth -spec {$ec}_rh.spec -surf_A rh.smoothwm.asc -met NN_geom -surf_out rh.smoothwm.SS500.ply -Niter 500 -match_area 0.01
```

These commands take FreeSurfer .asc files as input and writes out Suma .ply files as output. For Suma to load these files correctly, the spec file must be modified to read SurfaceType = Ply. If you are curious, It is easy to make movies to show the inflation process, see
[Beauchamp:InflationMovies](InflationMovies.md).

If new surfaces are created, they must be added to the .spec files so that they are loaded when SUMA is as
SPEC files are text files which tells SUMA which surfaces to load. In the previous step, new surfaces were created so these must be added to the SPEC file.
It is convenient to create a single SPEC file with both left and right hemispheres. The easiest way is to copy a previously made SPEC file or a text editor can be used to combine the lh.spec and rh.spec files, and to add the following

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

## OBSOLETE: Converting Sulc (Cortical Surface Curvature) Files for use in SUMA

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

FreeSurfer automatically determines ROIs based on two of its atlas brains. The following lines can be run to create 1D roi’s that can be overlayed on the surface in SUMA. This will look nicer than viewing the parcellation data on the surface after it has been converted to the volume.

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
[FreeSurferParcellation](../FreeSurferParcellation.md)

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

Because EPI data is lower resolution than atlases, resampling must be used. It is easier to resample the atlas to the lower resolution than the other way around.
In this example, we take the parcellation into +tlrc space to allow automatic selection of parts of the atlas regions (e.g. posterior to y = -20 in +tlrc space).

```
 @auto_tlrc -base TT_N27+tlrc -no_ss -input {$ec}anatavgSS+orig.HEAD
 adwarp -apar {$ec}anatavgSS_at+tlrc -dpar  {$ec}anatavg+orig 
 3dfractionize -template {$ec}EPIanat+orig -input /Applications/AFNI/TT_N27_CA_EZ_MPM+tlrc -warp {$ec}anatavgSS_at+tlrc -vote -prefix {$ec}_CA_MPM
 3dROIstats -quiet -mask '3dcalc(-a AT_CA_MPM+orig -expr equals(a,105) )' ATv1decirfpcnt+orig
```

Alternatively, we can use 3dresample. For example, if we create a mask from the parcellation atlas, we can resample it to the lower EPI resolution as follows:

```
 3dresample -master stats.MX+orig -prefix STSparc_resample -inset STSparc+orig  -rmode NN
```
