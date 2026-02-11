---
layout: default
title: "iEEGWorkflow2"
parent: Beauchamp
---
# iEEGWorkflow2


# Overview

This page describes the iEEG workflow at Baylor College of Medicine (BCM) as of December 2021 (YUE).

# Import Data

**1. Locate eCog data in the BCM-EMU shared drive**

Connect to BCM VPN (need BCM account), and connect to the eCog folder:

Press command + K, and in the address line type in:

```
 smb://ecog.bdc.bcm.edu/ecog
```

When prompted, type in your BCM login and password. When connected, go the folder "ECoG\_Data"

All the data collected at BCM-EMU are stored here:

```
 /Volumes/ecog/ECoG_Data/***Datafile/DATA/
```

Go to your subject folder (e.g., data collected for subject "YDZ" are in "YDZDatafile/DATA/"). Select the relevant blocks (numbers) for your task (e.g., "017"). The name structure for the data folder is:

```
 EMU-[Block number]-task-[TaskName]_run-[#]
```

e.g., folder "EMU-013\_task-noisyAV\_run-01" has data from the No.013 block (of all data from this subject), the task is "NoisyAV", and it's run#01 for this task.

Inside each block folder, there are five files for each NSP (still take subject YDZ for example here):

```
 YDJDatafile017.ccf
 YDJDatafile017.nev
 YDJDatafile017.ns3
 YDJDatafile017.ns5
 YDJDatafile017.ns6
```

The ".nev" file is the metadata. The ".ns3" and ".ns5" are the voltage electrode recordings. The ".ns6" file contains the micro-electrode data.

Copy all the above raw files for all the relevant blocks that are in the project to Beauchamp lab Server:

```
 /Volumes/BeauchampServe/rave_data/raw/YDZ/
```

**2. Convert eCog data**

Convert eCog data from the BlackRock files (e.g., ns3, ns5) into matlab files (.mat)

1) Method #1--use a fully automatic one-piece script:

```
 /Volumes/ecog/Foster_Lab/CODE/MASTER/BASICS/EMU_rawData2mat.m
 File:EMU rawData2mat.m
```

```
 1) In MATLAB, cd to the data folder:
 cd('/Volumes/ecog/ECoG_Data/YDLDatafile/DATA')
 2) call the converting function:
 EMU_rawData2mat('YDL',[4:9],150)
```

2) Method #2—convert the files manually in matlab:

```
 >> addpath /Volumes/ecog/Foster_Lab/CODE/EMU_code
    addpath /Volumes/ecog/Foster_Lab/CODE/BASICS
 >> openNSx('YDZDatafile013.ns3','p:double');
    openNSx('YDZDatafile013.ns5','p:double');
    openNSx('YDZDatafile013.ns6','p:double');
 >> save('YDZDatafile013_rawData', 'NS3', 'NS5', 'NS6','-v7.3');
```

Now all the individual channel files within a folder "Indiv\_chans" for this block are stored in:

```
 	/Volumes/ecog/ECoG_Data/YDZDatafile/DATA/013/
```

Lastly, copy all the individual channel files into Beauchamplab shared drive:
/Volumes/BeauchampServe/rave\_data/raw/YDZ/
Data are sorted by blocks. For example, in folder "013", there are 256 individual .mat files, representing each recorded channel in this block.

Note: HOW TO CHECK THE CHANNEL NUMBER FOR A SUBJECT?

[Click here for detailed steps in PDF format.](../../attachments/iEEGWorkflow2/HOW_TO_CHECK_THE_CHANNEL_NUMBER_FOR_A_SUBJECT.pdf "HOW TO CHECK THE CHANNEL NUMBER FOR A SUBJECT.pdf") 
[File:Call convert code.m](#)

# Pre-processing Data

The following steps are all done in RAVE

You can also refer to the RAVE wiki for more detailed information on each module, and the pre-processing flow in RAVE ([ravetutorials](../RAVE/ravetutorials.md))

**1. Import the subject in RAVE:**

Once you are connected to the Beauchamplab Serve, you can use the nice script (RAVE\_PreProc@MacPro.command) that Zhengjia wrote to run the whole processing in Beauchamplab Macpro (see more details on [MacPro](../RAVE/MacPro.md))

Alternatively, you can open an R terminal and type in:

```
 rave::rave_preprocess()
```

Click the 'Overview' module on the left panel:

1-1. 1) subject (e.g., YDZ); 2) project (e.g., EMU\_NoisyWords); Then click "Create Subject";

1-2. 3) folders (e.g., run1...run6/all the blocks that have eCog data); 4) electrodes (e.g., 1-256/based on electrodes.csv); 5) sample rate (2000); 6) physical unit (as-is/no change); 7) file format: .mat/.h5 file per electrode per block; Then click "Check Subject";

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

1) Electrodes: 1-256; 2) Target Sample Rate: 100; 3) Parallel, Number of Cores: 31; 4) Configurations: [New Settings];

Then click "Run Wavelet"; (this step may take 30-40min)

**4. Create Epoch file:**

Note: make sure to change photodiode.pd to photodiode.mat before this step

Click the 'Step3. Trial Epoch' module on the left panel:

1) Epoch Name: New Epoch; 2) Block: run1 (each run needs to be done independently and then exported together); 3) Epoch File: photodiode.mat; 4) Variable name: traces; 5) Variable sample rate: 30000;

Optional settings:
6) Plot range: 0; 7) Threshold select; 8) Minimal trial duration(s)

Use "Toggle Selection"--"Save Changes" once you confirmed the number of events and approximate time interval between events for this run.

After clicking "Save Changes", the selected/green events will be moved to the right panel, and then you can start epoching for the next run. Repeat the same steps till you finish all the runs.

After you did "Save Changes" for all the runs, click "Preview&Export" tab on the top/right side, then rename the epoch file: (e.g., epoch\_YDZ.csv)

**5. Make the final epoch file (applicable for 'EMU\_NoisyWords' project only):**

Click here for more details on how to make epoch\_YDZ\_ALL.csv:
[Click here for detailed steps in PDF format.](../../attachments/iEEGWorkflow2/EMU_NoisyWord_afterEpoch.pdf "EMU NoisyWord afterEpoch.pdf")

# Create the Common Average Reference file workflow

**1. Start a new RAVE window**

Starting from here, you need to start a new RAVE page. First completely close the RAVE pre-processing program by 1) close the RAVE web page; AND 2) close the Terminal/R session.

Same as above, you can either use the script (RAVE@MacPro.command) to run this step in Beauchamplab Macpro, or open an R terminal and type in:

```
 rave::start_rave()
```

Load the subject/project first. Now the pre-processed (above steps) data for this subject under the specific project should have been saved in a folder that RAVE can find automatically.

1) Project: EMU\_NoisyWords; 2) Subject: YDZ; 3) Epoch Table: YDZ\_ALL
Click the 'Overview' module on the left panel:

1) subject (e.g., YDZ); 2) project (e.g., EMU\_NoisyWords); 3) Pre:1; Post:3; 4) Reference Table: default; 5) Electrodes: 1-256;

Then click "Load Data";

**2. Electrode inspection**

After the data is loaded, go to the left side module selection panel and choose "Overview" "Reference Electrodes", then click "Load Data" (this is loading the h5 files for the pre-processed channels)

In the loaded "Reference Electrodes" window:

```
 In the middle panel, "Create Reference Groups":
```

1) Import From: reference\_default.csv; 2) Name: Default; 3) Type: No Reference; 4) Electrodes: 1-256;

This allows you to start inspect the signals from each individual channels per run, to determine which electrode is good/bad.

click the tab "Electrode Inspection" on the top right side, and start this process. You can switch block and electrode number from the "Data Control" panel on the right-most of the window.

Note: It is important to inspect each electrode for every run to determine whether the signals are good/bad.

**3. Generate a common average reference file**

After picking up the bad signal electrodes, exclude these electrodes, and generate a reference signal group using the 'good' electrodes:

In the same "Overview: Reference Electrodes" window, go to the

```
 In the top panel, "Generate Reference Signal"
```

put in the numbers of the 'good' electrodes: e.g. (for YDZ): 1-54,65-94,96-108,129-130,132-134,136-159

Then click "Generate Reference". This will create a group of appointed 'good' electrodes that we can later use for creating a common average reference file.

```
 In the middle panel, "Create Reference Groups":
```

1) Import From: new; 2) Name: CAR; 3) Type: Common Average Reference; 4) Electrodes: 1-256;

```
 In the bottom panel, "View Reference Groups":
```

1) Group Number: 1; 2) Reference to: ref\_1-54,65-94,96-108,129-130,132-134,136-159 (this is the file generated in the step before); 3) Bad Electrodes: (leave blank)

note: we want to leave "Bad Electrodes" blank because once we appoint electrode(s)as 'bad' electrode here, we won't be able to view it in our later analysis. On the contrary, if we do not nominate the 'bad' electrode(s) here, we can still view the performance of these electrode(s) in later analysis, but importantly, we have EXCLUDED them from generating the common average reference file.

Then click "Save Group".

Then click "Preview & Export", "Export & Cache".

This will take 10-15min to cache the files. Once it's done, you should re-load the subject to start your analysis.
