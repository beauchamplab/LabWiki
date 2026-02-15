---
layout: default
title: "Electrode Localization and Naming"
parent: Beauchamp
---
# Electrode Localization and Naming


Also see:
[Beauchamp:Electrophysiology#Processing\_Subject\_Data](Electrophysiology.md#Processing_Subject_Data "Beauchamp:Electrophysiology")

For more detailed instructions, see:
[Creating a Surface Model and Electrode Localization (by Muge Ozker Sertel)](#) "Beauchamp: Creating a Surface Model and Electrode Localization (by Muge Ozker Sertel)")

First you will need to align the CT and MRI data so that when you find the coordinates of the electrodes with the CT, they match up to the fMRI surface you will use. This is done with

3dAllineate -base 3dsag\_t1\_2.nii -source {$ec}\_CT+orig -prefix {$ec}CT\_REGtoanat2 -verb -warp shift\_rotate -cost mutualinfo -1Dfile {$ec}CT\_REGtoanat2

You will then need to make a .tag file to record the position of the electrodes. If you have the electrocorticgraphy report or a picture from surgery, this is helpful to have when you start. Define the underlay as the CT\_REGtoanat2 file and the overlay as the CT scan. It is easiest if you open SUMA and AFNI together for this. In AFNI, go to Define Data Mode, then plug-ins, then Edit Tagset. Using all three views, find the approximate center of the electrode. To record this location, first define the data set you are working with (CT\_Regtoanat2), then name the file in the Tag File box (ex: HJelectrodes.tag). When you have to location you like, select one of the tags and press Set. "Add" will add more spots, "Set" sets that tag to the location you chose. If you have the data available, use the Tag Label Box to define each tag (ex: ch 32- Frontal 1), which is much easier than Tag #1, Tag #2, etc. Try to work in a systematic fashion. Using the SUMA view with the crosshairs (F3) will help. Make sure you press Write and Save frequently. Once you have this file, it is good to make a backup (cp electrodes.tag electrodebackup.tag).

Next you will need to make a .1D file for SUMA to read. It is open the .tag file in Excel to format it correctly. Delete the header row and the labels so that the file is just 3 columns of coordinates. On every row you will need to add 1 1 1 1 1.5 2 so that there are a total of 9 columns. These values are the RGB values and diameter of the electrode spheres. The top row of the file is `#spheres`. Copy all this over back to Text Editor, then save as .1D. In SUMA, press control+command+S and find the 1D file. You should see your electrodes as white spheres. In the full surface view, some electrodes may be underneath the surface. To fix this, you will need to do a very complicated procedure. Notes on that will come later.

It is helpful to have each electrode labeled so that you do not have to refer back to a key in order to see which channel you might want to use. To do this, you will need to make a .do file (do = displayable objects) for SUMA to read that has the labels of each electrode. An example is under /volumes/data1/UT/HJ/afni/HJ\_electrodeslabels.do.txt. The first lines of the file are:
<nido\_head
coord\_type = "mobile"
default\_SO\_label = "CURRENT"
bond = "none"
/>
Then, each line after it is a separate label. It is formatted in the following way:

<T coord ="-33 -31 -46" col ="0.9 0.1 0.1" text=" 1" />

where -33 -31 -46 is the coordinate of that electrode, and 1 is the channel number. You can replace '1' with whatever you'd like as the label. It can be helpful again to use Excel to do the reformatting. "Mobile" is important so that the labels move as you rotate the brain. "None" is important so that the labels are seen regardless if which view is displayed. The .do file is loaded the same way as the .1D file above.

Note that the list of sphere (1D file beginning with `#spheres`) is an older file format, and is superseded by the NIDO sphere object e.g.

```

```

~~So that both spheres and text labels can be placed in the same file and loaded once.
Before doing that, it is good to attach each electrode and label to a surface node.
This prevents the problems of electrodes being partially buried in cortex and invisible. This is caused by changes in brain shape (during neurosurgery) between the pre-implantation MRI (used to create the cortical surface model) and the post-implantation CT (used to localize the electrode).~~
