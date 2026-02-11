---
layout: default
title: "FSStndSurf"
parent: Beauchamp
---
# FSStndSurf


## These steps are no longer required and may not be useful

for current instructions, please see

1. [Creating Surface Averages of Functional Data](SurfaceAveraging.md "Beauchamp:SurfaceAveraging")

## Creating and Using Standard FreeSurfer Brains

When surfaces are created in FreeSurfer, the spherical version of the subject's surface is automatically aligned to the FreeSurface standard atlas brain. A new surface is created with
the name lh.sphere.reg . This has the same number of nodes as the surface lh.sphere (and all of the other lh surfaces) but the nodes have been moved (morphed) to new positions so that each node on the subject's brain corresponds to a similar location on the atlas brain. If you view the .reg brain in SUMA, you will see swirling patterns that are a signature of the morphing process.
These registered brains can be used to average fMRI data or other surfaces values across subjects, because each node corresponds to a similar brain location.
Here is the README file from the FreeSurfer group average template.
[Beauchamp:FSAverageReadme](FSAverageReadme.md)
The data files for the FreeSurfer template is found in

```
 /Applications/freesurfer/subjects/fsaverage/surf
```

or equivalent depending on your installation directory. A copy has been created in

```
 /Volumes/data9/surfaces/fsaverage
```

And converted to SUMA format for ease of access.

```
cd /Volumes/data9/surfaces/fsaverage
./@fs
```

1. Functional activation must be mapped to the surface.

This is accomplished using the 3dVol2Surf command.
set sd = /Volumes/data9/surfaces/couch\_david/FM/SUMA/
set sb = 2
set sblabel = VisLoc

```
3dVol2Surf -overwrite -spec {$sd}/{$ec}_{$hemi}.spec -surf_A smoothwm  -sv {$ec}_SurfVol_Alnd_Exp+orig -oob_value 0 \
-grid_parent {$ec}v1mr+orig'['{$sb}']' -map_func mask   -out_1D {$ec}v1mr_{$hemi}_{$sblabel}.1D
```

This assigns a functional value to each node. See
[Beauchamp:CreateStndSurfModNew](CreateStndSurfModNew.md "Beauchamp:CreateStndSurfModNew") for more details on different mapping options in 3dVol2Surf.
The created .1D file has multiple columns; the data is in column 6.

1. Map the individual subject surface to the atlas surface.

The functional values on the registered sphere must now be mapped to the nodes on the atlas sphere, which has the same spatial orientation but a different number of nodes.

```
 SurfToSurf -prefix test -output_params Data -data  {$ec}v1mr_{$hemi}_{$sblabel}.1D'[6]'  \
-i /Volumes/data9/surfaces/fsaverage/SUMA/{$hemi}.sphere.reg.asc  -i {$sd}/{$hemi}.sphere.reg.asc
```

The created .1D file has multiple columns; the data is in column 7. It can be viewed on the fsaverage brain"

```
  cp FNv1mr_lh_VisLoc_reg.1D /Volumes/data9/surfaces/fsaverage/SUMA
 cd /Volumes/data9/surfaces/fsaverage
./@fs
```

Click on load dataset to view. Below are some pictures of the original activity from three subjects and the same activation on the fsaverage brain. Cases FL, FM, FN

[![](../../attachments/FSStndSurf/Beauchamp_FL_VisLoc.jpg)](../../attachments/FSStndSurf/Beauchamp_FL_VisLoc.jpg)[![](../../attachments/FSStndSurf/Beauchamp_FL_VisLoc_reg.jpg)](../../attachments/FSStndSurf/Beauchamp_FL_VisLoc_reg.jpg)
[![](../../attachments/FSStndSurf/Beauchamp_FM_VisLoc.jpg)](../../attachments/FSStndSurf/Beauchamp_FM_VisLoc.jpg)[![](../../attachments/FSStndSurf/Beauchamp_FM_VisLoc_reg.jpg)](../../attachments/FSStndSurf/Beauchamp_FM_VisLoc_reg.jpg)
[![](../../attachments/FSStndSurf/Beauchamp_FN_VisLoc.jpg)](../../attachments/FSStndSurf/Beauchamp_FN_VisLoc.jpg)[![](../../attachments/FSStndSurf/Beauchamp_FN_VisLoc_reg.jpg)](../../attachments/FSStndSurf/Beauchamp_FN_VisLoc_reg.jpg)

1. This mapping process takes about 1/2 hour per hemisphere. The following steps can be used to automate this process for many hemispheres.

```
set sdall = ( /Volumes/data9/surfaces/graham_tim/FL/SUMA/  /Volumes/data9/surfaces/couch_david/FM/SUMA/  /Volumes /data9/surfaces/graham_sean_v2/FN/SUMA/ \
/Volumes/data9/surfaces/elmore_caitlin/DK/SUMA/  /Volumes/data9/surfaces/jen_emily/FS/SUMA/  /Volumes/data9  /surfaces/pasalar_siavash/SP/SUMA/ \
/Volumes/data9/surfaces/rushworth_david/FW/SUMA/  /Volumes/data9/surfaces/yasar_nafi/DJ/SUMA/ /Volumes/data9    /surfaces/singh_akanksha/FZ/SUMA/ )
set idx = 1
foreach ec (FL FM FN FQ FS FU FW FY FZ)
set sd = $sdall[$idx]
cd /Volumes/data1/UT/{$ec}/afni
foreach hemi (lh rh)
 echo Processing $sd hemi $hemi
3dVol2Surf -overwrite -spec {$sd}/{$ec}_{$hemi}.spec -surf_A smoothwm  -sv {$ec}_SurfVol_Alnd_Exp+orig -oob_value 0 \
-grid_parent {$ec}v1mr_REML+orig -map_func mask   -out_1D {$ec}v1mr_{$hemi}_all.1D
SurfToSurf -overwrite -prefix {$ec}v1mr_{$hemi}_all_reg.1D -output_params Data -data  {$ec}v1mr_{$hemi}_all.1D  \
-i /Volumes/data9/surfaces/fsaverage/SUMA/{$hemi}.sphere.reg.asc  -i {$sd}/{$hemi}.sphere.reg.asc 
@ idx++
echo $idx
end
end
```

1. Perform group analysis

Many of the same techniques and tools used to perform volume group analysis can also be used on the surface.
Smoothing before averaging can be performed with SurfSmooth

```
 SurfSmooth -overwrite -target_fwhm 10 -output temp{$ec}.niml.dset -i  rh.sphere.reg.asc -met HEAT_07 -input {$ec}v1mr_{$hemi}_all_reg.1D'[13]'
```

A t-test can be performed to find all nodes that are different from 0

```
3dttest -base1 0 -set2 FLv1mr_FL_VisLoc_reg.1D'[7]' FMv1mr_lh_VisLoc_reg.1D'[7]' FNv1mr_lh_VisLoc_reg.1D'[7]' \
-prefix testavg
```

The results from averaging the three subjects above are shown here (with no smoothing)
[![](../../attachments/FSStndSurf/Beauchamp_Avg_VisLoc.jpg)](../../attachments/FSStndSurf/Beauchamp_Avg_VisLoc.jpg)
Here are the results from 9 subjects, with and without smoothing:

1. A similar process can be used to calculate the average time series across subjects for each node on the surface

This requires that a percent signal change IRF brik has been created already (it only makes to average data in standardized % signal change.)
This data is mapped to the surface and then to the standard surface, as above:

```
3dVol2Surf -overwrite -spec {$sd}/??_rh.spec -surf_A smoothwm  -sv {$ec}_SurfVol_Alnd_Exp+orig -oob_value 0 \
-grid_parent {$ec}_short_irfpcnt+orig  -map_func mask   -out_1D {$ec}v1mr_rh_irf.1D 
SurfToSurf -overwrite -prefix  {$ec}v1mr_rh_irf_reg.1D  -output_params Data -data   {$ec}v1mr_rh_irf.1D \
-i /Volumes/data9/surfaces/fsaverage/SUMA/rh.sphere.reg.asc  -i {$sd}/rh.sphere.reg.asc &
```

To speed things up, the lh and rh can be done in parallel ("&" above)

```
3dVol2Surf -overwrite -spec {$sd}/??_lh.spec -surf_A smoothwm  -sv {$ec}_SurfVol_Alnd_Exp+orig -oob_value 0 \
-grid_parent {$ec}_short_irfpcnt+orig  -map_func mask   -out_1D {$ec}v1mr_lh_irf.1D 
SurfToSurf -overwrite -prefix  {$ec}v1mr_lh_irf_reg.1D  -output_params Data -data   {$ec}v1mr_lh_irf.1D \
-i /Volumes/data9/surfaces/fsaverage/SUMA/lh.sphere.reg.asc  -i {$sd}/lh.sphere.reg.asc
```

SurfToSurf writes out 12 un-needed columns in the inefficient 1D format; take just the needed columns and convert to binary .niml format

```
3dbucket -prefix {$ec}v1mr_lh_irf_reg.niml.dset -fbuc  {$ec}v1mr_lh_irf_reg.1D'[13..$]'
3dbucket -prefix {$ec}v1mr_rh_irf_reg.niml.dset -fbuc  {$ec}v1mr_rh_irf_reg.1D'[13..$]'
```

This process can be repeated across subjects. Copy all of the datasets to the group directory. For instance,

```
 cp ??v1mr_?h_irf_reg.niml.dset /Volumes/data1/UT/TacRelGroup/
```

Then, they can be merged with

```
 3dmean -prefix Group_Block_lh_psc.1D  FPv1mr_lh_irf_reg.1D'[13-68]' FRv1mr_lh_irf_reg.1D'[13-68]'  ...
```

Note this requires an equal number of columns (time points) from each subject. If this is not true, create a "minimum % change" BRIK of only the tasks that all subjects have in common.
For instance,

```
3dbucket -prefix junk -abuc  {$ec}_Decv{$v}_REML_rbeta+orig'[24..65,80..107]' 
3dcalc -a {$ec}EPIanatAlbl+orig -b junk+orig -prefix {$ec}_short_irfpcnt -expr '100 * b/a * step(1-abs(b/a))'
```

The average IRF dataset (or any individual) can be loaded into SUMA with the "Load Dset" button. It doesn't make sense to color in the surface based on the timeseries, so unclick the "View" button and instead turn on the graph with the "G" button.
