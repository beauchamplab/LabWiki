# Making Resting State Correlation Maps

> **Navigation:** [Home](Beauchamp/index.md) | [Publications](Beauchamp/Publications.md) | [Resources](Beauchamp/DataSharing.md)

In order to more easily compare fMRI and ECoG resting state data, it is helpful to make maps of the cortical surface where the electrode spheres are color coded based on their correlation to a seed electrode. All code can be found in /volumes/data2/SARAH/intraelecproject/analysismfiles/corrmaps

**1. Obtain resting state time series**

*Get coordinates from underneath the electrodes*
It works best if you use the coordinates from the ClosestNodes data set, because these coordinates are tied to the surface. Make a version of this test file where the header is removed.

*Create a .1D file with just these coordinates*
To make a mask of with just these voxels, use:

```
1dcat input.1D'[6,7,8]' {$ec}xyz.1D
```

where input.1D is the name of the 1D file you made without the ClosestNodes header. It is important to stick to this naming convention because it is used in the MATLAB files later.

*Run dumpmasklist.csh to get the time series from the EPI.*

```
tcsh dumpmasklist.csh {$ec}xyz.1D dset+orig {$ec}reststTS.1D
```

where dset+orig is the fMRI resting state run. The output will have the raw time series for each voxel underneath the electrodes. If a line is empty (i.e. it only has # x y z and no time series) that means that particular voxel was outside of the fMRI coverage. It is ideal to limit the number of electrodes outside of fMRI coverage for obvious reasons.

**2. Compute correlations**

*Use TSconvert.m*
This will read in the coordinates and time series from the dumpmasklist.csh output, then make a table of all the correlations. It will also make a figure of this table, which might give you an idea of groups of electrodes that are highly correlated.

**3. Create .1D spheres files and take pictures.**

*Use corrconnect.m*
For each electrode, you will get a correlation map (seed electrode is colored black) and three pictures with different views of the surface will be taken in SUMA. It is important to have SUMA open and the surface you wish to use (usually the pial surface) already open. Because this is a large number of files (3 \* the number of electrodes), you may want to make a restingstateMRcorrmaps folder under {$ec}/afni to hold all these pictures.

***Make sure you have the latest version of SUMA downloaded. If you do not, the electrodes that should be colored green will appear white or yellow tinged white. This problem was fixed with the version that was compiled on October 26, 2010***
