# iEEG EMU MATLAB SOP

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

# SOP for running MATLAB in EMU(Jan2022)

[Click here for detailed steps in PDF format.](../../attachments/iEEG_EMU_MATLAB_SOP/NoisySpeechMATLAB_SOP_Beauchamplab.pdf "NoisySpeechMATLAB SOP Beauchamplab.pdf")

The noisy speech project (EMU\_NoisyWords) has 6 cohorts/folders in the MATLAB folder. The first patient will be presented with stimuli sequences in cohort1 by using the MATLAB code in the same folder. The second patient will be tested using the cohort2 folder, following the order, until the 6th patient gets the cohort6 folder, and then we will re-start from cohort1 for the 7th patient, for another round of the test.

Take the first patient for example, we will use the codes in the ‘cohort1’ folder.

Inside this folder there are 5 individual MATLAB codes representing 5 blocks/runs for this patient. For each patient, we will try to run all five blocks/runs.

However, the patient has the right to stop participating at any stage of the testing, and we need to make sure that the patient is aware of his/her right.

Each block/run will take 3-5min. You need to run them individually, by typing ‘run1’ ‘run2’ ‘run3’ ‘run4’ ‘run5’ in the command window (one at a time, of course)

```
 Important! Before you start Matlab, please make sure that you have the following three folders under the same directory:
```

folder #1. cohort (or the corresponding cohort for that subject);

folder #2. results (this is where MATLAB writes out the presentation list and time stamps);

folder #3. stimuli (this is the source of videos that MATLAB will source from);

```
 Here is how we run the MATLAB code to get the movies show up in a certain sequence on the stimuli screen:
```

1. Open MATLAB inside the ‘UPenn\_EMUmatlab\_codes/-8dB/cohort1’ folder;

2. Make sure to change MATLAB current working directory to ‘UPenn\_EMUmatlab\_codes/-8dB/cohort1’’;

3. In the ‘Command Window’, type in: run1
(This should start the stimuli. Press key ‘5’ allow you to get to the next video within the run);

4. There are about 50 videos in each run, after all 50 videos finished, MATLAB will opt out, and you can start the next run (by typing run2, etc.);
