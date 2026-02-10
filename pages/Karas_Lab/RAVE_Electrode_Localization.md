# RAVE Electrode Localization

> **Navigation:** [Home](../Beauchamp/index.md) | [Publications](../Beauchamp/Publications.md) | [Resources](../Beauchamp/DataSharing.md)

[![](../../attachments/Karas_Lab/Karas_Lab_Logo_Small_White.png)](../../attachments/Karas_Lab/Karas_Lab_Logo_Small_White.png)

[**Home**](index.md)        
 [**Contact**](Contact.md)        
 [**Lab Notebook**](Lab_Notebook.md)        
 [**Lab Members**](Lab_Members.md)        
 [**Publications**](Publications.md)        
 [**Research**](Research.md)        
 [**Talks**](#)")

# Processing Pipeline

## Pre-RAVE processing

RAVE currently (as of December 2021) does not have integrated CT and MRI co-registration, so it is necessary to complete these steps separately. Our current pipeline uses FreeSurfer to reconstruct the pial surface and iELVis to coregister the images.

The steps for this can be found at [Beauchamp:BuffyElectrodeNotes](Beauchamp/BuffyElectrodeNotes.md "Beauchamp:BuffyElectrodeNotes"). You will need to install the [prerequisites](../Beauchamp/BuffyElectrodeNotes.md#Prerequisites "Beauchamp:BuffyElectrodeNotes") (except for BioImage Suite), and then follow the steps from [Starting Electrode Localization](../Beauchamp/BuffyElectrodeNotes.md#Starting_Electrode_Localization "Beauchamp:BuffyElectrodeNotes") to [CT Alignment](../Beauchamp/BuffyElectrodeNotes.md#CT_alignment "Beauchamp:BuffyElectrodeNotes").

## Electrode Localization in RAVE

First things first: if you don't have RAVE installed, follow these steps to do so: [RAVE:Install](../RAVE/Install.md)

After RAVE installation and the pre-RAVE processing steps, you're ready to localize some electrodes in RAVE! You will need three things:

1. Subject code - the same one you used for the pre-RAVE processing steps
2. Path to the subject's FreeSurfer directory - this is the "target folder" that you have been using during the pre-RAVE steps. The folder's name should be the subject code and it should contain sub-folders including /elec\_recon, /label, /mri, and /surf, among others. These folders were all generated during pre-RAVE processing.
3. Path to the co-registered CT and MRI - this should be located in the /elec\_recon folder. It will be a file called postInPre.nii.gz.

Once you have these three things, call the rave::electrode\_localization command. Here is an example with the subject code YDL:

```
rave::electrode_localization(subject_code = 'YDL',
                             freesurfer_path = '/Applications/freesurfer/7.2.0/subjects/YDL',
                             ct_path = '/Applications/freesurfer/7.2.0/subjects/YDL/elec_recon/postInPre.nii.gz')
```

After a few seconds, this should load RAVE's electrode localization WebUI. [Here](https://youtu.be/raVyJKb1DTY?t=140) is a useful video on the electrode localization process. The description of how to use the actual UI starts at 2:20.

# Troubleshooting

## Pre-RAVE processing

Note: these tips are meant to be a supplement to the instructions on [Beauchamp:BuffyElectrodeNotes](Beauchamp/BuffyElectrodeNotes.md "Beauchamp:BuffyElectrodeNotes"). Make sure that you have followed all the steps there first, and check the [troubleshooting](../Beauchamp/BuffyElectrodeNotes.md#Troubleshooting "Beauchamp:BuffyElectrodeNotes") tips there as well.

### Change shell to BASH

Make sure that you are using BASH as your shell rather than zsh, which is the default on newer Macs. To do so, run

```
chsh -s /bin/bash
```

### .bashrc vs .bash\_profile?

[Buffy's Electrode Notes](../Beauchamp/BuffyElectrodeNotes.md#BASH "Beauchamp:BuffyElectrodeNotes") say to create a .bashrc file, but doing the same things except in a .bash\_profile file is what worked for me on MacOS. Apparently this is because .bashrc is for interactive non-login shells while .bash\_profile is for login shells, and opening Terminal in OS X defaults to running a login shell. Here is what's in my .bash\_profile file. Note that your directories/filepaths may be different from mine, depending on where you installed FreeSurfer and where you downloaded the iELVis-master folder.

```
# SETUP iELVis Freesurfer
export FREESURFER_HOME=/Applications/freesurfer/7.2.0
export SUBJECTS_DIR=$FREESURFER_HOME/subjects
source $FREESURFER_HOME/SetUpFreeSurfer.sh
# FSL Setup
FSLDIR=/usr/local/fsl
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH
. ${FSLDIR}/etc/fslconf/fsl.sh
# SETUP iELVIS BASH
export PATH=$PATH:/Applications/iELVis-master/iELVis_MAIN/iELVis_BASH
export PATH=$PATH:/Applications/iELVis-master/iELVis_MAIN/iELVis_MATLAB
# MATLAB
export PATH=$PATH:/Applications/MATLAB_R2021b.app/bin
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### ERROR: Matlab is required... or ERROR: <some command> not found

This happens when you haven't added something (either MATLAB or the directory containing <some command>) to the shell's path. The path lists the directories where the shell looks when it's trying to run a program, so if the path to a command isn't in there, there will be an error when that command is called. To check the directories in your path, type $PATH in terminal. You will need to figure out what command is missing, find what directory that command is in, and then add it to the path. For example, to add MATLAB to the path, you can enter

```
export PATH=$PATH:/Applications/MATLAB_R2021b.app/bin
```

Take a gander at the above .bash\_profile file to see what directories I have exported to the $PATH. Putting these in .bash\_profile ensures that they are added to the path each time you start a BASH terminal session, rather than only adding it in the current instance.

### ERROR: unrecognized function or variable 'fspecial'

It turns out that the recon-all process needs the image processing toolbox in MATLAB. After you install that toolbox this error should go away.
