# Old Protocols

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
| [Brain picture](../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](index.md "Beauchamp")
- [Lab Members](Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](Lab_Alums.md "Beauchamp:Lab Alums")
- [Projects](Projects.md "Beauchamp:Projects")
- [Publications](Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](Subjects.md "Beauchamp:Subjects")

- [Software Installation](Software_Installation.md "Beauchamp:Software Installation")
- [Ordering](Ordering.md "Beauchamp:Ordering")
- [MRI Data Analysis](MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](TMS.md "Beauchamp:TMS")

[Back to current protocol](Electrophysiology.md "Beauchamp:Electrophysiology")

## July Subjects Plan

*NOTE: These experiments were not completed due to technical difficulties with the new data acquisition software and hardware.*  
  
7/7/2008 SETUP   
1. Identify potential electrodes with combined fMRI/CT  
2. Create log file on log computer  
3. Identify which channels have been assigned to set A and B  
4. Record resting activity to make sure system is working  
  
**Microelectrode array experiments**   
If the new electrodes are ready, it will be a top priority to investigate their properties. A good start will be to compare small electrode LFPs with nearby big electrode LFPs.  
  
**A. Recording:**

1) Are small electrodes more selective than big electrodes?
e.g. if an electrode likes faces, does a small electrode respond to fewer faces than a big electrode?

2) Is response amplitude/latency to a preferred stimulus any different?   
Probably not, but we may have to adjust the pre-amp or amplifier settings.

3) Receptive Field Size   
do small electrodes have smaller RFs than big electrodes?

4) Gamma oscillation   
Are oscillations in the gamma band more correlated among nearby electrodes than far electrodes?

**B. Stimulation**   
If would be really interesting to compare perception thresholds. We might predict thresholds would be lower with small electrodes because of high current density.   
If the RFs are more selective (#1 above) then we might evoke percept with a small electrodes (because we are stimulating neurons with similar selectivity) where we could not with a big electrode.

**Regular electrode experiments**  
**0) Stimulate the big electrodes overlying visually responsive/identified areas.**
1) [General Selectivity](Selectivity.md "Beauchamp:Selectivity") – 10 minutes

:   • 80 stimuli, 20 blocks
:   • One-back task (patient reports repetitions of images)

*--Identify selective electrodes*
*--Choose selective category*
**2) ["Stop-sign" Repeat Adaptation](Selectivity.md "Beauchamp:Selectivity") – 10 minutes**

:   • 20 selective stimuli, 20 nonselective stimuli, 20 blocks
:   • Stop-sign task (patient reports stop-signs)
:   • Need to code a modified version of the current Selectivity plugin to satisfy these conditions:   

    :   1. the patient is supposed to press the button after stop-signs instead of after repeats
    :   2. Selective stimuli are directly repeated every 8-12 images
    :   3. The stimulus preceding the repeat is always a nonselective stimulus

**3) ["One-back" Repeat Adaptation](Adaptation_and_CP.md) – 10 minutes**

:   • 20 stims from selective category, 5 stims from each nonselective category
:   • One-back task
:   • 2 Hz presentation rate
:   • Get enough trials such that we can measure choice probability
:   • Need the plugin to be modified such that:   

    :   1. Selective stimuli are directly repeated every 8-12 images
    :   2. The stimulus preceding the repeat is always a nonselective stimulus

**4) ["One-back" Cross Adaptation](Adaptation_and_CP.md) – 10 minutes**

:   • 20 stims from selective category, 5 stims from each nonselective category
:   • Altered one-back task - subject is told to respond to two selective-category stimuli in a row

**5) [Multiple-repetitions adaptation](Adaptation.md "Beauchamp:Adaptation") - 5 minutes**

:   • 20 selective stimuli, 20 nonselective stimuli, 2 Hz presentation, patient is told to press button when he/she sees the stopsign.
:   • 8 nonselective stimuli (including stop-sign), 8 presentations of the same selective stimulus, 8 nonselective stimuli (w/ stopsign), 8 different selective stimuli.

**6) ["Stop-Sign" Adaptation](Adaptation.md "Beauchamp:Adaptation") – 20 minutes**

:   • Adapting stimuli A and B
:   • 20 blocks -> 20 direct repeats
:   • 2 Hz presentation rate
:   • 8-12 intervening stimuli

## May 2008 Subject AC Protocol

**[Setup](Setup_Apparatus.md "Beauchamp:Setup Apparatus")**  
• Identify at least 16 electrodes of interest using the combined fMRI functional map and CAT scan.  
[Images here]   
• Create log file AC[birthday].doc on log computer  
• Identify which channels ITC has assigned electrodes set A and B to  
• Record resting activity to make sure system is working  
  
**Day 1 Experiment Lineup (5/1/08)**  
**1) [General Selectivity](Selectivity.md "Beauchamp:Selectivity") – 5 minutes**

:   • 80 stimuli, 20 blocks
:   • One-back task

*--Identify selective electrodes*
*--Choose selective category*

**2) ["One-Back" Selectivity](Selectivity.md "Beauchamp:Selectivity") – 5 minutes**

:   • 20 stims from selective category, 5 stims from each nonselective category
:   • One-back task

**3) [Receptive Field Mapping](Receptive_Field_Mapping.md "Beauchamp:Receptive Field Mapping") with preferred stimulus – 10 minutes**

:   • Homogenized stimuli are 400x400 pixels, and are shown at 25 degrees of the visual field in selectivity plugin. We want the stimulus to be large enough to recogize whilst small enough such that we can draw a high-resolution receptive field map and compare it to RFs from other brain areas. As a reference, the color paper's RF mapping used a colored square that was 1/11 of the screen's width. We did a run with RG that was -10 to 10 azimuth and elevation in spatial extent, with 11 x 11 locations, and 5 x 5 degree stimuli. Let's use this as our standard.

**3b) [Receptive Field Mapping](Receptive_Field_Mapping.md "Beauchamp:Receptive Field Mapping") with other category's stimulus - 15 minutes**

:   • Choose another preferred stimulus, if possible from a different category, and map the receptive field.
:   • Prediction: if a different category, RF may be different (more foveal for faces, more peripheral for houses)

*--Choose adapting stimuli A and B: two highly responsive stimuli*
*--Choose 15 intervening stimuli - from non-test categories*
**4) [Direct-Repeat Adaptation](Adaptation.md "Beauchamp:Adaptation") – 18 minutes**

:   • Adapting stimulus A
:   • 20 blocks -> 20 direct repeats

**5) [Direct-Repeat Adaptation](Adaptation.md "Beauchamp:Adaptation") – 18 minutes**

:   • Adapting stimulus B br>
:   • 20 blocks -> 20 direct repeats

*--Finished at 5:20 pm*  
  
**Day 2 Experiment Lineup (5/2/08)**  
**1) ["Stop-Sign" Selectivity](Selectivity.md "Beauchamp:Selectivity") – 8 minutes**

:   • 20 stims from selective category, 5 stims from each nonselective category
:   • Stop-sign task – Same plugin, just tell patient to press button when he sees the stopsign

**2) [Direct-Repeat Adaptation](Adaptation.md "Beauchamp:Adaptation") – 18 minutes**

:   • Adapting stimulus C
:   • 20 blocks -> 20 direct repeats

**3) [Within-Category Adaptation](Adaptation.md "Beauchamp:Adaptation") – 30 minutes**

:   • Adapting stimuli A and B
:   • 30 adapting stimulus pairs → 360 blocks

**Day 3 Experiment Lineup (5/3/08)**  
**1) [Direct-Repeat Adaptation](Adaptation.md "Beauchamp:Adaptation") – 18 minutes**

:   • Adapting stimulus A
:   • **0.8 Hz** presentation time to ensure that LFP has returned to baseline before the repeat appears
:   • 20 blocks -> 20 direct repeats

**2)  [Choice Probability](Choice_Probability.md) - 15 minutes**

:   • Take two stimuli which elicit responses from two different electrodes. Overlay them in a series of images, with varied contrasts of each image. Use these images in the selectivity task.

**3) [Within-Category Adaptation](Adaptation.md "Beauchamp:Adaptation") – 30 minutes**

:   • Adapting stimuli A and B
:   • 20 blocks -> 20 direct repeats/ 20 category-repeats

**If we have extra time:**

:   • If an electrode has very fine selectivity, create stimuli to explore its tuning -- the selective object from different angles, colors, etc.
:   • Continue RF mapping for a finer map by making the spatial extent and stimulus spacing smaller. Keep the size of the stimulus the same so as not to degrade its recognizability.
:   • If we have a broadly selective electrode, we can try RF-mapping stimuli from different categories.
:   • "Scrambled Selectivity" - Pick out a preferred and non-preferred stimulus and make scrambled versions of them at different levels of coherence. Show them at random in the stop-sign task and see if the average response correlated with the amount of image coherence.
:   • Repeat the above experiments using another electrode's selectivity
:   • Multiple presentations of same stimulus:  

    :   Use object selectivity plug-in, and only choose stimulus A.
    :   Show the stimulus 10 times in a row, Stop and save.
    :   Use object selectivity plugin with 10 non-selective stims to de-adapt.
    :   Alternate 5 times
:   • Repeat experiment 4 and 7 with other stimuli
:   • Repeat experiments 2 and 6 to gather more data

## January 2008 Subjects

Proposed experiments for January 2008 subjects.

Focus on ventral temporal and lateral occipital-temporal electrodes with visual responses in fMRI
not on electrodes over early visual cortex  
  
EXPERIMENT: object selectivity to determine preferred and nonpreferred stimuli with 5 well-defined categories, including: faces, bodies, houses, tools, scrambles.  
PLUGIN NAME: HumanObjectSelectivity   
Can rank stimuli by RMS power in a selected window, -1 is worst, -5 is 5th worst, +1 is the best, +5 is the fifth best.   
Channel plot has to contain interval in which you will calculate the RMS power (gray shaded region is stimulation ON time)
Only calculates preferred stimuli for one channel at a time.

METHODS: Present stimuli at their natural size, centered at the fixation point (unless electrodes are only in one hemisphere, in which case present contralateral). If possible, use large, hi-res color stimuli. If not, whatever we can get. Present stimuli for 125 ms, 375 off (2 Hz rate). Each run will be ~10 minutes, allowing ~10 reps of each stimulus.

Task: Subjects will perform one-back repetition detection to ensure attention to the stimulus and maximize responses (SELECT IMAGE REPETITION in behavioral window). Backup task: use target image detection with very long trial duration.   
GOALS: Determine preferred objects of the electrode.

1) Determine if there is a fine-grained representation of category e.g. within the FFA, are there sites that prefer stimuli from other categories?  
2) Is there a sharp tuning within category e.g. within FFA, does the electrode respond to only a single face or many faces?

3) Relationship to retinotopy. Malach predicts that FFA is primarily foveal, PPA primarily peripheral.

ANTICIPATED RESULT:Like in the Malach paper, there will be a sharp tuning with some electrodes only responding to stimuli in their preferred category.  
  
EXPERIMENT: For electrode(s) with nice clean responses to a preferred stimulus, do RF mapping with the 3 most-preferred stimuli (or fewer if necessary)  
PLUGIN NAME: HumanLetterDetection.   
 Pick the preferred image and then do RF mapping; have to do separate runs for different stimuli. Make Letter Target times longer (change all three).  
METHODS: Subjects will perform central letter detection task.   
GOAL: Determine RFs in higher areas (identified with fMRI)  
PREDICTION: Higher areas will have large but not completely homogenous spatial RFs  
Possibility:also map RF with less-preferred stimuli

EXPERIMENT: stimulation at 2 (up to 8) mA (no psychometrics) to see which, if any, late sites evoke percepts  
If there is no percept, at the highest current do 20 trials with behavioral responses to quantify the lack of response.   
If there is a percept, see if it is complex or not.
If a simple phosphene in an early site, do 20 trials with behavioral response at a current to prove there was a percept.
If a complex percept or a later site, do the complete psychometric function.   
PLUGIN NAME: Microstim Staircase   
GOAL: additional data for Dona's current paper; pilot data for grant to show that stimulation in higher areas does NOT produce a percept.  
ANTICIPATED RESULT: few, if any, sites will produce percepts

EXPERIMENT: stimulation of higher electrodes at 2 (or higher) mA while subject makes object or noise discrimination  
i.e. perceptual biasing with preferred stimuli embedded in noise  
PLUGIN NAME: HumanBiasPerception.   
 3 categories of images (noise only, low noise, high noise) place in different folders, load images (images # is TOTAL # of images).   
Stimulus Settings are just within trial. Pre-interval is after trial start but before stimulus comes on; interval is stimulation on-screen or electrical. Inter-interval is between intervals (does not apply because only one choice). Post-choice is time between stimulation and when the response window opens. Behavior/Intertrial is a separate window: response time is length of time for response.

Detailed protocol:

STEP 1:
take preferred stimulus, add a lot of noise so the subject can only detect it 75% of the time in a 2-AFC
(e.g. FACE or NOISE?)
If there is no preferred stimulus, but strong fMRI response, use a stimulus from preferred fMRI category.

STEP 2:
Deliver electrical stimulation while showing the pictures and see if it changes the detection rate.
PREDICTION: Will increase (or decrease the detection rate.

DETAILED METHODS:
Present stimulus for 250 ms, deliver stimulation for the entire stimulation period.  
FEEDBACK: On no stim trials, subject receives correct, incorrect, no response feedback. On stim trials, subject receives correct (if any response is given) or no response feedback. All stim trials are correct because we do not know the subject's percept.

2x2 experimental design:
STIM or NO STIM and
PREF STIM+NOISE or NOISE

Question: for each cell, we will need multiple JPGs--is this possible?

Related experiments:
3x3 experimental design:
HIGH CURRENT STIM, LOW CURRENT STIM, or NO STIM and
PREF STIM, PREF STIM+NOISE, NOISE

Repeat with non-preferred stimulus; see if it produces a behavioral effect.

Future experiments:
Create a 2-IFC design, where each trial contains face and face+noise, subjects selects the interval containing the face.
Stimulation is delivered in one of the epochs or neither.

EXPERIMENT:10-min Resting state data (perhaps awake and asleep)   
  
PLUGIN NAME: Human Letter Detection, Stimulation=Eccentricity, Behavior Settings, click one trial only box, set eccentricity trial to be very long, make blocks be very big

If there is ample time:  
EXPERIMENT: repeated presentation of preferred stimulus; repeated presentation of nonpreferred stimulus (context: letter detection foveally)  
PREDICTION: AAAB more than BBBB  
PLUGIN NAME: HumanAdaptation   
Tries: random sequence parameter, leave at 100

EXPERIMENT:study motion, orientation selectivity using Ping's new screening program

object selectivity with preferred stimulus in big screen of same category stimuli   
object selectivity with preferred stimulus in big screen of nonpreferred category stimuli   
object selectivity with nonpreferred stimulus in big screen of same category stimuli   
object selectivity with nonpreferred stimulus in big screen of preferred category stimuli
