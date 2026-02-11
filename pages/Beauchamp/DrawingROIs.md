# DrawingROIs

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

How to draw ROIs on the surface for fMRI analysis using SUMA

## Draw ROI

Start SUMA, choose Tools/Draw ROI

Set a value for ROI (e.g., 1 for ROI1; when you start the next ROI, change the value for ROI2)

Use Right mouse button to trace region, double click right mouse button (or click "Join") to enclose region.
Then, right click inside region to fill. Then click "Finish".

Then "Save", rename it, and choose save as 1D file:
e.g. junk.1D.roi

## Convert to Volume

Next, we need to convert this file (e.g. junk.1D.roi) to the volume (i.e., BRIK, HEAD files that afni can use). This command should be run in the SUMA directory for the subject.
Note that the spec file used must match the surface that was drawn on. For example, if we drew the ROI on the std.141.lh brain so we must give 3dSurf2Vol this spec file.

In terminal, run the command:

```
3dSurf2Vol                           \
      -spec         std.141.fs_lh.spec        \
      -surf_A       std.141.lh.smoothwm.gii    \
      -surf_B       std.141.lh.pial.gii         \
      -sv           ../../afni/fs_SurfVol_Alnd_Exp+orig      \
      -grid_parent '../../afni/$function+orig[0]'   \
      -sdata_1D     ../../afni/junk.1D.roi        \
      -map_func     mode                \
      -f_steps      10                  \
      -prefix       junk_SurftoVol
```

## Combine with Functional Threshold

If you have a functional threshold that you would apply to this ROI mask, you can set the threshold as follows:

```
3dcalc -prefix junk_SurftoVol_thres -a junk_SurftoVol+orig -b87 function+orig -expr "equals(a,1)*step(b-10)"
```

In this case, we want to keep the voxels that pass F-stats > 10 in this ROI.

Then you will get a new ROI mask that has been converted from SUMA: junk\_SurftoVol\_thres+orig.
