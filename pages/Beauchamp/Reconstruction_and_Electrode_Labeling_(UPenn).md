---
title: Reconstruction and Electrode Labeling (UPenn)
parent: Beauchamp
---
# Reconstruction and Electrode Labeling (UPenn)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

# Reconstruction and Electrode Labeling (UPenn)

The electrode labeling is usually done the day after the implant (i.e. since implants are Wednesday, the labels are finished on Thursday).
Login to the shared Box folder "CNT Implant Reconstructions", sort by date, look for the most recent, e.g.

```
 RID808_ITK-SNAP
```

Copy the entire contents of this folder (e.g. RID808\_ITK-SNAP.zip) to the server in the subject's directory (e.g. /BeauchampServe/rave\_data/raw/PAV001) and unzip the file by double clicking on it. (After unzipping, the original .zip file can be deleted). Some of the files in this folder can be used by RAVE, in particular, the T1 (anatomical MRI)

```
 T00_RIDxxxx_mprage.nii.gz
```

the coordinates of the electrodes

```
 electrode_coordinates_T1.csv
```

The names of the electrodes

```
 electrodenames_coordinates_native_and_T1.csv
```

Optional files for checking

```
 electrode_snaplabel.txt (to confirm the channels)
 electrodelabels.csv (optional, for double checking)
```

Copy only these files to the

## Creating Electrode Labeling File

The electrode labeling file (electrodes.csv) is required for RAVE to localize the electrodes (channels). Make sure the coordinates are in T1 space (NOT MNI, or other spaces).
Open this file, and save a copy as "electrodes.csv"

```
 electrodenames_coordinates_native_and_T1.csv
```

Move the columns into the right order and delete the remaining columns.

1. The first column should be the electrode number (1-x). Create this with the fill command, or copy from column G or H of the file
2. The next three columns are the coordinates of each electrode. Columns K-L-M of the above file
3. The last two columns are the labels (electrode clinical label and parcellation label).

Next, insert a row with the following headers (the first five column headers must be EXACTLY as written)
Electrode Coord\_x Coord\_y Coord\_z Label Anatomical\_Label

This is how you make electrodes.csv:

```
 copy the first THREE columns from "electrode_coordinates_T1.csv" (they are the coordinates in T1 space: Coord_x;Coord_y;Coord_z);
```

```
 copy the first TWO columns from "electrodenames_coordinates_native_and_T1.csv" (they are the Label; FreeSurferLabel for each channel);
```

```
 Copy the numbering label from "electrodenames_coordinates_native_and_T1.csv"--Column G or H (this is the 'Electrode' numbers);
```

This will create an electrodes.csv file with the following columns: Electrode; Coord\_x; Coord\_y; Coord\_z; Label; FreeSurferLabel

To finish up this file, fill all the blank rows in the 'FreeSurferLabel' column with 'OOB' (standing for 'out of brain').

Save this electrodes.csv in /BeauchampServe/rave\_data/${subj}/localization.

This file will need to be copied into the pre-processed subject folder (usually it's under a project folder), for example, it should be in:

```
 /BeauchampServe/rave_data/ent_data/EMUNoisyWords/HUP225/rave/meta/electrodes.csv
```

This shows that electrodes.csv is in subject HUP213 pre-processed RAVE folder, and this subject belongs to the 'EMUNoisyWords' project.

IMPORTANT NOTE:: Compare the channel number and channel label between the electrode.csv file and the channels.csv (generated when downloading the RAVE data), to confirm the channels.

## OPTIONAL: It can be helpful to create a cortical surface reconstruction in FreeSurfer. If doing so, use the following steps

### Create a cortical surface model

Also see similar pages on the Lab Notebook.)
Open a terminal, and navigate to the subject folder in rave directory. Each subject has a RID code that was assigned by UPenn, for example, subject HUP225 was assigned as RID700:

```
 cd /BeauchampServe/rave_data/${subj}/localization
```

```
 set subj = HUP225
```

```
 setenv SUBJECTS_DIR `pwd`
```

Unzip the T1\_MPRAGE file by double clicking the file "T00\_RID${subj}\_mprage.nii.gz"

Reconstruction in freesurfer:

```
 recon-all -all -parallel -subject fs -i ./T00_RID700_mprage.nii
```

Freesurfer will complete the reconstruction (This step may take 4-5 hours)

## Creating Electrode Labeling File

The electrode labeling file (electrodes.csv) is required for RAVE to localize the electrodes (channels). Make sure the coordinates are in T1 space (NOT MNI, or other spaces):

This is how you make electrodes.csv:

```
 copy the first THREE columns from "electrode_coordinates_T1.csv" (they are the coordinates in T1 space: Coord_x;Coord_y;Coord_z);
```

```
 copy the first TWO columns from "electrodenames_coordinates_native_and_T1.csv" (they are the Label; FreeSurferLabel for each channel);
```

```
 Copy the numbering label from "electrodenames_coordinates_native_and_T1.csv"--Column G or H (this is the 'Electrode' numbers);
```

This will create an electrodes.csv file with the following columns: Electrode; Coord\_x; Coord\_y; Coord\_z; Label; FreeSurferLabel

To finish up this file, fill all the blank rows in the 'FreeSurferLabel' column with 'OOB' (standing for 'out of brain').

Save this electrodes.csv in /BeauchampServe/rave\_data/${subj}/localization.

This file will need to be copied into the pre-processed subject folder (usually it's under a project folder), for example, it should be in:

```
 /BeauchampServe/rave_data/ent_data/EMUNoisyWords/HUP225/rave/meta/electrodes.csv
```

This shows that electrodes.csv is in subject HUP213 pre-processed RAVE folder, and this subject belongs to the 'EMUNoisyWords' project.

IMPORTANT NOTE:: Compare the channel number and channel label between the electrode.csv file and the channels.csv (generated when downloading the RAVE data), to confirm the channels.

### Converting coordinates from T1 space to fs space using RAVE

Note:: Subject's T1 needs to be reconstructed in freesurfer (i.e., there is a fs folder in project/subject) before you run the following code
In R, type in the following commands:

```
 rave::import_electrodes("/Volumes/PennRAID/Dropbox (PENN Neurotrauma)/BeauchampServe/rave_data/raw/HUP225/localization/electrodes.csv",subject = 'EMU_NoisyWords/HUP225',use_fs = TRUE)
```

This is a one-line code to convert T1 space to fs space for RAVE to use in the 3D viewer.

The columns in the electrodes.csv file are:

```
 Electrode	Label	ClearLabel	T1R	T1A	T1S
```

Electrode: 1 - # (all the electrode numbers in order, COPIED from the electrodenames\_coordinates\_native\_and\_T1.csv/column G)

Label, T1R, T1A, T1S: COPIED from the electrodenames\_coordinates\_native\_and\_T1.csv (columns B, K, L, M)

This one-line code will then save a new electrodes.csv file in the subject/project folder:
/Volumes/PennRAID/Dropbox (PENN Neurotrauma)/BeauchampServe/rave\_data/ent\_data/EMU\_NoisyWords/HUP225/rave/meta/

With freesurfer coordinates (Coord\_x, Coord\_y, Coord\_z), and two different mni space coordinates (MNI305\_x, y, z/MNI152\_x, y z)
RAVE used one coord to generate all others.
The order of these coordinates is: freesurfer coord > T1 coord > MNI305 coord > MNI152 coord
Thus, if freesurfer coordinates exist, all other coordinates will be ignored.

```
 Note: in order for this one-line code to work, you have to make sure there is a electrodes.csv existed in the $project/$subject/rave/meta/ folder. Usually RAVE generates it when you first imported the subject.
 If this file is accidentally deleted, you can always make a dummy electrodes.csv file with all the electrode coordinates as ' 0 0 0 '. As far as the columns are named exactly as: 
 Electrode	  Coord_x  Coord_y  Coord_z   Label
```
