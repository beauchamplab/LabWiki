---
title: VibrationArtifacts
parent: Beauchamp
---
# VibrationArtifacts

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

# Some Background

Most subjects will tell you that the bed shakes during a DTI experiment. For some DTI experiments, this level of bed shaking is problematic as it leads to vibration artifacts. When the bed moves, it causes the brain wiggle inside the head, and you've effectively started to do MR Elastography at the same time as your DTI. The result of these vibrations is a signal loss when the bed shakes. Unfortunately, for most scanners (notably the Siemens Tim Trio, e.g. Bay 5; but for a [variety of scanners](https://onlinelibrary.wiley.com/doi/abs/10.1002/hbm.22846) ) the shaking (and signal loss) is mostly related to the strength of the x-gradients. That's also what it looks like when there's strong x-direction diffusion. So, the end result is that, after running data with these artifacts through your general processing pipeline, you get what looks like absurdly strong x-direction diffusion in places where it shouldn't be. Also, because the vibration increases linearly-ish with the strength of the x-gradients, many DTI data checks and algorithms are unable to fix or even detect the artifact. (Based on my not-terribly-extensive literature searching), one method has been proposed for correcting these artifact. Both the method and some more background on the artifact itself are described [here](https://onlinelibrary.wiley.com/doi/full/10.1002/hbm.20856) by Gallichan, et al. The rest of this page will describe step by step how to apply the correction described by Gallichan and colleagues to some data that was acquired at CAMRI.

OF COURSE, it's always better to acquire data  *without*  artifacts. Some things that (probably? maybe?) contributed to the occurrence of the vibration artifact in these data were that the partial Fourier was aggressive at 5/8, and the gradient directions were set up such that the x-gradients varied the most over time.

# Overview

1. Select volumes with low x-gradients (MATLAB)
2. Compute distortion correction, motion correction, eddy current correction (TORTOISE)
3. Compare the DT fits, identifying the regions that are most affected by the vibration artifact
4. Calculate the effect of vibration on the DWIs
   1. Simulate the ‘right’ DWI volumes from the low-x data DTs and the gradients
   2. Fit the difference between measured and simulated to get a correction equation
5. Apply the correction equation to the measured DWIs, and re-do tractography to check the results (and presumably, carry on with whatever analyses you originally intended.)

# Select volumes with low x-gradients (MATLAB)

a. Load .bvec file into MATLAB

b. Add column of index

```
 >> ind=[1:79]';
 >> V = [V ind];
```

c. Identify which volumes had low x-gradient values

```
 >> alt_fit=V(abs(V(:,1))<0.5, 4)'
 >> for a=1:size(alt_fit); fprint(1, "%d, ", alt_fit(a)-1); end
```

d. Make new NIFTI, .bval, and .bvec files with the selected gradients
Copy the output from MATLAB, and paste into terminal shell

```
 $ low_x_str=”PASTED_OUTPUT” 
 $  3dTcat -prefix lowx.nii DTI.nii”[$low_x_str]”
 $ 1dcat DTI.bval"[$low_x_str]" > lowx.bval
 $ 1dcat DTI.bvec”[$low_x_str]” > lowx.bvec
```

# Compute distortion correction, motion correction, eddy current correction (TORTOISE)

```
ImportNIFTI -i DTI.nii -b DTI.bval -v DTI.bvec -p vertical
ImportNIFTI -I lowx.nii -b lowx.bval -v lowx.bvec -p vertical
```

```
DIFFPREP -i DTI_proc/DTI.list --will_be_drbuddied 0 --do_QC
DIFFPREP -i lowx_proc/lowx.list --will_be_drbuddied 0 --do_QC
```

# Compare the DT fits, identifying the regions that are most affected by the vibration artifact

```
EstimateTensorNLLS -i DTI_proc/DTI_DMC.list 
EstimateTensorNLLS -i lowx_proc/lowx_DMC.list
```

```
3dcalc -a DTI_proc/DTI_DMC_N1_DT.nii -b lowx_proc/lowx_DMC_N1_DT.nii -expr ‘abs(a-b)’ -prefix diff_DT.nii
```

We’re actually going to compute this again later, because it turns out that TORTOISE and AFNI don’t use the same origin… but it’s good to sanity check here.

**SANITY CHECK— These look a lot like the regions in the paper.**  If they don't look like the regions in the Gallichan paper, then you should double check that you're actually looking at a vibration artifact.

# Calculate the effect of vibration on the DWIs

a. Convert the format

```
ConvertNewListfileToOld DTI_proc/DTI_DMC.list
ConvertNewListfileToOld lowx_proc/lowx_DMC.list
```

```
cd /Applications/TORTOISE/DIFFCALC/DIFFCALCV25/DIFFCALC/diffcalc_main
./calcvm
```

- “load listfile”, navigate to DTI\_proc/DTI\_DMC\_OF.list
- “export images”, “AFNI”, “DONE”
- Repeat for lowx\_proc/lowx\_DMC\_OF.list

b. Calculate the DTs from the low-x DWIs

```
3dDWItoDT -prefix lowx_DT.nii -bmatrix_Z lowx_proc/lowx_DMC_OF_SAVE_AFNI/BMTXT_AFNI.txt lowx_proc/lowx_DMC_OF_SAVE_AFNI/DWI.nii
```

```
3dcopy lowx_DT.nii lowx_DT+orig.HEAD
```

*Not entirely sure this step was actually necessary, but it didn't seem to hurt anything.*

## Simulate the ‘right’ DWI volumes from the low-x data DTs and the gradients

(in DTI\_proc/DTI\_DMC\_OF\_SAVE\_AFNI folder)

```
3dTcat -prefix b0.nii DWI.nii"[0,10,20,30,40,50,60,70]"
```

These volume indices were specific to this particular acquisition. Use whatever indices are suitable to \*your\* data to get all your b=0 volumes.

```
3dTstat -mean -prefix mean.b0.nii b0.nii
3dAutomask -prefix m.mean.b0.nii mean.b0.nii
```

**SANITY CHECK— Make sure you look at this mask file.**  If there are parts that are missing/shouldn’t be there, you can modify it using the draw ROI plugin. See info here: <https://afni.nimh.nih.gov/pub/dist/edu/latest/afni_handouts/afni11_roi.pdf>, starting at page 6. You could also make the brain mask from the anatomical and resample to DTI resolution (3dresample or 3dfractionize)

```
3dcalc -a m.mean.b0.nii -b mean.b0.nii -expr 'a*b' -prefix mask.mean.b0.nii
1dDW_Grad_o_Mat++ -in_col_matA BMTXT_AFNI.txt -out_col_vec Gxyz.txt
```

- Manually remove 0 0 0 lines from Gxyz.txt

```
3dDTtoDWI -prefix sim_DWI.nii Gxyz.txt mask.mean.b0.nii lowx_DT+orig
```

## Fit the difference between measured and simulated to get a correction equation

a. Find mask of area affected by artifact (again)

(In DTI\_proc/DTI\_DMC\_OF\_SAVE folder, assuming bash shell)

```
3dDWItoDT -prefix allx_DT.nii -bmatrix_Z BMTXT_AFNI.txt DWI.nii
3dcalc -a allx_DT.nii -b lowx_DT+orig. -expr 'a-b' -prefix diff.nii
for n in `count -dig 1 0 5`
  do 
  echo $n
  dif_avg=`3dmaskave -q -sigma -mask m.mean.b0.nii diff.nii | awk -v N=$n 'NR==(N+1){print $1}'`
  sd=`3dmaskave -q -sigma -mask m.mean.b0.nii diff.nii | awk -v N=$n 'NR==(N+1){print $2}'`
  3dcalc -a diff.nii"[$n]" -b m.mean.b0.nii -prefix diff_z_$n.nii -overwrite -expr "b*abs((a-$dif_avg)/$sd)"
done
```

*I bet if you tried for a bit you’d find a more elegant way to do this… it’s essentially taking a z-score of each difference map of the DTs.*

```
3dMean -prefix mean_diff_z.nii diff_z*
3dcalc -a mean_diff_z.nii -b m.mean.b0.nii -expr 'b*step(a-1)' -prefix artifact_mask.nii
```

This next bit gets rid of the stray voxels

```
3dmask_tool -overwrite -dilate_inputs -1 1 -prefix dil.artifact_mask.nii -input artifact_mask.nii
```

**SANITY CHECK— Make sure you look at this mask file.**  If you have regions that are included because they’re on the edges of the brain or in non-brain, it’s going to mess up the ratio, and then the fit, and then the correction… look closely, or risk having to do a few pieces over. Trust me.

b. Fit the difference within the mask

```
3dTcat -prefix b1000.nii DWI.nii"[1..9, 11..19, 21..29, 31..39, 41..49, 51..59, 61..69, 71..78]"
```

As before, these indices are specific to this acquisition. You may have to adjust to make it work for your own data.

The simulated DWI data has one b=0 volume at the start, so get rid of that.

```
3dTcat -prefix c.sim_DWI.nii sim_scale_DWI.nii'[1..$]'
```

**SANITY CHECK— Check that this correction make sense.**  Open b1000.nii in afni, turn on a graph. Click “Opt” in the bottom right of the graph window, choose “Tran 1D” dropdown and option “Dataset #N”. Turn on “input #01”, choose dataset, and pick c.sim\_DWI.nii. Then, “Set+Keep.” If you click in an area where the artifact was, the red and black lines should look very different, if you click in an area where there wasn’t much artifact, they should look largely the same.

```
3dcalc -a c.sim_DWI.nii -b b1000.nii -c m.mean.b0.nii -expr '(b/a)*c' -prefix ratio.nii
3dmaskave -q -mask dil.artifact_mask.nii ratio.nii > ratio_in_mask.txt
```

(IN MATLAB)

```
>> G=load('Gxyz.txt');
>> R = load('ratio_in_mask.txt');
```

**SANITY CHECK— plot(G(:,1), R, ‘o’) should look a lot like Figure 6a from the paper.**

[MATLAB Code Here](../BeauchampLab/VibrationMatlabCode.md)

# Apply the correction equation to the measured DWIs, and re-do tractography to check the results (and presumably, carry on with whatever analyses you originally intended.)

a. For those voxels inside the mask, divide their measured DWI data by the fitted tukey correction.

```
3dcalc -a dil.artifact_mask.nii -b tukey_correction.1D -c DWI.nii -expr 'c/(a*b + step(1-a))' -prefix mask_corrected.nii -datum float
```

b. Load the ‘corrected’ DWIs into DTItoolkit/TRACKVIS and see how the tractography looks.

```
1dDW_Grad_o_Mat++ -in_col_matA BMTXT_AFNI.txt -out_col_vec unit_Gxyz.txt -unit_mag_out
more unit_Gxyz.txt
```

- Copy and paste output into DTItoolkit, and reconstruct using mask\_corrected.nii
