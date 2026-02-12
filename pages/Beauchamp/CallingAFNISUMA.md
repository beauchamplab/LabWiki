---
layout: default
title: "CallingAFNISUMA"
parent: Beauchamp
---
# CallingAFNISUMA


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

Previous step is [Cortical Surface models overview](CorticalSurfaceOverview.md "Beauchamp:CorticalSurfaceOverview")

It can be quite a chore to invoke AFNI and SUMA and set up the viewers in an aesthetically appealing way. To automate this process, in each subject directory we create a script in each subject's home directory called "@ec" that is invoked like this:

```
./@ec
```

This does all of the work required to call AFNI and SUMA. The @ec script contains the following lines:

```
#! /bin/tcsh -f
echo "Calling full version of @ec that loads the std141 brains. Do it this way for easy updates of @ec script without updating multiple copies"
/Volumes/data/scripts/@ec_home_std141 $1
```

There are multiple copies of the @ec script (one in each subject directory). Each @ec script calls the same "home" script, @ec\_home\_std141 . As suggested by the comments, this script is structured this way because then only one script has to be updated (the home script) instead of updating every individual copy of the @ec script. The script @ec\_home\_std141 contains the following lines:

```
#! /bin/tcsh -f
echo "@ec: A script that automatically loads AFNI and SUMA for the current directory. See the Beauchamp Lab wiki ([Beauchamp](index.md)) for more details."
echo "This version of the script (@ec_home_std141) loads the std 141 brains because they are better for intersubject comparisons. This is designed for use with FreeSurfer 6.0. Michael S Beauchamp, August 2017."
echo "It should be run from an experiment directory. Example usage 1:  cd /Volumes/data/BCM/XX \n ./@ec \n"
set scriptsdir = /Volumes/data/scripts
set subjdir = `pwd`
cd afni
set afnidir = `pwd`
cd ../fs/SUMA
set sumadir = `pwd`
# Check if T1 anatomy exists for surface volume. If not, create it (required because AFNI multiple sessions functionality does not work with SUMA.)
cd $afnidir
if ( -f T1.nii ) then
echo "T1.nii already in place, loading AFNI and SUMA right away."
else
cd $sumadir
if ( -f T1.nii ) then
echo "Copying T1.nii from SUMA directory to AFNI directory."
cp T1.nii {$afnidir}
else
echo "Please create a T1.nii file in the AFNI directory to serve as SUMA's surface volume reference. e.g. 3dcopy XXanatavg+orig T1.nii"
goto END
endif
endif
cd $afnidir 
afni -R -niml  . $sumadir &
suma -niml  -spec {$sumadir}/std.141.fs_both.spec -sv {$afnidir}/T1.nii &
DriveSuma -com surf_cont -load_dset {$sumadir}/std.141.lh.sulc.niml.dset -surf_label lh.smoothwm.gii  -view_surf_cont y -load_cmap {$scriptsdir}/nice.1D.cmap -Dim 0.6
DriveSuma -com surf_cont -switch_cmap nice.1D -Dim 0.6
DriveSuma -com viewer_cont -key b  -1_only n
DriveSuma -com viewer_cont -key F3
DriveSuma -com viewer_cont -load_view  {$scriptsdir}/nice.niml.vvs -com surf_cont -switch_surf lh.inf_200.gii
DriveSuma -com viewer_cont -key t
DriveSuma -com surf_cont -1_only n
END:
```

This script references the following files. nice.1D.cmap contains the following lines

```
0.30	0.30	0.30	
0.33	0.33	0.33	
0.35	0.35	0.35	
0.38	0.38	0.38	
0.41	0.41	0.41	
0.43	0.43	0.43	
0.46	0.46	0.46	
0.48	0.48	0.48	
0.51	0.51	0.51	
0.54	0.54	0.54	
0.56	0.56	0.56	
0.59	0.59	0.59	
0.62	0.62	0.62	
0.64	0.64	0.64	
0.67	0.67	0.67	
0.69	0.69	0.69	
0.72	0.72	0.72	
0.75	0.75	0.75	
0.77	0.77	0.77	
0.80	0.80	0.80
```

nice.niml.vvs contains the following lines

```
# <Viewer_Visual_Setting
#  self_idcode = "XYZ_DwOIIz5Qag0UTN_FQL9Ytw"
#  domain_parent_idcode = "~"
#  geometry_parent_idcode = "~"
#  currentQuat = "0.500000 -0.500000 -0.500000 0.500000 "
#  translateVec = "0.000000 0.000000 "
#  clear_color = "1.000000 1.000000 1.000000 0.000000 "
#  FOV = "55.518543"
#  Aspect = "1.000000"
#  WindWidth = "350"
#  WindHeight = "350"
#  BF_Cull = "0"
#  Back_Modfact = "3.000000"
#  PolyMode = "1"
#  ShowEyeAxis = "0"
#  ShowMeshAxis = "0"
#  ShowWorldAxis = "0"
#  ShowCrossHair = "0"
#  ShowForeground = "1"
#  ShowBackground = "0"
# />
```
