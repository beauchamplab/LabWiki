# ROIanalysis

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

If you would like to compare activity across subjects in threshold-defined areas, an ROI analysis may be right for you!

## Creating a posterior STS ROI

This is the method used in Zhu & Beauchamp, Journal of Neuroscience (2017).

For 2009 atlas:

```
 LH:
 STS - ctx_lh_S_temporal_su - 117
 STG - ctx_lh_G_temp_sup-Lat - 78
 MTG - ctx_lh_G_temporal_mid - 82

 RH:
 STS - ctx_rh_S_tempral_su - 191
 STG - ctx_rh_G_temp_sup-Lat - 152
 MTG - ctx_rh_G_temporal_mid - 156
```

For "renumbered data sets" (replacing the 'RANK' dataset since Nov2019 in default outputs for @suma\_make\_spec\_fs)

```
 LH:
 STS - ctx_lh_S_temporal_su - 121
 STG - ctx_lh_G_temp_sup-Lat - 82
 MTG - ctx_lh_G_temporal_mid - 86

 RH:
 STS - ctx_rh_S_tempral_su - 196
 STG - ctx_rh_G_temp_sup-Lat - 157
 MTG - ctx_rh_G_temporal_mid - 161
```

==(For the following steps, replacing 'aparc.a2009s+aseg\_rank\_Alnd\_Exp' with 'aparc.a2009s+aseg\_REN\_Alnd\_Exp+orig', the REN file was created by:
3dAllineate -master anatavg+orig -1Dmatrix\_apply fs\_SurfVol\_Alnd\_Exp.A2E.1D -input aparc.a2009s+aseg\_REN\_all.nii.gz -prefix ./aparc.a2009s+aseg\_REN\_Alnd\_Exp -final NN)==

Create an ROI that includes all 6 of these regions. Left hemisphere ROIs are assigned value 1, right hemisphere ROIs are assigned value 2.

```
 3dcalc -prefix STSparc09_v1 -a aparc.a2009s+aseg_rank_Alnd_Exp+orig -expr "1*step(equals(a,117) + equals(a,78) + equals(a,82)) + 2*step(equals(a,191)+equals(a,152)+equals(a,156))"
```

Because the ROI is in anatomical space (typically higher resolution than the BOLD fMRI data) we must resample the ROI to fMRI resolution. Replace stats+orig with the stats dataset you will be applying the ROI to. The NN option uses nearest-neighbor interpolation to be sure that new ROI values are not created.

```
 3dresample -master stats+orig -prefix STSparc09_v1_resample -inset STSparc09_v1+orig  -rmode NN
```

Find the full A-P extent of the ROI.

```
 3dclust 5 100 STSparc09_v1_resample+orig
```

You will get something that looks like this:

```
 #Volume  CM RL  CM AP  CM IS  minRL  maxRL  minAP  maxAP  minIS  maxIS    Mean     SEM    Max Int  MI RL  MI AP  MI IS
 #------  -----  -----  -----  -----  -----  -----  -----  -----  -----  -------  -------  -------  -----  -----  -----
   24750  -58.7   -5.2  -25.6  -72.5  -40.0  -56.2   51.3  -49.9   -2.4        2        0        2  -72.5   -1.2   -9.9 
   24625   53.1    2.8  -24.1   30.0   70.0  -53.7   61.3  -49.9    2.6        1        0        1   30.0   51.3  -19.9
```

Take the halfway point of the full A-P extent:

```
 cutoff = 0.5 * (minAP + maxAP)
```

Left is POSITIVE in DICOM co-ordinates, so the first row in the table is the RIGHT hemisphere (negative RL values) and the second row in the table is the LEFT hemisphere (positive RL values). We do the calculation separately for each hemisphere.
In this example, the A-P cutoffs are:

```
 RH: (-56.2+51.3)/2 = -2.45
 LH: (-53.7+61.3)/2 = 3.8
```

Use these values to select out the posterior half of the STS (remember that LH has value 1 and RH has value 2).

```
3dcalc -prefix pSTS_ROI -a STSparc09_v1_resample+orig -expr "1*equals(a,1)*step(x-(-2.45)) + 2*equals(a,2)*step(x-(3.8))"
```

NB: This will fail if the x-axis of the dataset is not Anterior-to-Posterior. Check this with

```
 3dinfo STSparc09_v1_resample+orig | grep Anterior-to-Posterior
```

If this returns

```
 first  (x) = Anterior-to-Posterior
```

You are OK. If not, replace "x" with the axis letter inside the parentheses (either y or z).
This ROI can then be applied to your statistical data. For instance, select all LH pSTS voxels that have Full-F>7.8 (sub-BRIK 0) and a positive value on the Mouth vs. Eye contrast (sub-BRIK 17).

```
 3dcalc -prefix MouthVoxels -a pSTS_ROI+orig -b0 stats2.PU+orig.HEAD -c17 stats2.PU+orig.HEAD -expr "equals(a,1)*step(b-7.8)*step(c-2)"
```

Finally, calculate the average response to auditory speech in these voxels.

```
 3dROIstats -mask MouthVoxels+orig stats2.PU+orig'[7]'
```

## Creating 5 different ROIs

For example, we may be interested in comparing amplitude of activity in auditory cortex during different types of speech stimuli in people with different behavioral characteristics. While we could use a group whole-brain analysis to see if there are any voxels in a combined map within auditory cortex that show a differential response, it may be better to separately define each auditory ROI in each subject using strict and reproducible criteria, such as T stat > 3.

To facilitate this process, the surfaces in SUMA come already parcellated into useful regions. With the parcellation, each anatomical region is assigned a value (same in left and right hemisphere). So, for each subject, we can find active areas within these anatomical locations to use as ROIs. Depending on when the surface was made, the parcellation is done either with a 2005s or 2009s atlas.

Here are the parcellation values corresponding to 5 regions of interest using the 2005s atlas:

```
 Auditory cortex                        33, 81
 Extrastriate visual cortex (V5/MT)     60
 Fusiform gyrus                         17, 63
 Inferior frontal gyrus                 6,  72
 Superior temporal sulcus               80
```

And for the 2009s atlas:

```
 Auditory cortex                        466, 514
 Extrastriate visual cortex (V5/MT)     493
 Fusiform gyrus                         450
 Inferior frontal gyrus                 285, 505
 Superior temporal sulcus               513
```

To use these parcellations, first copy over the parcellation files from the SUMA folder:

```
 cd /Volumes/data9/surfaces/last_name/subjID/SUMA/				
 cp lh.aparc.a2005s.annot.1D.roi /Volumes/data1/UT/{$ec}/afni				
 cp rh.aparc.a2005s.annot.1D.roi /Volumes/data1/UT/{$ec}/afni				
 cd /Volumes/data1/UT/{$ec}/afni				
```

Then, convert them into BRIK files for AfNI analysis:

```
 3dSurf2Vol -spec /Volumes/data9/surfaces/netek_anne/HO/SUMA/both.spec -surf_A lh.smoothwm.asc \				
 -grid_parent {$ec}v1mr+orig -sv {$ec}_SurfVol_Alnd_Exp+orig -map_func max -prefix L_parc -sdata_1D lh.aparc.a2005s.annot.1D.roi				
```

```
 3dSurf2Vol -spec /Volumes/data9/surfaces/netek_anne/HO/SUMA/both.spec -surf_A rh.smoothwm.asc \
 -grid_parent {$ec}v1mr+orig -sv {$ec}_SurfVol_Alnd_Exp+orig -map_func max -prefix R_parc -sdata_1D rh.aparc.a2005s.annot.1D.roi
```

The Freesurfer parcellation gives us the entire length of the STS, but what if you are interested only in the posterior portion of this sulcus? It seems fair to consider only the posterior half of the STS for further analysis when studying STSms. To do this, first create an STS ROI for the entire length. In this example, the left STS in a 2009s parcellation of subject HT:

```
 3dcalc -prefix {$ec}_L_STS_anat_parc -a0 L_parc+orig -expr "step(equals(a,513))"
```

Now, let's see how far anterior and posterior this ROI actually goes:

```
 3dclust 5 100 {$ec}_L_STS_anat_parc+orig
```

with output of

```
 #Volume  CM LR  CM PA  CM IS  minLR  maxLR  minPA  maxPA  minIS  maxIS    Mean     SEM    Max Int  MI LR  MI PA  MI IS
 #------  -----  -----  -----  -----  -----  -----  -----  -----  -----  -------  -------  -------  -----  -----  -----
   16516  -52.8  -22.7   -6.9  -66.0  -38.5  -74.2   33.1  -25.9   13.1        1        0        1  -44.0   27.6  -25.9
```

This is the entire STS. If we examine the conjunction of auditory and visual activity (t > 2) in the STS, it extends from -31 mm to + 6 mm.
There are a few approaches to handling this blob:

1. Circle the entire blob manually using the draw tool in SUMA
2. The blob is essentially in the mid STS, but FreeSurfer does not parcellate the STS into different sub-regions. One way to do this would be to divide it up ourselves based on the A-P extent, in this case from -74 to 33.

Divide up the STS into halves or thirds, and use that as the cutoff.

Here is an example of how to do this with 3dcalc.
We can determine the halfway "cutoff" for y-values in the posterior segment:

```
 cutoff = ((maxPA-minPA) * 0.5) + minPA
```

In this example, cutoff = (abs(33.1) + abs(-74.2)) \* 0.5 - 74.2 = -20.55.

Set this cutoff in the script:

```
 set cutoff = -20.55
```

Now, we can find voxels that are within the STS anatomical parcellation (in a 2009 parcellation in this case), active during auditory and visual blocks \*and\* are posterior to y = -20.55:

```
 3dcalc -prefix {$ec}_L_pSTS_auto_parc -a0 L_parc+orig -b17 {$ec}v1mr+orig -c20 {$ec}v1mr+orig -expr "step(b-2)*step(c-2)*step(equals(a,513))*step(y+$cutoff)"
```

```
 (I realize that the "step(y+$cutoff)" command is kind of backwards. If we want all the values more negative than -20.55, 
 I thought it would've been "isnegative(y-$cutoff)". But, this way works.)
```

Another example: here we find voxels within the left auditory cortex that are active (T > 2) during auditory blocks in a subject with an old-school 2005s parcellation:

```
 3dcalc -prefix {$ec}_L_aud_parc -a0 L_parc+orig -b17 {$ec}v1mr+orig -expr "step(b-2)*step(equals(a,33)+equals(a,81))"
```

## Calculating Activity Strengths after the ROI is created

Perhaps you would like to know the strength of activity averaged across these voxels. It's nice to use percent signal change values, since these are more easily comparable across subjects. First, use tent functions withing 3dDeconvolve to create a nice hemodynamic response for each voxel for each stimulus type:

```
 set v = 2
 3dDeconvolve -fout -tout -full_first -polort a -concat runs.txt \
 -input {$ec}Albl+orig -num_stimts 12 -nfirst 0 -jobs 2 \
 -mask {$ec}maskAlbl+orig  \
 -stim_times 1 McG.txt 'TENT(0,16,9)' -stim_label 1 McGurk \
 -stim_times 2 NonMcG.txt 'TENT(0,16,9)' -stim_label 2 InC \
 -stim_times 3 Cong.txt 'TENT(0,16,9)' -stim_label 3 Cong \
 -stim_times 4 Target.txt 'TENT(0,16,9)' -stim_label 4 Target \
 -stim_times 5 Ablock.txt 'TENT(0,26,14)' -stim_label 5 Ablock \
 -stim_times 6 Vemotion.txt 'TENT(0,26,14)' -stim_label 6 Vemotion \
 -stim_file 7 {$ec}rall_vr_motion.1D'[0]' -stim_base 7 \
 -stim_file 8 {$ec}rall_vr_motion.1D'[1]' -stim_base 8 \
 -stim_file 9 {$ec}rall_vr_motion.1D'[2]' -stim_base 9 \
 -stim_file 10 {$ec}rall_vr_motion.1D'[3]' -stim_base 10 \
 -stim_file 11 {$ec}rall_vr_motion.1D'[4]' -stim_base 11 \
 -stim_file 12 {$ec}rall_vr_motion.1D'[5]' -stim_base 12 \
 -iresp 1 irf1_tent -iresp 2 irf2_tent -iresp 3 irf3_tent -iresp 4 irf4_tent -iresp 5 irf5_tent -iresp 6 irf6_tent \
 -prefix {$ec}v{$v}mr
```

```
 3dTcat -prefix {$ec}v{$v}irf irf1_tent+orig irf2_tent+orig irf3_tent+orig irf4_tent+orig  irf5_tent+orig irf6_tent+orig
```

Then, convert these impulse response functions into percent signal change:

```
 3dcalc -a {$ec}v2irf+orig -b {$ec}EPIanatAlbl+orig -expr '100 * a/b * ispositive(10-a/b)' -prefix {$ec}psc_AV
```

Perhaps we are interested in the amplitude of response during each of four event-related conditions listed (McGurk, incongruent, congruent and target). The hemodynamic response peaks between 4-6 seconds, so it works to average the 3rd and 4th points together to estimate the height of the response in percent signal change:

```
 # Psc files-- takes average of points 2 and 3 of the HRF (the numbering is 0-8, so points 2 and 3 are the 3rd and 4th points of the series)
 3dMean -prefix {$ec}McGpsc {$ec}psc_AV+orig'[2]' {$ec}psc_AV+orig'[3]' 
 3dMean -prefix {$ec}InCpsc {$ec}psc_AV+orig'[11]' {$ec}psc_AV+orig'[12]' 
 3dMean -prefix {$ec}Congpsc {$ec}psc_AV+orig'[20]' {$ec}psc_AV+orig'[21]' 
 3dMean -prefix {$ec}Targetpsc {$ec}psc_AV+orig'[29]' {$ec}psc_AV+orig'[30]'
```

Now, you can find the average percent signal change in the anatomical-functional ROI during each of the four conditions:

```
 3dROIstats -quiet  -mask  {$ec}_L_aud_parc+orig {$ec}McGpsc+orig
 3dROIstats -quiet  -mask  {$ec}_L_aud_parc+orig {$ec}InCpsc+orig
 3dROIstats -quiet  -mask  {$ec}_L_aud_parc+orig {$ec}Congpsc+orig
 3dROIstats -quiet  -mask  {$ec}_L_aud_parc+orig {$ec}Targetpsc+orig
```

## What hemodynamic response function (HRF) to use

The above examples use the 3dDeconvolve TENT functions to model the HRF.
A recent addition is the TENTzero function, which forces the HRF to finish and end at zero value. This is sensible.
Another option is CSPLINE and CSPLINEzero. These are useful if you don't have enough degrees of freedom to do a full TENT function fit to the HRF.
Here is a picture of the HRF from a subject's STS calculate with TENTzero(0,16,9) and CSPLINEzero(0,16,4); 4 is the minimum n for CSPLINE; if 9 is used, it gives the same results as TENT.
[![](../../attachments/ROIanalysis/BeauchampIRF.jpg)](../../attachments/ROIanalysis/BeauchampIRF.jpg)

## Obtaining trial-specific estimates of response amplitudes

Usually with ROI analyses we are only interested in obtaining one average HRF for a given ROI. This is an average of each time a given stimulus was presented in the scanner. Sometimes we may want to have an estimate for each individual trial. This can be useful for a connectivity analysis, MVPA, or getting more N for an individual subject.

Previously we have used 3dDeconvolve with -stim\_times\_IM (individual modulation) to create a bucket file with an estimate for each stimulus presentation for each voxel in the brain. You can then use 3dROIstats to average across a set of voxels. This method works, but can often have very high variance.

Another way to do this is to use 3dDeconvolve using -stim\_times\_IM for only one stimulus, while holding all other stimuli at -stim\_times. This makes sure that the regression analysis accounts for the presentation of other stimuli (otherwise they are considered "baseline", which can skew your results) while only obtaining estimates for a single stimulus of interest. To do this we have used the following command lines:

```
 3dDeconvolve -fout -tout -full_first -polort a -concat runs.txt -cbucket {$ec}v{$v}mr_bucket -x1D_uncensored {$ec}v{$v}.xmat.1D \
 -input {$ec}Albl+orig -num_stimts 16 -nfirst 0 -jobs 2 \
 -mask {$ec}maskAlbl+orig  \
 -stim_times_IM 1 Arel.txt 'BLOCK(2,1)' -stim_label 1 Arel \
 -stim_times_IM 2 Vrel.txt 'BLOCK(2,1)' -stim_label 2 Vrel \
 -stim_times_IM 3 TargetRel.txt 'BLOCK(2,1)' -stim_label 3 TargetRel \
 -stim_times_IM 4 McG.txt 'BLOCK(2,1)' -stim_label 4 McGurk \
 -stim_times_IM 5 NonMcG.txt 'BLOCK(2,1)' -stim_label 5 InC \
 -stim_times_IM 6 Cong.txt 'BLOCK(2,1)' -stim_label 6 Cong \
 -stim_times_IM 7 Target.txt 'BLOCK(2,1)' -stim_label 7 Target \
 -stim_times_IM 8 Ablock.txt 'BLOCK(20,1)' -stim_label 8 Ablock \
 -stim_times_IM 9 Vblock.txt 'BLOCK(20,1)' -stim_label 9 Vblock \
 -stim_times_IM 10 AVblock.txt 'BLOCK(20,1)' -stim_label 10 AVblock \
 -stim_file 11 {$ec}rall_vr_motion.1D'[0]' -stim_base 11 \
 -stim_file 12 {$ec}rall_vr_motion.1D'[1]' -stim_base 12 \
 -stim_file 13 {$ec}rall_vr_motion.1D'[2]' -stim_base 13 \
 -stim_file 14 {$ec}rall_vr_motion.1D'[3]' -stim_base 14 \
 -stim_file 15 {$ec}rall_vr_motion.1D'[4]' -stim_base 15 \
 -stim_file 16 {$ec}rall_vr_motion.1D'[5]' -stim_base 16 \
 -prefix {$ec}v{$v}mr
```

This is then followed by using 3dbucket to obtain the amplitudes for one select stimulus of interest, then using 3dROIstats to obtain an average of these estimates across a group of voxels (i.e. an ROI).

```
  3dbucket -prefix {$ec}McGbucket 'IEv{$v}mr_bucket+orig[208-257]'
  3dROIstats -quiet  -mask {$ec}_R_pSTS_parc2009_AudVis+orig {$ec}McGbucket+orig > {$ec}McG_bucket.1D
```

A better way however is to do this, however, is to obtain an trial-specific estimates for a one stimulus at a time. To do this, you could use the following command lines:

```
 3dDeconvolve -fout -tout -full_first -polort a -concat runs.txt -x1D {$ec}McG.xmat.1D \
 -input {$ec}Albl+orig -num_stimts 16 -nfirst 0 -jobs 2 \
 -mask {$ec}maskAlbl+orig  \
 -stim_times 1 Arel.txt 'BLOCK(2,1)' -stim_label 1 Arel \
 -stim_times 2 Vrel.txt 'BLOCK(2,1)' -stim_label 2 Vrel \
 -stim_times 3 TargetRel.txt 'BLOCK(2,1)' -stim_label 3 TargetRel \
 -stim_times_IM 4 McG.txt 'BLOCK(2,1)' -stim_label 4 McGurk \
 -stim_times 5 NonMcG.txt 'BLOCK(2,1)' -stim_label 5 InC \
 -stim_times 6 Cong.txt 'BLOCK(2,1)' -stim_label 6 Cong \
 -stim_times 7 Target.txt 'BLOCK(2,1)' -stim_label 7 Target \
 -stim_times 8 Ablock.txt 'BLOCK(20,1)' -stim_label 8 Ablock \
 -stim_times 9 Vblock.txt 'BLOCK(20,1)' -stim_label 9 Vblock \
 -stim_times 10 AVblock.txt 'BLOCK(20,1)' -stim_label 10 AVblock \
 -stim_file 11 {$ec}rall_vr_motion.1D'[0]' -stim_base 11 \
 -stim_file 12 {$ec}rall_vr_motion.1D'[1]' -stim_base 12 \
 -stim_file 13 {$ec}rall_vr_motion.1D'[2]' -stim_base 13 \
 -stim_file 14 {$ec}rall_vr_motion.1D'[3]' -stim_base 14 \
 -stim_file 15 {$ec}rall_vr_motion.1D'[4]' -stim_base 15 \
 -stim_file 16 {$ec}rall_vr_motion.1D'[5]' -stim_base 16 \
 -prefix {$ec}McG
```

You could then take the output file, {$ec}McG+orig, find the sub-briks that contain the beta-weight coefficients for your stimulus of interest (this can be found in the header file) and use 3dROIstats to obtain an averaged estimate for your ROI. This uses the LS-A method to estimate trial-specific responses.

```
 3dROIstats -quiet  -mask {$ec}_R_pSTS_parc2009_AudVis+orig '{$ec}McG+orig[10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108]' > {$ec}McG_LSA.1D
```

However, the best way to obtain trial-specific estimates is to using the resulting X-matrix as the input into 3dLSS:

```
 3dLSS -matrix {$ec}McG.xmat.1D \
 -input {$ec}Albl+orig -mask {$ec}maskAlbl+orig  \
 -save1D McG.LSS.1D -prefix {$ec}McGLSS
```

And then averaging those estimates across voxels in your ROI:

```
 3dROIstats -quiet  -mask {$ec}_R_pSTS_parc2009_AudVis+orig {$ec}McGLSS+orig > {$ec}McG_LSS.1D
```

To illustrate how this might change your results, the following graph shows three different ways to obtain stimulus estimates. The x-axis shows individual trials for the McGurk stimulus and the y-axis shows the response amplitude estimate in percent signal change (psc). In each case the results have been averaged across the same ROI mask. Method 1 is the result from using 3dDeconvolve with -stim\_times, which only gives you one stimulus estimate for every voxel. Methods 2 and 3 are the different ways of obtaining trial specific estimates. Method 2 shows the results from using the LS-A method and Method 3 shows the results from using the LS-S method, all as described above.

[![](../../attachments/ROIanalysis/Stimtimescomparison.jpg)](../../attachments/ROIanalysis/Stimtimescomparison.jpg)

While the average amplitude obtained from using LS-A or LS-S is very similar (with this example dataset, they were 0.2609 and 0.2605, respectively), using LS-S results in much smaller variance, which can be very helpful if you are trying to detect any changes in response amplitude within one subject (like a patient). This method would also be useful for a functional connectivity analysis.

## What if the FreeSurfer parcellation doesn't work

FreeSurfer generates a .stats file which contains the GM volume and surface area for each area in the brain.
Sometimes the FreeSurfer parcellation may fail, for instance if there is a lesion in the brain.
In this case, you can manually edit the parcellation file and then calculate the volume for each area (see subject IE for details).
The volumes calculate by this method are not as accurate because they don't take partial voluming into account.
Another possibility is to edit the aseg FS parcellation files, e.g. aseg.mgz and then run the
mri\_segstats
program. This will take partial voluming into account.
The more precise way to do this is to fill in the lesion in the wm.mgz file and then the surface should go outside the lesion.
Of course, that means that you'd have to run freesurfer again, which is slow. Make sure when you do, you use one of the -autorecon flags so that it doesn't just start over and overwrite your lesion mask. See [this page](https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all).
