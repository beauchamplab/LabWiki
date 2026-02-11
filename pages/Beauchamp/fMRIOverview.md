# fMRIOverview

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

Overview of fMRI Experiments

# BEFORE THE FMRI EXPERIMENT

1. Reserve scanner time.

```
 https://bcm.corefacilities.org/sc/3684/camri/?tab=equipment
```

Prepare all paperwork:

1. Consent form for the subject
2. Payment form for the subject
3. Experiment sheet listing the details of the experiment, including the subject name, DOB and experiment code (see below). [Experiment Sheet](../../attachments/fMRIOverview/ExperimentSheet.doc "ExperimentSheet.doc")
4. fMRI safety screening form. This must be filled out for EVERY EXPERIMENT, even if the subject has been scanned before (something could have changed in the meantime).
5. CAMRI billing half-sheet
6. Subject payment form (including SSN and home address for tax purposes)

Take all of this paperwork to the MR scanner. After scanning, leave the billing half-sheet and the screening form in the provided folder.
Use the ScanScap document scanner to make PDFs of the other docuemnts (consent form, payment form, experiment sheet) and put them in the subject's directory (created below).

# AFTER THE FMRI EXPERIMENT

see
<CreateAFNIBRIKfromMR.md#Getting_Data_From_the_UT_Philips_Scanner>
for more details.

The first step is to obtain the fMRI data from the scanner.

1. [Getting raw fMRI data from the scanner](CreateAFNIBRIKfromMR.md "Beauchamp:CreateAFNIBRIKfromMR")

Vips will copy the data into a directory on the server, such as

```
 /Users/mri/raw/2008_data
```

(If you don't see this directory, you may have to mount it using Apple-K first).
We do not analyze the data in this directory, because we want to keep a pristine copy of the raw data.
Instead, we copy the data to an analysis directory. This is usually in the format
/Volumes/data1/UT/XX
Where "XX" is a unique two-letter code that corresponds to the experiment.
Each fMRI experiment is assigned a successive code, beginning at AA.
To keep track of which is the current code, and which code corresponds to which experiment, there is an Excel spreadsheet called
"ExperimentSummaryv2.XLS" in /Volumes/data1 .
Before and after you do an experiment it is important to check this spreadsheet to make sure that you use the correct experiment code.
The demographic data MUST be entered into this spreadsheet.

All paperwork must be scanned into a PDF (using Epson Scan software) and placed into the subject's directory (/Volumes/data1/UT/XX). This is especially critical for the experiment sheet, the consent form, and the subject payment form.

# ANALYSING THE FMRI DATA

After determining the correct experiment code, create the experiment directory

```
 cd /Volumes/data1/UT
 mkdir EI 
 cd EI
```

Within this experiment directory, several subdirectories are created:

```
 mkdir afni
```

This will hold all of the AFNI data.

```
 mkdir behavioraldata
```

This folder should contain a copy of the ACTUAL stimulus presentation script that was run on the subject,
such as a Presentation .SCE/.PCL file or a Python .py program.
All programs that were run should be copied for ease of reference.
As well, logs recording the behavioral responses made by the subject, such as button presses or eye-movement data, should be copied from the stimulus or eye-movement computer to this directory.

As a guide to processing data, it is critical to keep notes of all processing steps. These notes are kept in a text file in the experiment directory, such as

```
 XX_notes.rtf
```

These notes should contain the date, a summary of the experimental conditions, and ALL steps used to process the data. To make creating this easier, it is good to copy it from a Notes file of a previous experiment with a similar task paradigm or experimental design. For instance

```
 cp /Volumes/data1/UT/EG/EGNotes.rtf ./EINotes.rtf
 open EINotes.rtf
```

and make necessary changes.
The notes files is NOT a shell script. Instead, use the copy and paste commands to copy commands from the notes file to a Terminal or X11 window.

The "behavioraldata" folder

After a directory is created, it is important to change the permissions so that other users can access it.

chmod -R 777 \*
