# MVPA Notes

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
| [Brain picture](../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](index.md "Beauchamp")
- [Lab Members](Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](Lab_Alums.md)
- [Projects](Projects.md)
- [Publications](Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](Subjects.md "Beauchamp:Subjects")

- [Software Installation](Software_Installation.md)
- [Ordering](Ordering.md)
- [MRI Data Analysis](MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](TMS.md "Beauchamp:TMS")

To analyse data, we use the 3dsvm program. Data from some runs is used for training; data from other runs is used for testing. This process can be automated.

To see what brain areas are important for making the classification, we can look at the weight mask output by

```
 3dsvm -bucket
```

For this, we can't just do all runs at once since we don't care about getting an accuracy %.

3dsvm needs brain volumes to train and test on. For block designs, this would just be the volumes collected during each task (possibly eliminating the first few as the MR signal increases).
For event-related designs, this can be approximated by just picking the brain volume collected 2 TRs (4 seconds) after the stimulus was presented. Or, it can be calculated using STIM\_TIMES\_IM in 3dDeconvolve.
It is not clear that one way gives better results or not.

For STIM\_TIMES\_IM, the estimates of the response to trials that are very late in a run will be wacky, so it is best to delete these from the text file first.

```
 foreach f (*txt)
 cp $f newreg/trunc_{$f}
 end
```

Manually get rid of anything in last 10 seconds of each run.
We only need to use IM for events that we are trying to classify; for other trial types (e.g. controls) there is no need.
Sample command line:

```
 3dDeconvolve -fout -tout -full_first -polort a -concat runs.txt \
 -input {$ec}Albl+orig -num_stimts 15 -nfirst 0 -jobs 2 \
 -mask {$ec}maskAlbl+orig  \
 -stim_times_IM 1 newreg/trunc_VTv1T2.txt 'BLOCK(2,1)'  -stim_label 1 TacD2 \
 -stim_times_IM 2 newreg/trunc_VTv1T5.txt 'BLOCK(2,1)'  -stim_label 2 TacD5 \
 -stim_times_IM 3 newreg/trunc_VTv1V2.txt 'BLOCK(2,1)'  -stim_label 3 VisD2 \
 -stim_times_IM 4 newreg/trunc_VTv1V5.txt 'BLOCK(2,1)'  -stim_label 4 VisD5 \
 -stim_times_IM 5 newreg/trunc_VTv1TV2.txt 'BLOCK(2,1)'  -stim_label 5 TacVisD2 \
 -stim_times_IM 6 newreg/trunc_VTv1TV5.txt 'BLOCK(2,1)'  -stim_label 6 TacVisD5 \
 -stim_times 7 VTv1CT.txt 'BLOCK(2,1)'  -stim_label 7 TacCtrl \
 -stim_times 8 VTv1CV.txt 'BLOCK(2,1)'  -stim_label 8 VisCtrl \
 -stim_times 9 VTv1CVT.txt 'BLOCK(2,1)'  -stim_label 9 TacVisCtrl \
 -stim_file 10 {$ec}vr.1D'[0]'  -stim_base 10 \
 -stim_file 11 {$ec}vr.1D'[1]'  -stim_base 11 \
 -stim_file 12 {$ec}vr.1D'[2]'  -stim_base 12 \
 -stim_file 13 {$ec}vr.1D'[3]'  -stim_base 13 \
 -stim_file 14 {$ec}vr.1D'[4]'  -stim_base 14 \
 -stim_file 15 {$ec}vr.1D'[5]'  -stim_base 15 \
 -prefix {$ec}v{$v}mr
```

Next, we chop this up into separate files for each event type; it is easiest if there is the same number of events of each type.

```
 set f = EVv2mr+orig.HEAD
 3dinfo -verb $f | grep Coef
```

```
 3dbucket -overwrite -prefix {$ec}_T2 -fbuc $f'[1..119(2)]'
 3dbucket -overwrite -prefix {$ec}_T5 -fbuc $f'[122..240(2)]'
 3dbucket -overwrite -prefix {$ec}_V2 -fbuc $f'[243..357(2)]'
 3dbucket -overwrite -prefix {$ec}_V5 -fbuc $f'[360..476(2)]'
 3dbucket -overwrite -prefix {$ec}_TV2 -fbuc $f'[479..597(2)]'
 3dbucket -overwrite -prefix {$ec}_TV5 -fbuc $f'[600..718(2)]'
```

To avoid having to select every other BRIK, we can use the -cbucket option in 3dDeconvolve to create a file with only the coefficients (no statistics).

After creating the coefficient files, we can further subdivide them for training/testing, e.g. into even and odd trials.

```
 3dinfo EV_*HEAD | grep "pixel ="
```

++ 3dinfo: AFNI version=AFNI\_2008\_07\_18\_1710 (May 21 2009) [64-bit]
Number of values stored at each pixel = 60
Number of values stored at each pixel = 60
Number of values stored at each pixel = 60
Number of values stored at each pixel = 60
Number of values stored at each pixel = 58
Number of values stored at each pixel = 59

```
 foreach f (EV_*HEAD)
  3dbucket -overwrite -prefix even_{$f} -fbuc $f'[0..56(2)]'
  3dbucket -overwrite -prefix odd_{$f} -fbuc $f'[1..57(2)]'
 end
```

Since the classification is easiest for pairwise comparisons, we pair the BRIKs.
3dbucket -prefix even\_T2\_T5 even\_EV\_T2+orig.HEAD+orig.HEAD even\_EV\_T5+orig.HEAD+orig.HEAD
3dbucket -prefix even\_V2\_V5 even\_EV\_V2+orig.HEAD+orig.HEAD even\_EV\_V5+orig.HEAD+orig.HEAD
3dbucket -prefix even\_TV2\_TV5 even\_EV\_TV2+orig.HEAD+orig.HEAD even\_EV\_TV5+orig.HEAD+orig.HEAD
3dbucket -prefix odd\_T2\_T5 odd\_EV\_T2+orig.HEAD+orig.HEAD odd\_EV\_T5+orig.HEAD+orig.HEAD
3dbucket -prefix odd\_V2\_V5 odd\_EV\_V2+orig.HEAD+orig.HEAD odd\_EV\_V5+orig.HEAD+orig.HEAD
3dbucket -prefix odd\_TV2\_TV5 odd\_EV\_TV2+orig.HEAD+orig.HEAD odd\_EV\_TV5+orig.HEAD+orig.HEAD

3dsvm requires the data to have a time axis, so add this back in
3drefit -TR 2000 even\* odd\*

Create the train/test text files depending on how many of each event there is:

```
 1deval -num 29 -expr '0' > {$ec}_svmv1_train.1D
 1deval -num 29 -expr '1' >> {$ec}_svmv1_train.1D
```

Classification usually works best if given some sort of mask, typically all brain voxels, or only brain voxels showing some activation.

```
 set v = 1
 set f = {$ec}_svmv{$v}_results.txt
 rm $f 
 foreach ds (T2_T5 V2_V5 TV2_TV5)
 rm *svmv{$v}*model*
 set train = even
 set test = odd
 3dsvm -overwrite -trainvol  {$train}_{$ds}+orig \
 -trainlabels {$ec}_svmv1_train.1D \
 -mask  {$ec}maskv1+orig  \
 -model {$ec}_svmv{$v}_{$train}_model
 echo Results from training on {$train} trials testing on {$test} trials  >>  $f
 3dsvm -overwrite  -nodetrend -classout \
 -testvol {$test}_{$ds}+orig \
 -model {$ec}_svmv{$v}_{$train}_model+orig \
 -testlabels  {$ec}_svmv1_train.1D  \
 -predictions {$ec}_svmv{$v}_predict >> $f
set train = odd
 set test = even
rm *svmv{$v}*model*
 3dsvm -overwrite -trainvol  {$train}_{$ds}+orig \
 -trainlabels {$ec}_svmv1_train.1D \
 -mask  EVmaskAlbl+orig \
 -model {$ec}_svmv{$v}_{$train}_model
 echo Results from training on {$train} trials testing on {$test} trials  >>  $f
 3dsvm -overwrite  -nodetrend -classout \
 -testvol {$test}_{$ds}+orig \
 -model {$ec}_svmv{$v}_{$train}_model+orig \
 -testlabels  {$ec}_svmv1_train.1D  \
 -predictions {$ec}_svmv{$v}_predict >> $f
 end
```

```
 cat $f | grep -i "accuracy"
 open -e $f
```

EVmaskAlbl+orig
Accuracy on test set: 55.17% (32 correct, 26 incorrect, 58 total)
Accuracy on test set: 58.62% (34 correct, 24 incorrect, 58 total)
Accuracy on test set: 43.10% (25 correct, 33 incorrect, 58 total)
Accuracy on test set: 48.28% (28 correct, 30 incorrect, 58 total)
Accuracy on test set: 53.45% (31 correct, 27 incorrect, 58 total)
Accuracy on test set: 48.28% (28 correct, 30 incorrect, 58 total)

3dcalc -overwrite -datum byte -prefix {$ec}maskv1 -a0 {$ec}v1mr+orig -expr "step(a-3.2)\*step(3+z)"
$ec}maskv1+orig
Accuracy on test set: 53.45% (31 correct, 27 incorrect, 58 total)
Accuracy on test set: 58.62% (34 correct, 24 incorrect, 58 total)
Accuracy on test set: 44.83% (26 correct, 32 incorrect, 58 total)
Accuracy on test set: 48.28% (28 correct, 30 incorrect, 58 total)
Accuracy on test set: 62.07% (36 correct, 22 incorrect, 58 total)
Accuracy on test set: 48.28% (28 correct, 30 incorrect, 58 total)
