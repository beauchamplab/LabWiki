---
title: CreateCortSurfMod
parent: Beauchamp
---
# CreateCortSurfMod

## Creating the surface

Creating the surface is a 3 step process.
Here are the steps:
[Cortical Surface Models Creation Overview](CorticalSurfaceOverview.md "Beauchamp:CorticalSurfaceOverview")

## Automation

Most of the steps below are contained in the scripts file; information about them is included here for educational purposes.
For the old web page describing an earlier incarnation of @recon, please see
[OLD version of Creating Cortical Surface Models](CreateCortSurfModOLD.md)

## Running FreeSurfer

The cortical surface reconstruction program recon-all has many options for processing the files, which are listed on the wiki:
<https://surfer.nmr.mgh.harvard.edu/fswiki/recon_2dall>
The easiest option is to run the entire file stream with the following command:

```
recon-all –all –s subjID
```

Often this will result in errors because FreeSurfer has permissions issues when copying and appending files. Processor usage can be checked using the program top in another window. If recon-all has been running one subprogram for an inordinate amount of time you can kill it using ctrl-c from the window where you are running recon-all. Reset the permissions so everyone can read and write files from the subject’s directory:

```
sudo chmod –R 777 $SUBJECTS_DIR/subjID
```

After resetting the permissions you should check where the program crashed by viewing recon-all-status.log in the subject’s scripts folder. Check the FreeSurfer wiki on how to restart the file stream from where the program crashed. For example, if the program during CA Normalize the program can be restarted using the following line:

```
recon-all –nogcareg –autorecon2 –autorecon3 –s subjID
```

Since the all the Macs in the lab are multiprocessor machines, the program can delegate each hemisphere to a single processor. To do this recon-all first needs to preprocess the anatomical data and then identify the white matter:

```
recon-all -autorecon1 -s subjID
recon-all -autorecon2 -s subjID -notessellate -nosmooth1 -noinflate1 -noqsphere -nofix -nofinalsurfs -nosmooth2 -noinflate2 –nocortribbon
```

After the white matter has been defined, recon-all can process the two hemispheres separately using separate log and status files:

```
recon-all -s subjID -hemi lh -log $SUBJECTS_DIR/subjID/scripts/recon-all_lh.log -status $SUBJECTS_DIR/subjID/scripts/recon-all-status_lh.log -tessellate -smooth1 -inflate1 -qsphere -fix -finalsurfs -smooth2 -inflate2 -cortribbon -autorecon3 &; recon-all -s subjID -hemi rh -log $SUBJECTS_DIR/subjID/scripts/recon-all_rh.log -status $SUBJECTS_DIR/subjID/scripts/recon-all-status_rh.log -tessellate -smooth1 -inflate1 -qsphere -fix -finalsurfs -smooth2 -inflate2 -cortribbon -autorecon3
```

Alternatively you can use the script in the surfaces folder, which runs recon-all in the manner described above:

```
/surfaces/@recon-all_sep_hemi –subj subjID
```

## Making a Pial Envelope

It can also be useful to have a pial "envelope" that holds the whole brain. For instance, electrodes can be mapped to this surface with the guarantee that they will be visible in any surface model and not buried in cortex. The command to make a pial envelope is

```
 set subjid = pasalar_siavash
 set SUBJECTS_DIR = /Volumes/data9/surfaces/{$subjid}/
 setenv SUBJECTS_DIR /Volumes/data9/surfaces/{$subjid}/
 set ec = SP
 recon-all -s $ec -localGI
```

This command requires that Matlab be in your path; you will receive an error if it is not.
You may also not be able to run multiple copies of Matlab at once, so you should quit all open Matlabs before executing.
This command also computes a local gyrification index, which may be decreased in diseases or disorders and could be interesting to look at.

## Sample Subjects To Look At

Condensed Notes

/Volumes/data9/surfaces/autism/ASD/EB\_010806/EB\_010806notes.rtf

When errors were encountered during autorecon-all

/Volumes/data9/surfaces/autism/ASD/DB\_073006/DB\_073006notes.rtf

Pretty complete Notes

/Volumes/data9/surfaces/hicks\_kali/BVnotes.rtf

covers merging in afni, running recon-all, creating SS500, creating sulc.asc files, aligning to experimental data
