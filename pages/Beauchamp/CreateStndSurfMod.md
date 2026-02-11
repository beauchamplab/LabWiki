---
layout: default
title: "CreateStndSurfMod"
parent: Beauchamp
---
# CreateStndSurfMod


N.B. See also a newer version at
[Creating Standardized Surface Models New](../Creating_Standardized_Surface_Models_New.md)

The first few steps in creating a standardized surface are accomplished by running @GroupAnalysis. The main steps follow:

1) Run @new\_auto\_tlrc to compute a rigid transformation into TLRC space
This is a slightly modified version of @auto\_tlrc that can be found on /Volumes/data9.
We wish to use the -rigid\_equiv option transformation so that the surface is aligned but not stretched.
This is known as ACPCIATE within the script

```
@new_auto_tlrc -base TT_icbm452+tlrc -no_ss -input AXanatr3SS+orig -rigid_equiv
```

THIS WILL OVERWRITE any existing talairach transformations.

2) Run 3drefit to rename \*+tlrc files to \*+acpc files
For consistency, we want to call the files what they actually are (ACPC aligned, NOT talairach transformed)
3drefit -view acpc AXanatr3SS\_at\_S\_R+tlrc.

3) Run ConvertSurface to translate the FreeSurfer surfaces according to the transformation matrix from the first step (note that this converts the filetype to \*.ply)
This makes ACPC-aligned versions of the surface.

```
ConvertSurface -i_fs lh.smoothwm.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply lh.smoothwm_at_S_R -acpc 
ConvertSurface -i_fs rh.smoothwm.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply rh.smoothwm_at_S_R -acpc
ConvertSurface -i_fs lh.pial.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply lh.pial_at_S_R -acpc
ConvertSurface -i_fs rh.pial.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply rh.pial_at_S_R -acpc
ConvertSurface -i_fs lh.inflated.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply lh.inflated_at_S_R -acpc
ConvertSurface -i_fs rh.inflated.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply rh.inflated_at_S_R -acpc
ConvertSurface -i_fs lh.smoothwm.SS500.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply lh.smoothwm.SS500_at_S_R -acpc
ConvertSurface -i_fs rh.smoothwm.SS500.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply rh.smoothwm.SS500_at_S_R -acpc
ConvertSurface -i_fs rh.sphere.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply rh.sphere_at_S_R -acpc
ConvertSurface -i_fs lh.sphere.asc -sv AXanatr3SS_at_S_R+acpc.HEAD -o_ply lh.sphere_at_S_R -acpc
```

4) Run MapIcosahedron to create a standardized surface with EXACTLY 156,252 nodes.
Because each surface now has the same number of nodes, we can average at each node across subjects.

```
MapIcosahedron -spec lh+acpc.spec -prefix lh+acpc -morph sphere -ld 125 -it 20 
MapIcosahedron -spec rh+acpc.spec -prefix rh+acpc -morph sphere -ld 125 -it 20
```

Have to do this step separately for SS500 surface.

5) Create partially inflated surfaces from step 4 using SurfSmooth
THIS STEP IS OPTIONAL; lets you view partially inflated standard surfaces.

```
SurfSmooth -spec both+acpc_std.spec -surf_A lh+acpc_std.smoothwm.ply -met NN_geom -surf_out lh+acpc_std.smoothwm.SS500.ply -Niter 500 -match_area 0.01
SurfSmooth -spec both+acpc_std.spec -surf_A rh+acpc_std.smoothwm.ply -met NN_geom -surf_out rh+acpc_std.smoothwm.SS500.ply -Niter 500 -match_area 0.01
```

6) Create a surface volume that is aligned to the functional datasets

```
@SUMA_AlignToExperiment
```

[this step may not be necessary, check and see if surface is already in alignment for doing this step]

7) Run 3dVol2Surf to convert the functional dataset into a NIML file for faster processing (note that the NIML files are not currently working in our data analysis and we use 1D files instead)
This creates 1D or NIML files. These can then be processed with other programs, like 3dANOVA2, to create group surface maps.
for examples, see /Volumes/data1/UT/TactileGroup

## Creating Averaged Pial and Smoothwm Surfaces from multiple subjects

Here are the steps for creating averaged surfaces from anatomical data of many subjects:

1) Copy all the ply surface files from each of the subjects into a common directory.

2) Convert each ply file to a 1D file using ConvertSurface:

```
ConvertSurface -i_ply subjIDlh+acpc_std.pial.ply -o_1D subjIDlh+acpc_std.pial subjIDlh+acpc_std.pial
ConvertSurface -i_ply subjIDrh+acpc_std.pial.ply -o_1D subjIDrh+acpc_std.pial subjIDrh+acpc_std.pial
ConvertSurface -i_ply subjIDlh+acpc_std.smoothwm.ply -o_1D subjIDlh+acpc_std.smoothwm subjIDlh+acpc_std.smoothwm
ConvertSurface -i_ply subjIDrh+acpc_std.smoothwm.ply -o_1D subjIDrh+acpc_std.smoothwm subjIDrh+acpc_std.smoothwm
```

3) Average the location of each node on the standardized surface using 3dMean

```
3dMean -prefix rh.smoothwm.avg ASrh+acpc_std.smoothwm.1D.coord AXrh+acpc_std.smoothwm.1D.coord AYrh+acpc_std.smoothwm.1D.coord AZrh+acpc_std.smoothwm.1D.coord BArh+acpc_std.smoothwm.1D.coord BBrh+acpc_std.smoothwm.1D.coord BCrh+acpc_std.smoothwm.1D.coord BDrh+acpc_std.smoothwm.1D.coord BErh+acpc_std.smoothwm.1D.coord
```

```
3dMean -prefix lh.smoothwm.avg ASlh+acpc_std.smoothwm.1D.coord AXlh+acpc_std.smoothwm.1D.coord AYlh+acpc_std.smoothwm.1D.coord AZlh+acpc_std.smoothwm.1D.coord BAlh+acpc_std.smoothwm.1D.coord BBlh+acpc_std.smoothwm.1D.coord BClh+acpc_std.smoothwm.1D.coord BDlh+acpc_std.smoothwm.1D.coord BElh+acpc_std.smoothwm.1D.coord
```

4) Convert the 1D files using ConvertSurface

```
ConvertSurface -i_1D  rh.smoothwm.avg.1D ASrh+acpc_std.smoothwm.1D.topo -o_ply rh.smoothwm.avg.ply
ConvertSurface -i_1D  lh.smoothwm.avg.1D ASlh+acpc_std.smoothwm.1D.topo -o_ply lh.smoothwm.avg.ply
```

5) Use SurfSmooth to partially inflate the averaged surfaces
