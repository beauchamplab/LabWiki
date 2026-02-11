---
title: Unwarping
parent: Beauchamp
---
# Unwarping

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

As you've probably noticed if you've examined your epi (that is, echo planar imaging) data closely, the shape of the brain looks a little funny. This is because there is susceptibility near the tissue boundaries (like the sinuses), which causes some inhomogeneities in the magnetic field near them. This has two main results-- first, spins near these areas will dephase faster, resulting in signal dropout. Second, the variations in the magnetic field strength experienced by the spins will displace them on the image. There isn't really a way to fix the first problem\* (getting signal back), but there are a few methods for minimizing the effect of the second problem (geometric distortions) on your data. This can be really important to do if you're interested in precise anatomical locations of brain bits near the distortions. It can also be really important to do if you're doing some sort of precise masking, such as sampling from a volume to a surface. The strategies for doing this depend a bit on what data you have.

- I mean, not after you've acquired the data. You can do things to prevent it, mostly making your TE shorter.

# Nothing but an EPI and an anatomical

If these are the data you have, your best bet is to do a nonlinear alignment to the anatomical. (Also, if you tried to acquire a pair of blipup/blipdown data and the participant moved in between, consider this your plan B). Essentially, you're mapping the spatial contrast of the epi to the spatial contrast in the anatomical. So, if this is the route you're taking, you'll want to use images with the best spatial contrast you've got. If you collect without dummy volumes (that is, if you keep the data that's collected in the first few TRs of your functional run, before the magnetization has stabilized), those first few runs will have higher signal, and better spatial contrast. If you're using the CMRR sequence, that SBref will fit the bill. You can use these to compute the nonlinear alignment. Otherwise, you could take an average of all the (motion-corrected) volumes, and use that as a single volume to align. Just make sure that you motion correct to \*this\* volume later.

This procedure would look something like this (unabashedly plagiarized from the AFNI help page for 3dQWarp.)

```
** For aligning EPI to T1, the '-lpc' option can be used; my advice
   would be to do something like the following:
     3dSkullStrip -input SUBJ_anat+orig -prefix SUBJ_anatSS
     3dbucket -prefix SUBJ_epiz SUBJ_epi+orig'[0]'
     align_epi_anat.py -anat SUBJ_anat+orig                            \
                       -epi SUBJ_epiz+orig -epi_base 0 -partial_axial  \
                       -epi2anat -master_epi SUBJ_anat+orig            \
                       -big_move
     3dQwarp -source SUBJ_anatSS+orig.HEAD   \
             -base   SUBJ_epiz_al+orig       \
             -prefix SUBJ_anatSSQ            \
             -lpc -verb -iwarp -blur 0 3
     3dNwarpApply -nwarp  SUBJ_anatSSQ_WARPINV+orig  \
                  -source SUBJ_epiz_al+orig          \
                  -prefix SUBJ_epiz_alQ
   * Zeroth, the T1 is prepared by skull stripping and the EPI is prepared
     by extracting just the 0th sub-brick for registration purposes.
   * First, the EPI is aligned to the T1 using the affine 3dAllineate, and
     at the same time resampled to the T1 grid (via align_epi_anat.py).
   * Second, it is nonlinearly aligned ONLY using the global warping -- it is
     futile to try to align such dissimilar image types precisely.
   * The EPI is used as the base in 3dQwarp so that it provides the weighting,
     and so partial brain coverage (as long as it covers MOST of the brain)
     should not cause a problem (we hope).
   * Third, 3dNwarpApply is used to take the inverse warp from 3dQwarp to
     transform the EPI to the T1 space, since 3dQwarp transformed the T1 to
     EPI space. This inverse warp was output by 3dQwarp using '-iwarp'.
   * Someday, this procedure may be incorporated into align_epi_anat.py :-)
** It is vitally important to visually look at the results of this process! **
```

I would note that these instructions really only tell you how to get one volume of your fMRI unwarped. But importantly, it's giving you that SUBJ\_anatSSQ\_WARPINV+orig file, which is what the un-distortion should look like. To apply to the rest of your data, you would motion correct and align the epi run to the anatomical, then run that last line (3dNwarpApply) again, but with the source being your epi run. You could apply all three of these transformations (motion correction, alignment, and distortion correction) at the same time (along with the TLRC transform, if you're doing that, too), but I'm not seeing a graceful way to add that to an afni\_proc.py command. I'm not quite sure what to recommend here, because it would seem to depend a bit on what other processing steps you're running. You could do the motion correction, alignment, and distortion correction outside of afni proc and then give this to an afni proc to continue with the rest of your analysis (not compatible with slice timing correction or ricor in the afni proc script, because now you've changed up your slices). You could also manually edit the afni proc script, but that's generally not recommended.

# An EPI and a fieldmap

Sometimes, people measure the fieldmap directly, generally by collecting an image with different TEs that keeps both phase and magnitude, and watching the speed of the phase progress with TE. If that's the case, you can compute how much signal loss and distortion should have arisen, and compensate accordingly in your alignment to the anatomical. FSL has a tool called [FUGUE](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FUGUE) that handles this.

# Two EPIs with different phase encode directions

The susceptibility-induced distortions will depend on the phase encode direction of your scans. An approach that's becoming more common is to collect two scans with phase encode directions going to opposite directions (such as R>>L and L>>R or A>>P and P>>A). This is also called "blip up/blip down" or the like. This will give you two distorted images (which sounds worse, actually). Since they're distorted equally wrong but in opposite directions, the half-way point is undistorted (ideally). It's also worth noting that this is a much faster acquisition scheme than collecting a full fieldmap. If you're collecting multiple task runs, you could collect every other one with a phase encode flip, and you've added no time to your acquisition. Alternatively, you could collect a very short flipped acquisition in between runs. Even if you only have one run, you only need a volume (or maybe two or three, for averaging) to do the calculation. That means that it only takes a few TRs of extra acquisition (if any) to do this correction.

This approach can be used with both gradient echo or spin echo EPI (for instance, fMRI and DTI, respectively).

## Some considerations for the acquisition

1. The two images must be matched for the kinds of things that effect distortions. It's easiest to set this up by picking the first one, copying it, and then changing the phase encode direction. BUT...
   1. If you copy references between these later, sometimes Siemens will flip the phase encode not from A>>P to P>>A... but from A>>P to R>>L. Which is not really that helpful. In that case, you may have to use the "..." button next to "Phase Enc. Dir." and manually enter 180 degrees. BUT...
   2. If you're acquiring obliquely (for instance, if you are using AAscout and the autoalign feature), 180 degrees from A>>P isn't 180 degrees from your first acquisition. You have to calculate this out explicitly. I recommend grabbing the handy dandy calculator function on the nearest smart phone. I know, I know. You're a competent professional and can add and subtract numbers in your head. But, angles greater than 180 aren't an option, so if your angle started out negative you need to add 180 and if it was positive you need to subtract, and it ends up being a simultaneous working memory and number manipulation task that is error prone enough that you should just use the calculator. Come on, you and I both know you were going to play games on it during the session anyway. ;-)
   3. For certain base sequences, notably the sequences distributed by CMRR and MGH for multiband, there's a ultra-secret super-special way to do this. You \*leave\* the phase encode direction as it was, and in the Sequence->Special card, you toggle the checkbox for a phase encode flip (sometimes labeled something like "Reverse RO/PE polarity"). This resolves the issue of calculating the angle on the fly, but does mean that you have to keep track of both the listed phase encode direction and the "is it flipped?" toggle.
2. It's important that the tissues that are causing distortions stay in the same place between these two scans. So...
   1. They should be acquired back-to-back if at all possible, and
   2. It's often best to un-check "wait for user to start" in the "execution" section of the scan. Since, presumably, there should be no additional shimming or adjustments needed (since the scans are nearly identical), this will mean that the scanner flows right from the end of one into the beginning of the other, and there is as little chance as possible for your participant to decide that the scan is over and they are now free to adjust themselves wildly.
   3. If you're reading this after you've already collected your data, then at least pick the best pair available to you. So, for instance, if you've collected run01\_AP, then run00\_PA, then run02\_AP; then you have two choices (the end of run01\_AP and the beginning of run02\_AP) to compare to the PA set. Pick the one with the least motion between them.
3. You should be able to see the change in phase encode direction at the scanner, and you should check just to be sure.
   1. First, when you set them up and (on a Siemens system) you've got the yellow box on top of the localizer's picture of the brain, there's an arrow. This indicates the phase encode direction. If you watch the box and arrow while you're setting up the slice prescription, you should see that the box does not change, but the arrow does. This is a good sign.
   2. Then, after they're acquired, you should be able to view them and see parts of the brain (normally the 'devil's horns' at the front are an easy target) switch the direction of their distortion. One of the should look like the image is smeared up, and the next should look like the image is smeared down (or down, then up... or left, then right... you get the picture.)
   3. While you're checking this, go ahead and make sure the subject didn't move their head in between. Remember, the algorithm is restricting the distortion to within plane, so if there's also a movement shift, it's hard to be sure what the computed distortion correction will be... but it's probably not gonna be right.

Now that you've got the images, there are a number of tools that are able to compute the unwarping.

## AFNI: afni\_proc.py

When to use: I'm doing task or rest fMRI, and I was already planning to use afni\_proc.py. I've acquired one (and only one) blip reversed set, which is short and contains no other useful data.

How to use:
Minimally, you can add the -blip\_reverse\_dset flag and give afni\_proc your blip\_down dataset. Note, if this is all the information you give it, it will assume that it's comparing this blipdown file to the first few volumes of run 1. This only makes sense if you ran the blidown FIRST. If that's not the case for you, you probably want to give it a -blip\_forward\_dset file as well, which would be a blip-up acquisition next to (in time) your blip-down. So, as an example, let's say you acquired one 450-volume AP task run, followed by a 10-volume PA run with no task data. Then you would set up your afni\_proc script with whatever other choices you would have made without the PA run, along with

```
 -blip_reverse_dset Task_PA.nii -blip_forward_dset Task_run01_AP.nii'[440..449]'
```

or something like that.

The nice part about using this approach is that (1) if you were already doing afni\_proc, this is pretty painless; and (2) because it's part of an afni\_proc pipeline, afni will make a series of reasonable decisions about when things happen. So, for instance, de-spiking will happen before this distortion correction, but TLRC-ing will happen after.

## AFNI: unWarp\_epi.py

When to use: I'm doing task or rest fMRI. I've done something fancy, such as (1) collected some runs AP and some PA, (2) collected multiple blip-down sets throughout the protocol, (3) instead of collecting your gradient-echo runs with the phase encode flip, you've got a pair of spin-echo runs, or (4) some other odd iteration such that you haven't met the assumptions of afni\_proc.py. Alternatively, if you plan to use AFNI for just this bit, and then transfer to another imaging toolkit.

How to use:

AFNI has a tool called [unWarpEPI.py](https://afni.nimh.nih.gov/pub/dist/doc/program_help/unWarpEPI.py.html). Here's an example of how to use it, assuming you've got a 450-volume AP run, and a 10-volume PA run:

```
 unWarpEPI.py -f rfMRI_REST_AP_8+orig'[440..449]' -r rfMRI_REST_PA_9+orig -d 'rfMRI_REST_AP_8' -a T1+orig -s unwarped_data
```

In this example, the warp is calculated from the last 10 volumes of the AP run and (all) 10 volumes of the PA run. The calculated warp will be applied to all of the AP run. The anatomical (T1) will be used to help it along. Note that it's assuming that your runs are in AFNI's .BRIK and .HEAD format with +orig in the filename. If you have .nii's instead, you need to convert them using something like 3dcopy.

For another example, let's say you've got two 450-volume runs, one that AP and one that's PA. You would now do...

```
 unWarpEPI.py -f rfMRI_REST_AP_8+orig'[440..449]' -r rfMRI_REST_PA_9+orig'[0..9]'      -d 'rfMRI_REST_AP_8' -a T1+orig -s unwarped_data_AP
 unWarpEPI.py -f rfMRI_REST_PA_9+orig'[0..9]'     -r  rfMRI_REST_AP_8+orig'[440..449]' -d 'rfMRI_REST_PA_9' -a T1+orig -s unwarped_data_PA
```

Hopefully, the first line makes sense... it's just like the example above, except now we want to specify that we're only using the first part of the PA run. But this time, you also want to correct your PA run, so you'll do the same thing all over again, with everybody switching the parts they play. This isn't particularly computationally efficient, I'll admit. I suppose you could use 3dNWarpApply with some sort of inverse as well. But this is the example I'm showing you.

To switch it up even more, let's say I've got 4 runs, each 100 volumes. Run01\_AP.nii, Run02\_AP.nii, Run\_03\_PA.nii, Run\_04\_PA.nii. I could...

```
 3dTcat -prefix AP_runs+orig Run01_AP.nii Run02_AP.nii
 3dTcat -prefix PA_runs+orig Run03_PA.nii Run04_PA.nii
 3dvolreg -prefix vr.AP+orig -base 199 AP_runs+orig
 3dvolreg -prefix vr.PA+orig -base 0 PA_runs+orig
 3dTstat -mean -prefix m.vr.AP+orig vr.AP+orig
 3dTstat -mean -prefix m.vr.PA+orig vr.PA+orig
 unWarpEPI.py -f m.vr.AP+orig -r m.vr.PA+orig -d 'vr.AP' -a T1+orig -s unwarped_data_AP
 unWarpEPI.py -f m.vr.PA+orig -r m.vr.AP+orig -d 'vr.PA' -a T1+orig -s unwarped_data_AP
```

NOTE: unWarp\_epi doesn't seem to like .nii volumes. It's assuming everything you've got is in AFNI's .BRIK and .HEAD files. So, if your data is in .nii, you may have to start with

```
 3dcopy mydata.nii mydata+orig
```

## FSL: TOPUP followed by either applytopup or eddy

When to use: I'm doing DTI, and I've got a dataset of blip-down b0's, either because that's all I acquired, or because I'm willing to extract all the b0 volumes from dataset with diffusion encoded volumes.

How to use: Start by running TOPUP.

### FSL: TOPUP

To start with, you're going to need some information from your acquisition files. You can get these from off the scanner, from the protocol printout, or from the .json files (if you used dcm2niix or the like), or from the dicom headers.

1. The echo spacing. This is found in the "sequence" section of the protocol card on the scanner (normally part 1)and protocol printout; or under "EffectiveEchoSpacing" in the .json.
2. The EPI factor. This is found in the "sequence" section of the protocol card on the scanner (normally part 2)and protocol printout; or under "PhaseEncodingSteps" in the .json. It's often the same as the base resolution.
3. Phase encoding direction. In most cases, this is A>>P or P>>A, but R>>L and L>>R is sometimes used and I>>S and S>>I is possible but pretty rare.

More info here: <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy/Faq#How_do_I_know_what_to_put_into_my_--acqp_file>

Using this information, you're going to make a new text file. If your phase encoding direction is A>>P and P>>A, then the first 3 columns will be

```
  0 1 0 
  0 -1 0
```

If it's R>>L and L>>R, it would be

```
 1 0 0
 -1 0 0
```

Now, the fourth column is the harder part. You're going to calculate the time between the middle of the first echo and the middle of the last one. This is ((EPI factor)-1) \* Echo spacing in seconds. Your echo spacing is in ms on the scanner and the pdf, so you need a factor of 1/1000 in there. If your echo spacing was .54ms (or, .00054 seconds in the .json) and your EPI factor was 116, this would come out to 0.54\*0.001 \* (116-1) = 0.0621. So, our file (with AP/PA) now reads:

```
 0 1 0 .0621
 0 -1 0 .0621
```

I generally call this file acqp.txt (which stands for acquisition parameters), but the name doesn't matter.

Next up, we're going to put together a file of the blip up and blip down volumes. These almost certainly came from two different acquisitions, so you'll have to stitch them together yourself. There may also be some additional manipulations here, such as grabbing the b0 volumes in a DTI dataset, or taking the first/last volumes of a longer fMRI run that are nearest to the blipdown set. This process may look like 3dTcat with a subbrik selector, e.g.

```
 3dTcat -prefix b0s_only.nii all_my_dti.nii'[0,1,17,33,49,65,81]'
```

or fslsplit-ing the full run into a separate folder and selecting the ones you want, e.g.

```
 fslsplit my_run.nii ./f -t
 fslmerge -t just_the_ones_I_want.nii f0000.nii f0001.nii f0017.nii f0033.nii f0049.nii f0065.nii f0081.nii
```

Once that's done, you can stitch the blipup and blipdown volumes you want into a single 4-D dataset:

```
 fslmerge -t blipset.nii  blipup.nii blipdown.nii
```

Now, we can call topup

```
 topup --imain=blipset --datain=acqp.txt --config=b02b0.cnf --fout=fieldmap --iout=blipset_unwarped
```

When this finishes, it's a good idea to display blipset\_unwarped on top of your T1. This will give you a good idea as to whether this worked, or something funky is going on.

### FSL: EDDY

From here, you can take this output and use eddy to move along with your DTI processing. And example is as follows:

```
 eddy --imain=AP.nii --mask=AP_brain_mask.nii.gz --acqp=acqp.txt --index=index.txt --bvecs=AP.bvec --bvals=AP.bval --topup=blipset_unwarped --out=eddy_AP
```

The index.txt is a text file that tells eddy which of the lines of acqp.txt each volume of imain belongs to. Often, what I want this to look like can be generated from something like this:

```
 for (( i=1; i<=99; i++ )); do indx="$indx 1"; done; echo $indx > index.txt
```

Where in this case, the dataset was 99 volumes long, and all of them were acquired like the first volume of blipset.nii

### FSL: APPLYTOPUP

FSL has already written a useful guide for this, and I will simply link it here.
<https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup/ExampleTopupFollowedByApplytopup>

## FSL: TOPUP and FUGUE/FEAT

When to use: I'm doing task or rest fMRI, and I was already planning to use FEAT, or otherwise just prefer to work in FSL-world.

How to use: Start with the process for running topup, as described above.

Now, we're going to make the output fieldmap suitable for use with fugue. In the example above, my output files were named "fieldmap." That's what we're working with now. Take the fieldmap, and convert to radians.

```
 fslmaths fieldmap -mul 6.28 fieldmap_rads
```

Now, take the distortion-corrected file, calculate the magnitude and a mask.

```
 fslmaths blipset_unwarped -Tmean fieldmap_mag
 bet2 fieldmap_mag fieldmap_mag_brain
```

The naming convention from that last line actually matters. The name of the files for magnitude and mask of the magnitude file need to differ only by the "\_brain" suffix.

Now, we are going to look up a few more parameters about our scans, before turning to the FEAT gui.

1. We need the echo spacing of the run we want to correct. It should probably be the same as what you found to calculate the number in topup
2. We need the echo time (TE) of the scan we want to correct. This is on the "routine" page on the scanner, under "EchoTime" in the .json (in seconds), and will probably show up with a variety of other information extraction tools (mri\_info, fslinfo, 3dinfo, etc).

In the FEAT gui window, under Pre-stats, there is a checkbox for B0 unwarping. This is where FEAT will implement FUGUE.

1. Where it asks for "Fieldmap" input fieldmap\_rads
2. where it asks for "Fieldmap mag" input fieldmap\_map\_brain
3. effective EPI echo spacing should match the scanner protocol (or the .json file value \* 1000)
4. EPI TE (ms) should match the scanner protocol (or the .json file value \* 1000)
5. unwarp direction depends on (1) the direction and (2) which one you specified as positive in the acqp.txt file. In the examples as I've written it, I would use -y.
6. % signal loss threshold. 10% has been fine for me, but I haven't played with this very much.

One of the issues I have found as I play around with this is that sometimes, the distortion correction itself isn't the problem, but rather, it's the registration to the T1. You can tell if this is an issue for your own data by loading the report\_unwarp.html file into your browser and checking out the quality of the alignment. My fix for this was to use the SBRef (that is, single-band reference) files that are output with the CMRR scans for most people. I ran this through a quick brain extraction, and gave that to FEAT under "Select Alternate reference image(s)". If this image isn't available to you, the next thing I'd try would be to motion-correct the fMRI run, then take the mean image, then run it through BET. This would give you a very similar image. The nice thing about the SBRef is that it's kept as the first image in the series (without dummy scans), so the spatial contrast is a little crisper.

## TORTOISE: DRBUDDI

When to use: I'm doing DTI and have acquired two complete (symmetric) runs of diffusion-encoded data, one with each phase encode direction. Also, I'm a patient person who doesn't get frustrated easily.

How to use:
See instructions here: <UsingTORTOISE.md>
