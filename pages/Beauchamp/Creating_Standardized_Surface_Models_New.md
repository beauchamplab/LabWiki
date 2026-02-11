---
layout: default
title: "Creating Standardized Surface Models New"
parent: Beauchamp
---
# Creating Standardized Surface Models New


1) First, we create an AC-PC aligned version of the surface, as follows

Find the AC-PC transform using the AFNI script @auto\_tlrc (which calls various other programs) to compute a rigid transformation into TLRC space (this is the AC-PC alignment step without the stretching entailed by TLRC)

```
 @auto_tlrc -base TT_N27+tlrc -input DB_SurfVol+orig -rigid_equiv
```

2) Next, we apply this transformation back to the surface volume. Note that THIS WILL OVERWRITE any existing talairach transformations; there can only be one transformation per dataset.

```
 adwarp -apar DB_SurfVol_at_rigid+tlrc -dpar DB_SurfVol+orig
```

3) Run ConvertSurface to translate the original space FreeSurfer surfaces according to the transformation matrix from the first step (note that this converts the filetype to \*.ply). This makes ACPC-aligned versions of various version of the surface. We don't do all of them because they are rarely used (but we could).

```
 ConvertSurface -i_fs lh.smoothwm.asc -sv DB_SurfVol+orig -o_ply lh.smoothwm_tlrc -tlrc
 ConvertSurface -i_fs lh.inflated.asc -sv DB_SurfVol+orig -o_ply lh.inflated_tlrc -tlrc 
 ConvertSurface -i_fs lh.pial.asc -sv DB_SurfVol+orig -o_ply lh.pial_tlrc -tlrc
 ConvertSurface -i_fs lh.sphere.asc -sv DB_SurfVol+orig -o_ply lh.sphere_tlrc -tlrc 
 ConvertSurface -i_fs rh.smoothwm.asc -sv DB_SurfVol+orig -o_ply rh.smoothwm_tlrc -tlrc
 ConvertSurface -i_fs rh.inflated.asc -sv DB_SurfVol+orig -o_ply rh.inflated_tlrc -tlrc 
 ConvertSurface -i_fs rh.pial.asc -sv DB_SurfVol+orig -o_ply rh.pial_tlrc -tlrc
 ConvertSurface -i_fs rh.sphere.asc -sv DB_SurfVol+orig -o_ply rh.sphere_tlrc -tlrc
```

Create spec files to load these into SUMA

```
 cp /Volumes/data9/surfaces/scripts/both_tlrc.spec .
 cp /Volumes/data9/surfaces/scripts/lh_tlrc.spec .
 cp /Volumes/data9/surfaces/scripts/rh_tlrc.spec .
```

Check with

```
 afni &
 suma -spec both_tlrc.spec -sv DB_SurfVol+tlrc
```

4) Run MapIcosahedron to create a standardized surface with EXACTLY 156,252 nodes.
Because each surface now has the same number of nodes, we can average at each node across subjects.
Note that the program adds "\_std" to the given prefix.

```
MapIcosahedron -spec lh_tlrc.spec -prefix lh_tlrc -morph sphere -ld 125 -it 20 
MapIcosahedron -spec rh_tlrc.spec -prefix rh_tlrc -morph sphere -ld 125 -it 20
```

MapIcosahedron creates its own SPEC files but it is easier to use a single file that contains both hemispheres

```
  cp /Volumes/data9/surfaces/scripts/both_tlrc_std.spec .
```

Check with

```
 afni &
 suma -spec both_tlrc_std.spec -sv DB_SurfVol+tlrc
```

5) Register with experiment anatomy
Next, we have to register the standardized surface with the experiment data so we can map functional data onto the standardized surface.

```
 @auto_tlrc -base TT_N27+tlrc -input DBanatavg+orig -rigid_equiv
 adwarp -apar DBanatavg_at_rigid+tlrc -dpar DBanatavg+orig
 @SUMA_AlignToExperiment -exp_anat DBanatavg+tlrc -surf_anat /Volumes/data9/surfaces/beauchamp_michael/DB/SUMA/DB_SurfVol+tlrc
```

test with

```
 afni &
 suma -spec both_tlrc_std.spec -sv /Volumes/data1/UT/DB/afni/test/DB_SurfVol_Alnd_Exp+tlrc
```

((In theory, if a registered SurfVol already exists in ORIG space it might be possible to use that transformation with a command like

```
 adwarp -apar DB_SurfVol_at_rigid+tlrc -dpar DB_SurfVol_Alnd_Exp+orig
```

But that doesn't work.))

6) Using the standardized surface

```
 AFNI can get confused if there are multiple +tlrc datasets in a directory, so when mapping function we have to make sure that AFNI uses the right transformation.
 3drefit -apar DBanatavg+orig DBt1v1dec+orig
```

For some reason, SUMA doesn't like displaying the functional data in tlrc view of the AFNI viewer, so make sure to select "Original View" in the AFNI window. The correct transformations should be applied internally.

7) 3-D Coordinates
To plot 3-D coordinates to the standardized surface, first we convert them to AC-PC space

```
 VecWarp
```

and then we map to the surface

```
 SurfaceMetrics
```

8) To create sulcal depth files on the standardized surface, we map the existing sulcal depth file onto the standardized surface. It can then be loaded in with the SUMA surface controller for visualization.

```
 SurfToSurf -prefix test.1D -output_params Data -i  lh_acpc_std.smoothwm.asc -i lh.smoothwm.asc -data lh.sulc.asc
```

If a sulc file does not exist already it might be possible to create another one with these steps

```
3dSkullStrip -input TT_N27_SurfVol+tlrc.HEAD -o_ply TT_N27_BrainSurface.ply
SurfToSurf -i lh_acpc_std.smoothwm.asc -i TT_N27_BrainSurface.ply -prefix newdepth.1D -output_params DistanceToSurf
```

But this fails because the Surfaces are not in alignment.
