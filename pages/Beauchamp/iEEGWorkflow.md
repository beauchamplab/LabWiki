---
title: iEEGWorkflow
parent: Beauchamp
---
# iEEGWorkflow

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

To search for things on the wiki, use Google's site search feature. For instance, to find an Experiment Sheet, type

```
 on this wiki ExperimentSheet
```

# Overview

This page describes the iEEG workflow at University of Pennsylvania (UPENN) as of December 2021 (YUE).

# Check iEEG Data Files

Following the script and protocol "Download iEEG data from ieeg.org (UPENN data)", you should have the eCog data for the subject before the following steps.

Data should be kept on the Beauchamp lab server in (take HUP225 for example here):

```
  /Volumes/BeauchampServe/rave_data/raw/HUP225/run#
```

Inside the individual run folder, there are two matlab files:

```
data.mat
photodiode.pd
```

"data.mat" is the voltage electrode recording file. All the channels are collapsed into this single file.
"photodiode.pd" is the photodiode timestamp for epoch. Before the epoching step, this file needs to be changed to "photodiode.mat".

# Go to RAVE and begin the preprocessing workflow

You can also refer to the RAVE wiki for more detailed information on each module, and the pre-processing flow in RAVE ([ravetutorials](../RAVE/ravetutorials.md))

**1. Import the subject in RAVE:**

Once you are connected to the Beauchamplab Serve, you can use the nice script (RAVE\_PreProc@MacPro.command) that Zhengjia wrote to run the whole processing in Beauchamplab Macpro (see more details on [MacPro](../RAVE/MacPro.md))

Alternatively, you can open an R terminal and type in:

```
 rave::rave_preprocess()
```

Click the 'Overview' module on the left panel:

1-1. 1) subject (e.g., HUP225); 2) project (e.g., EMU\_NoisyWords); Then click "Create Subject";

1-2. 3) folders (e.g., run1...run5/all the blocks that have eCog data); 4) electrodes (e.g., 1-175/based on electrodes.csv); 5) sample rate (1024); 6) physical unit (as-is/no change); 7) file format: Single .mat/.h5 file per block; Then click "Check Subject";

**2. Notch Filter:**

Click the 'Step1. Notch Filter' module on the left panel:

1) Base Frequency: 60; 2) X(Times): 1,2,3; 3) +-(Band Width, Hz): 1,2,2;

```
 Band 1:
 59 Hz - 61 Hz (60±1)
 Band 2:
 118 Hz - 122 Hz (120±2)
 Band 3:
 178 Hz - 182 Hz (180±2)
```

Then click "Apply Notch Filters"; (this step may take 2-5 min)

**3. Wavelet:**

Click the 'Step2. Wavelet' module on the left panel:

1) Electrodes: 1-175; 2) Target Sample Rate: 100; 3) Parallel, Number of Cores: 31; 4) Configurations: [New Settings];

Then click "Run Wavelet"; (this step may take 30-40min)

**4. Create Epoch file:**

Note: make sure to change photodiode.pd to photodiode.mat before this step

Click the 'Step3. Trial Epoch' module on the left panel:

1) Epoch Name: New Epoch; 2) Block: run1 (each run needs to be done independently and then exported together); 3) Epoch File: photodiode.mat; 4) Variable name: traces; 5) Variable sample rate: 1024;

Optional settings:
6) Plot range: 0; 7) Threshold select; 8) Minimal trial duration(s)

Use "Toggle Selection"--"Save Changes" once you confirmed the number of events and approximate time interval between events for this run.

After clicking "Save Changes", the selected/green events will be moved to the right panel, and then you can start epoching for the next run. Repeat the same steps till you finish all the runs.

After you did "Save Changes" for all the runs, click "Preview&Export" tab on the top/right side, then rename the epoch file: (e.g., epoch\_HUP225.csv)

**5. Make the final epoch file (applicable for 'EMU\_NoisyWords' project only):**

Click here for more details on how to make epoch\_HUP225\_ALL.csv:
[Click here for detailed steps in PDF format.](../../attachments/iEEGWorkflow/EMU_NoisyWord_afterEpoch.pdf "EMU NoisyWord afterEpoch.pdf")

# Create the Common Average Reference file workflow

**1. Start a new RAVE window**

Starting from here, you need to start a new RAVE page. First completely close the RAVE pre-processing program by 1) close the RAVE web page; AND 2) close the Terminal/R session.

Same as above, you can either use the script (RAVE@MacPro.command) to run this step in Beauchamplab Macpro, or open an R terminal and type in:

```
 rave::start_rave()
```

Load the subject/project first. Now the pre-processed (above steps) data for this subject under the specific project should have been saved in a folder that RAVE can find automatically.

1) Project: EMU\_NoisyWords; 2) Subject: HUP225; 3) Epoch Table: HUP225\_ALL
Click the 'Overview' module on the left panel:

1) subject (e.g., HUP225); 2) project (e.g., EMU\_NoisyWords); 3) Pre:1; Post:3; 4) Reference Table: default; 5) Electrodes: 1-175;

Then click "Load Data";

**2. Electrode inspection**

After the data is loaded, go to the left side module selection panel and choose "Overview" "Reference Electrodes", then click "Load Data" (this is loading the h5 files for the pre-processed channels)

In the loaded "Reference Electrodes" window:

```
 In the middle panel, "Create Reference Groups":
```

1) Import From: reference\_default.csv; 2) Name: Default; 3) Type: No Reference; 4) Electrodes: 1-175;

This allows you to start inspect the signals from each individual channels per run, to determine which electrode is good/bad.

click the tab "Electrode Inspection" on the top right side, and start this process. You can switch block and electrode number from the "Data Control" panel on the right-most of the window.

Note: It is important to inspect each electrode for every run to determine whether the signals are good/bad.

**3. Generate a common average reference file**

After picking up the bad signal electrodes, exclude these electrodes, and generate a reference signal group using the 'good' electrodes:

In the same "Overview: Reference Electrodes" window, go to the

```
 In the top panel, "Generate Reference Signal"
```

put in the numbers of the 'good' electrodes: e.g. (for HUP225): 1-15,23-30,32-42,44-102,104-114,117-125,128-174

Then click "Generate Reference". This will create a group of appointed 'good' electrodes that we can later use for creating a common average reference file.

```
 In the middle panel, "Create Reference Groups":
```

1) Import From: new; 2) Name: CAR; 3) Type: Common Average Reference; 4) Electrodes: 1-175;

```
 In the bottom panel, "View Reference Groups":
```

1) Group Number: 1; 2) Reference to: ref\_1-15,23-30,32-42,44-102,104-114,117-125,128-174 (this is the file generated in the step before); 3) Bad Electrodes: (leave blank)

note: we want to leave "Bad Electrodes" blank because once we appoint electrode(s)as 'bad' electrode here, we won't be able to view it in our later analysis. On the contrary, if we do not nominate the 'bad' electrode(s) here, we can still view the performance of these electrode(s) in later analysis, but importantly, we have EXCLUDED them from generating the common average reference file.

Then click "Save Group".

Then click "Preview & Export", "Export & Cache".

This will take 10-15min to cache the files. Once it's done, you should re-load the subject to start your analysis.
