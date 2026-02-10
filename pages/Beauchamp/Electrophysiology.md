# Electrophysiology

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

[Old Protocols](Old_Protocols.md)

## September 2008 E-Phys Protocol

**9/22/2008 Setup and Surgery**   
1. Identify potential electrodes with combined fMRI/CT   
2. Create log file on log computer   
3. Record resting activity and assess recording setup (Test signal-to-noise, etc.)

**Microelectrode array experiments**   
If the new electrodes are ready, it will be a top priority to investigate their properties.  
Some things to look at:   
**Recording**

:   **1. Stimulus selectivity**   

    :   How does the stimulus-selectivity of microelectrodes differ from large electrodes?
    :   How does stimulus-selectivity vary within a single microelectrode array (MEA)?

:   **2. Response latency/duration**   

    :   Within an object-selective visual area, do different patches of cortex depolarize at different latencies or for different durations?

:   **3. Receptive Field Size**   

    :   Do small electrodes have different RFs than big electrodes?
    :   How does RF size vary within and between object-selective visual areas?
:   **4. Gamma oscillation**   

    :   Are oscillations in the gamma band more correlated among nearby electrodes than far electrodes?

:   **5. Adaptation**

    :   Do microelectrodes demonstrate different adaptation behavior than large electrodes?
    :   Do different microelectrodes within an ME array adapt differently to the same repeated stimuli?

:   **6. Choice probability**

    :   Does the pattern of activity in object-selective cortical areas (as measured by MEAs) correlate in any way with the subject's behavior?

**Stimulation**

:   **1. Perception thresholds**

    :   Perception thresholds may be lower with microelectrodes because of high current density.
:   **2. Percepts in higher visual areas**

    :   If the microelectrodes have smaller RFs or are more feature-selective than the large electrodes, it could mean that sending current through them would activate a more functionally-segregated group of neurons than has previously been possible. If so, microstimulation with microelectrodes may be more likely to evoke percepts in higher-level visual areas than with the large electrodes.

**Ryan's Adaptation Experiments**  
**1) [Target-detection Selectivity](Selectivity.md) – 20 minutes**

:   • 80 stimuli (+5 target stimuli), 20 blocks
:   • Stop-sign task (patient reports stop-signs)

**2) [Repeat-detection Selectivity](Selectivity.md) – 20 minutes**

:   • 80 stimuli, 20 blocks
:   • One-back task (patient reports repetitions of images)

**3) [Multiple-repetitions adaptation](Adaptation.md) - 5 minutes**

:   • 20 selective stimuli, 20 nonselective stimuli, 2 Hz presentation, patient is told to press button when he/she sees the stopsign.
:   • trial structure: 8 nonselective stimuli, 8 of the same selective stimulus, 8 nonselective stimuli, 8 different selective stimuli. Stopsign appear at random or at the end of each run.
:   • A rudimentary way to approximate this would be to have several copies of the same image in the image folder, and selecting all of them in the selectivity plugin.

**Notes:**

:   • Now that we can record from all the electrodes simultaneously, it will be less important to identify selective categories. By showing equal amount of all the categories, we can get good sample sizes for several differently-selective electrodes.

:   •It would be nice to have a modified version of the current Selectivity plugin to satisfy these conditions:   

    :   1. the patient is supposed to press the button after stop-signs instead of after repeats
    :   2. Selective stimuli are directly repeated every 8-12 images
    :   3. The stimulus preceding the repeat is always a nonselective stimulus

## Electrophysiology Protocols

[Presurgical Scanning](Presurgical_Scanning.md)

After analysing fMRI data, upload the entire contents of the AFNI and SUMA directories to Xfiles.
This can be simplfied by Apple-K (Connect to Server) in Finder and choosing XFiles;

```
 xfiles.hsc.uth.tmc.edu (129.106.148.217)
```

then the folders can be dragged from the server to Xfiles, or copied in the command line, easily (without using the Web-based GUI interface).

*In the EMU*

[Setup Apparatus](Setup_Apparatus.md)

[Receptive Field Mapping](Receptive_Field_Mapping.md)

[Electrical Stimulation](Electrical_Stimulation.md)

[Selectivity](Selectivity.md)

[Perceptual Biasing](Perceptual_Biasing.md)

[Adaptation](Adaptation.md)

[Making Grayscale From Color Images](Making_Grayscale_From_Color_Images.md)

It is also good to collect 10 minutes of resting data (no stimulation) from as many visual electrodes as possible for later analyses.

## Todo list

Decide on screening stimuli i.e. pick 20 from each category
faces, houses, bodies, scenes, tools, scrambles   
Get rid of bad looking stimuli; make detailed protocol   
Install matlab in EMU to allow image scrambling; install scrambling program.

1/16/2008
Add peak deflection (either -,+ or ABS) to RMS power measurement when ranking stimuli.

## Processing Subject Data

see also [Beauchamp:Electrode\_Localization\_and\_Naming](Electrode_Localization_and_Naming.md "Beauchamp:Electrode Localization and Naming")

After obtaining the CD containing the patient CT data from St. Luke's, use OsiriX to export all images
(using the export to DICOM option, and the hierarchical, uncompress options).

CT scans have voxel size 0.488x0.488x1 mm; this may need to be adjusted manually with

```
 3drefit -zdel 1.000 DE_CTSDE+orig
```

(If the CTs look distorted in AFNI, then the voxel size must be adjusted).
Next, the CTs must be registered with the hi-res presurgical MRI anatomy.
This may fail because the CT has a coordinate system with a very different origin than the MRI.
Registration routines will not work if the input datasets are not in rough alignment.
To check this, type

```
 3dinfo DE_CTSDE+orig
```

returns

```
 R-to-L extent:  -124.756 [R] -to-   124.756 [L] -step-     0.488 mm [512 voxels]
 A-to-P extent:  -124.756 [A] -to-   124.756 [P] -step-     0.488 mm [512 voxels]
 I-to-S extent:  -258.000 [I] -to-   -86.000 [I] -step-     1.000 mm [173 voxels]
```

We want the center of the dataset to be roughly at (0,0,0). For this example, this is true for (x,y) but not for z.
First, create a copy of the dataset

```
 3dcopy DE_CTSDE+orig DE_CTSDEshift
```

Then, recenter the z-axis

```
 3drefit -zorigin 80 DE_CTSDEshift+orig
```

3dinfo returns

```
 R-to-L extent:  -124.756 [R] -to-   124.756 [L] -step-     0.488 mm [512 voxels]
 A-to-P extent:  -124.756 [A] -to-   124.756 [P] -step-     0.488 mm [512 voxels]
 I-to-S extent:   -80.000 [I] -to-    92.000 [S] -step-     1.000 mm [173 voxels]
```

The z-axis is now roughly centered around 0. In AFNI, examine the MR and the shifted CT to make sure they are in rough alignment. Next, use 3dAllineate to align the two datasets.

```
 3dAllineate -base {$ec}anatavg+orig -source DE_CTSDEshift+orig -prefix {$ec}CTSDE_REGtoanatV4 -verb -warp shift_rotate -cost mutualinfo -1Dfile {$ec}CTSDE_REGtoanatXformV4
```

Check in AFNI to make sure that they alignment is correct. NB: It is also possible to crop the MRI before Allineating since the MR coverage is typically greater than the CT coverage. In a test case, this did not have a big effect.

Next, the electrodes positions are manually located and saved as Tags. Then, these positions can be used to create an Electrodes file for display as spheres in SUMA.
To label the electrodes, a separate .niml.do file can be created with the label for each electrode.
Sample file electrodes.1D

```
 #spheres
 -20.43       81.53       4.254  0.0 0.0 0.0 1.0  1.1   
 -28.43       76.84       4.254  0.0 0.0 0.0 1.0  1.1           
 -36.43       70.28       4.254  0.0 0.0 0.0 1.0  1.1             
 -42.43       61.84       4.254  0.0 0.0 0.0 1.0  1.1           
 -48.43       54.34       4.254  0.0 0.0 0.0 1.0  1.1            
 -52.43       44.03       4.254  0.0 0.0 0.0 1.0  1.1
```

Sample file testelectrodeslabels.niml.do

```
 <nido_head
 coord_type = "mobile"
 default_SO_label = "CURRENT"
 bond = "surface"
   default_color = '1.0 1.0 1.0'
 default_font = 'he14'
 />
 <T
 coord = "-20.43       81.53       4.254"
 col = "0.1 0.9 0.1"
 text = "RPIT1"
 />
 />
```

## Things to do

HumanImageDetection

:   Can stimuli be vector-based rather than pixel based, so as not to lose resolution with scaling? POSSIBLE if original file is vector-based
:   Enable online scrambling LOOKING INTO IT
:   Enable online color to black and white conversion LOOKING INTO IT

HumanLetterDetection

:   Analyze data from LR to see where the RFs are

DEBUGGING KNOT PROBLEMS

First, quit Knot.
Then, unplug one ITC from the USB port, wait for the power light to go off, plug it back in.
Repeat this, one at a time, for all ITCs.
Before beginning experiment, always make sure you get nice traces in Channel Data window, not just flat lines (even if looks nice on oscilloscope).

1-AFC task:
change feedback so that it is not always correct.

can we extend stimulation into the response window?

## Measuring Impedance

From Nafi
preamp should have a built-in impedance tester? That’s generally a good thing to have with low-impedance electrodes so that you can know what the actual impedance is as you’re recording since how the electrodes are placed can affect the functional impedance. But basically the way they work is that they have a parallel circuit which connects a resistor to the point that the preamp is measuring the voltage. At the other end of the resistor they pass an AC signal (a 1kHz sinusoid is standard), and based on the voltage you read on the preamp you can calculate the impedance; for instance if you’re using a 1MOhm resistor along with a 1V signal, and you read 10mV across the electrode, you’ll know your impedance is roughly 10k (0.10V = 1V\*[R/(1M +R)] -> 0.99R = 10,000). To do it by hand you could use a function generator and an oscilloscope, just connect a resistor to where the electrode would connect to the preamp, put the electrodes in saline and apply a signal at the resistor with ground in the saline, and measure the voltage in between the resistor and the electrode using your scope.
