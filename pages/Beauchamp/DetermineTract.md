# DetermineTract

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

After your diffusion tensor data has been processed and whole-brain pathways have been computed, DTIQuery v1.1 allows regions to be drawn for interactive tractography.

This is a great, fast way to explore all the fiber paths, but the regions you draw must be cuboid VOIs. The size of the cube can change, but it must be cuboid.

[![](../../attachments/DetermineTract/TA314_VOIexample.jpg)](../../attachments/DetermineTract/TA314_VOIexample.jpg)

For a more sophisticated analysis it's better to specify regions based on a mask or a combination of multiple masks.

This way, it's possible to see fiber pathways that intersect with areas of functional activation, probabilistic atlas templates, or a combination of both.

**This Wiki page shows how to automatically edit DTIQuery pathway files (.pdb files) based on regions specified in NIfTI image masks.**

## Downloading Code

These methods were developed by Tim Ellmore. Here is the link to his lab web page:
<https://sites.google.com/site/ellmorelab/code>

## Creating NIfTI Mask Files

If you've read the part of the Wiki entitled *Processing Diffusion Tensor Imaging Data*, you know how to compute whole-brain fiber pathways.

These pathways are stored in .pdb files. For example, you may like to find out which of the fibers in the pdb file intersect with the Zilles Brodmann area 44 probabilistic
template.

To do this, you first need to make a mask that is in NIfTI format (with a .nii extension) and that is in the same space as DTI from which your fiber paths were computed.

The example below shows how to use AFNI's programs to:

1) make a .nii file from the Anatomy Toolbox Maximal Probability Map AFNI BRIK

2) include only area 44 voxels: in the MPM file area 44 voxels have integer values of 165

THIS VALUE WILL CHANGE FROM VERSION TO VERSION OF THE ANATOMY TOOLBOX.
(It is correct for version 1.3, but in version 1.5, area 44 has the value of 160).
To examine what values are assigned to an area for your atlas,
type

```
 whereami -show_atlas_code
```

3) use 3dresample to make the mask have 2mm isotropic voxel sizes (the resolution of the DTI volumes)

```
 3dcopy -verb TT_N27_CA_EZ_MPM+tlrc.BRIK N27_MPM.nii
 3dcalc -a N27_MPM.nii -expr 'iszero(a-165)' -prefix BA44_mask.nii
 3dresample -master TA314_tlrc_fa.nii -prefix BA44_mask_2mm.nii -inset BA44_mask.nii
```

The mask produced from these commands is shown below, and may be loaded as a Background Image in DTIQuery

[![](../../attachments/DetermineTract/TA314_BA44Mask.jpg)](../../attachments/DetermineTract/TA314_BA44Mask.jpg)

## Visualizing NIfTI Mask Files

For visualization of mask files in DTIQuery, there are several options.
Using the "Load Background Images" menu, multiple files can be selected with the Apple key.
Then, the background images can be cycled through with the Cycle Background image.
However, this works well only if all background images are in the same space.
Here are the commands to convert a T1 anatomy to the same space as the DTI images:

```
 3dresample -master  CD_DMaps32+orig -prefix temp1 -inset {$ec}anatr2SS+orig
 set m = `3dBrickStat -max temp1+orig`
 3dcalc -prefix temp2 -datum float -a temp1+orig.HEAD -expr "a/$m"
 3dcopy  temp2+orig CD_anatresam.nii
```

It is often helpful to combine the T1 anatomy with the mask file for visualization.
First, we create a functional mask file, blurring it to ensure that it enters white matter:

```
  3dcalc -prefix test4 -a CDSTPv1+orig -expr "100*a"
  3dmerge -datum float -1blur_fwhm 10 -prefix test5 test4+orig
  3dcalc -prefix test6 -a test5+orig -expr "step(a)"
  3dresample -master CD_DMaps32+orig -rmode NN -prefix test7 -inset test6+orig
```

Next, we combine the T1 and functional mask using the MAX operation so that mask areas are colored in bright white:

```
  3dcalc -prefix temp8 -datum float -a temp2+orig -b test7+orig -expr "max(a,b)"
  3dcopy temp8+orig CD_anatSTPv2.nii
```

## The OR Operation: Finding Fiber Paths That Intersect with Any Voxels in a Single Image Mask

Using the mask created in the previous step and a pdb file containing whole-brain fiber pathways,
you may find the fiber pathways that intersect with the mask voxels by using autoedit\_pdb.m

This matlab function and other necessary sub-functions are found in /data9/matlab/dti

To use autoedit\_pdb properly, you must set your matlab path to include this directory and sub-directories (in Matlab choose File, then choose Set Path).

You can run the program from the Matlab command line by giving it the following 6 command line arguments:

**1)** mask file in .nii format (voxels with values of 1 or above will be considered the mask region)

**2)** a pdb file of whole-brain pathways (file must end in .pdb)

**3)** the name you want for the output pdb file (file name must end in .pdb)

**4)** a string to operate on either both, left, or right hemispheres

**5)** an integer check\_mode of either 1 or 2 indicating the type of desired intersection check:

*if 1, the algorithm will check all points of each pathway for mask intersection*

*if 2, the algorithm will check just the start and end points of each path for mask intersection*

**6)** the filename of a .nii image representing the number of pathways found to intersect the mask at each voxel

Here's an example of a typical command line:

```
autoedit_pdb('BA44_2mm_mask.nii','TA314_tlrc_precomputed.pdb','TA314_BA44.pdb','both',2,'TA314_BA44PathIntersect.nii');
```

The edited pdb output can be viewed in DTIQuery and you can see the pathways that intersect in this case with any of the mask voxels

[![](../../attachments/DetermineTract/TA314_editcheckmode2.jpg)](../../attachments/DetermineTract/TA314_editcheckmode2.jpg)

## Viewing pdb Files Created with autoedit\_pdb in DTIQuery

autoedit\_pdb works by keeping the path coordinates and path statistics (length, FA value, curvature) for fibers that intersect with the mask voxels,
and nulling the data fields for those fiber paths that do not intersect with any mask voxel.

What this means is that the same number of fibers exist in the edited compared to the unedited file,
but the coordinates and associated statistics fields of the non-intersecting paths have been set to zero.

THEREFORE IT IS EXTREMELY IMPORTANT THAT YOU DO THE FOLLOWING WHEN VIEWING THE EDITED PDB FILE:

After you load a background image and the edited pdb file in DTIQuery, you will notice that the min FA value (in the "Average FA Along Pathway" subwindow) is set to 0.0.

*You must set this value to a non-zero value and press RETURN in order to see accurate path count reports in the lower-left window.*

I recommend setting this FA value to 0.2, since that's the FA threshold used during the whole-brain fiber pathway computation step.

Keep in mind that if you view the edited fibers with a min FA value of 0.0, DTIQuery will mis-report the number of fibers you are looking at in the lower-left corner.

So, set the min FA to 0.2 and you will get accurate path counts when viewing the output of autoedit\_pdb.

Here's a picture of the min FA value box and the accurate count of the edited pdb file

[![](../../attachments/DetermineTract/TA314_minFA.jpg)](../../attachments/DetermineTract/TA314_minFA.jpg)

## The AND Operation: Finding Fiber Paths That Intersect with Multiple Regions

autoedit\_pdb essentially performs an OR operation. Given a mask it will find fiber pathways that intersect with any non-zero voxel in the mask.

If the mask contains two regions of voxels, it will return pathway 1 that passes through region 1 but not necessarily region 2, OR it will return pathway 2 that passes through region 2 but not necessarily region 1.

While this is useful, sometimes one wants to find pathways that pass both through region 1 and also through region 2, which is effectively the AND operation.

A separate function called autoand\_pdb has been written to do this.

It takes 7 command line arguments in the following order:

**1)** a string name of the first .nii mask image file (all non-zero voxels will be considered as a mask1)

**2)** a string name of the second .nii mask image file (all non-zero voxels will be considered as a mask2)

**3)** a string name for the input .pdb file of whole-brain fiber pathways

**4)** a string name for the output edited .pdb file to be written to disk

**5)** a string to operate on 'both' hemispheres, or just the 'left' or 'right' hemisphere

**6)** an integer check\_mode specified such that

*if 1 check all points of each path for mask intersection*

*if 2 check start and end points of each path for intersection*

**7)** a string name for the output .nii image summarizing path intersections

The first mask file should contain a set of non-zero voxels which does not overlap with a set of non-zero voxels in the second mask file.

An example of how to use autoand\_pdb is illustrated below in which fibers connecting BA 45 with left pre-SMA are isolated from the set of whole-brain fiber pathways:

```
autoand_pdb('BA45_2mm_mask.nii','LSMA_2mm_mask.nii','TA314_tlrc_precomputed.pdb','TA314_LPreSMAtoBA45.pdb','both',2,'TA314_LPreSMAtoBA45.nii');
```

The first argument is a mask of BA 45, the second argument is a mask of left pre-SMA, the third argument is the set of whole-brain fiber pathways, the fourth argument is the pdb file to be created, the fifth argument is the string both to operate on both hemispheres, the sixth is a 2 to just check the start and end points of each path for intersection, and the seventh is the name of the output .nii summary image to be created.

Below are two snapshots taken of the output at different axial levels, the first showing BA 45 and the second showing left pre-SMA.

The green fibers are the 20 pathways connecting the two mask regions.

[![](../../attachments/DetermineTract/TA314_LPreSMAMask.jpg)](../../attachments/DetermineTract/TA314_LPreSMAMask.jpg)

[![](../../attachments/DetermineTract/TA314_LBA45Mask.jpg)](../../attachments/DetermineTract/TA314_LBA45Mask.jpg)

autoand\_pdb can work with only two input masks at the moment, althought support for an unlimited number may be added in the future.

autoand\_pdb is a bit slower than autoedit\_pdb, especially when you give it a whole-brain set of pathways. You can speed it up by giving check\_mode as 2 rather than 1 but be careful interpeting the data.

One way to achieve a big speed boost is to give it a smaller pdb file created with the autoedit\_pdb OR operation and a single mask containing both regions (mask1 + mask2).

This way, a smaller subset of pathways may be considered, and autoand\_pdb function will select only pathways intersecting with mask1 and mask2.

## Appendix 1: the DTIQuery pdb file specification

David Akers, one of the creators of DTIQuery at Stanford, has generously provided us with the pdb file specification, describes how the path coordinates are stored in binary format.

This is what was provided and is how autoedit\_pdb.m assumes the pdb file is structured.

```
[ header size] - integer
-- HEADER FOLLOWS --
[ 4x4 transformation matrix which was used to transform from voxel space to scanner space (or some other space) ] - 16 doubles
[ number of pathway statistics ] - integer
for each statistic:
   [ currently unused ] - boolean
   [ is this statistic stored per point, or just as an aggregate per path? ] - boolean
   [ currently unused ] - boolean
   [ name of the statistic ] - char[255]
   [ currently unused ] - char[255]
   [ unique ID - an integer that uniquely identifies this statistic, across files ] - integer
[ number of algorithms ] - integer
for each algorithm:
   [ algorithm name ] - char[255]
   [ comments about the algorithm ] - char[255]
   [ unique ID - an integer that uniquely identifies this algorithm, across files ] - integer
-- HEADER ENDS --
[ number of pathways ] - integer
for each pathway:
   [ header size ] - integer
   -- PATHWAY HEADER FOLLOWS --
   [ number of points ] - integer
   [ algorithm ID ] - integer
   [ seed point index ] - integer
   for each statistic:
      [ precomputed statistical value ] - double
    -- PATHWAY HEADER ENDS --
   for each point:       [ position of the point - ALREADY TRANSFORMED from voxel space! ] - 3 doubles
   for each statistic:
      IF the statistic is also computed per point (see statistics header, second boolean field):
         for each point:
         [ statistical value for this point ] - double
```

## Appendix 2: Documentation for autoedit\_pdb.m

Here's matlab help documation for how autoedit\_pdb.m.

To really understand how it works, take a look at the code for autoedit\_pdb.m and the sub-function check\_pdbpath.m in /data9/matlab/dti

```
% [num_paths_in_mask,mask_coords,sum_img]=autoedit_pdb(mask_fname,pdb_in_fname,pdb_out_fname,hemi,check_mode,sum_img_fname)
%
% Edits the contents of a path database file (pdb_in_fname) made with DTIQuery 1.1
% based on the intersection of paths with non-zero voxels specified by a mask 
% file (mask_fname). Outputs those intersecting paths in a new file (pdb_out_fname).
% It keeps those pathways that intersect and nulls those that do not
% intersect. The output pdb file can be viewed in DTIQuery 1.1. This function
% was written to provide an alternative to cube VOIs, the only method
% currently available in DTIQuery to specify regions for tractography.
%
% For more information on DTI Query see:
%   http://graphics.stanford.edu/projects/dti/dti-query/
%
% This function loads .nii files using code written by:
%  Jimmy Shen of the Rotman Research Institute 
%   e-Mail: jimmy@rotman-baycrest.on.ca 
%   http://www.rotman-baycrest.on.ca/~jimmy/NIFTI/
%
% Inputs: 
%        mask_fname - .nii image file (non-zero voxels will be considered as a mask)
%        pdb_in_fname - .pdb file with whole-brain set of fiber pathways
%        pdb_out_fname - output edited .pdb filename to be written to disk
%        hemi - string to operate on 'both' hemispheres, or just the 'left' or 'right' hemisphere
%        check_mode - if 1 check all points of each path for mask intersection
%                   - if 2 check start and end points of each path for intersection
%        sum_img_fname - name of output .nii image summarizing path intersections
%
% Outputs (written to disk): 
%        pdb_out_fname - name of the output .pdb file (string must have .pdb suffix)
%
% Outputs (returned in matlab):
%        num_paths_in_mask - number of pathways that intersected with the mask
%        mask_coords - DTI Query coordinates of nonzero input mask voxels 
%        sum_img - image of number of path intersections at each voxel
%
% Notes: 
%        Input pdb files must be created with DTIQuery version 1.1, not
%         version 1.0
%        When you view the output file in DTI Query 1.1, set the FA threshold
%         to 0.2 and press return to see in the lower left corner the correct 
%         number of pathways retained during the autoediting operation. 
%
% Example Usage:
%        
% [num_paths_in_mask,mask_coords]=autoedit_pdb('BA44_2mm_mask.nii','TA314_tlrc_precomputed.pdb','TA314_BA44.pdb','both',2,'TA314_BA44PathIntersect.nii');
```

## Appendix 3: Documentation for autoand\_pdb.m

```
% [num_paths_in_mask,mask1_coords,mask2_coords,sum_img]=autoand_pdb(mask_fname1,mask_fname2,pdb_in_fname,pdb_out_fname,hemi,check_mode,sum_img_fname)
%
% Edits the contents of a path database file (pdb_in_fname) made with DTIQuery 1.1
% based on the intersection of paths with non-zero voxels specified by two mask 
% files (mask_fname1 and mask_fname2). Outputs paths that intersect voxels in both 
% mask files, effectively performing an AND function and outputs these paths in a 
% new file (pdb_out_fname). It keeps pathways that intersect with both masks and 
% nulls those that do not intersect. The output pdb file can be viewed in 
% DTIQuery 1.1. This function was written to provide an alternative to cube VOIs, 
% the only method currently available in DTIQuery to specify regions for tractography.
%
% For more information on DTI Query see:
%   http://graphics.stanford.edu/projects/dti/dti-query/
%
% This function loads .nii files using code written by:
%  Jimmy Shen of the Rotman Research Institute 
%   e-Mail: jimmy@rotman-baycrest.on.ca 
%   http://www.rotman-baycrest.on.ca/~jimmy/NIFTI/
%
% Inputs: 
%        mask_fname1 - .nii image file (non-zero voxels will be considered as a mask1)
%        mask_fname2 - .nii image file (non-zero voxels will be considered as a mask2)
%        pdb_in_fname - .pdb file with whole-brain set of fiber pathways
%        pdb_out_fname - output edited .pdb filename to be written to disk
%        hemi - string to operate on 'both' hemispheres, or just the 'left' or 'right' hemisphere
%        check_mode - if 1 check all points of each path for mask intersection
%                   - if 2 check start and end points of each path for intersection
%        sum_img_fname - name of output .nii image summarizing path intersections
%
% Outputs (written to disk): 
%        pdb_out_fname - name of the output .pdb file (string must have .pdb suffix)
%
% Outputs (returned in matlab):
%        num_paths_in_mask - number of pathways that intersected with the mask
%        mask1_coords - DTI Query coordinates of nonzero input mask1 voxels 
%        mask2_coords - DTI Query coordinates of nonzero input mask2 voxels
%        sum_img - image of voxels where fibers intersect both mask regions
%
% Notes: 
%        Input pdb files must be created with DTIQuery version 1.1, not
%         version 1.0
%        When you view the output file in DTI Query 1.1, set the FA threshold
%         to 0.2 and press return to see in the lower left corner the correct 
%         number of pathways retained during the autoediting operation. 
%
% Example Usage:
%        
% [num_paths_in_mask,mask_coords]=autoand_pdb('BA45_2mm_mask.nii','LSMA_2mm_mask.nii','TA314_tlrc_precomputed.pdb','TA314_LPreSMAtoBA45.pdb','both',2,'TA314_LPreSMAtoBA45.nii');
%
```

## Appendix 4: Documentation for read\_pdb.m

A general purpose function has been written to read pdb files and return the contents in matlab cell arrays: read\_pdb.m also found in /data9/matlab/dti

This function is not used by autoedit\_pdb.m, but nonetheless is very useful if you want to do some more compicated analysis or measurement of individual fiber pathways within matlab.

```
% [npathways,pd,ps,max_fa,min_fa,max_length,min_length,max_curv,min_curv]=read_pdb(pdb_fname, dbg)
% Reads the contents of the binary *.pdb file output from DTIQuery 1.1
%
% Inputs: 
%        pdb filename - string
%        dbg - verbose 1, or not verbose 0
%
% Outputs: 
%        npathways - number of fiber paths
%        pd - NPATHS-by-NPOINTS-by-3 cell array of path x,y,z coordinates
%        ps - NPATHS-by-4 cell array of path statistics (path length in mm, avg FA, avg curvature 1/mm)
%        max_fa - maximum avg path fractional anisotropy
%        min_fa - minimum avg path fractional anisotropy
%        max_length - maximum pathway length
%        min_length - minimum pathway length
%        max_curv - maximum average curvature
%        min_curv - mininum average curvature
%
% Notes: 
%        This function is intended for use with DTIQuery version 1.1, not version 1.0
%        This function is still in a development ... interpret output very carefully!!!
%        Each path can have different number of points, that's why output
%        is a cell array, not a matrix or a struct
%
% Example Usage:
%        % read small pdb file of 104 arcuate fasciculus fibers, verbose mode
%        [npathways,pd,ps]=read_pdb('TA301laf_fibers.pdb', 1);
%
%        % read large pdf file of entire set of brain fibers, no verbose
%        [npathways,pd,ps]=read_pdb('precomputed.pdb', 0);
%
% Last modified: 10/3/07, Timothy.Ellmore@uth.tmc.edu
%
```
