> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# SuthanaDemo 2023

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/SuthanaDemo_2023/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

text grab of file SuthanaDemo.html

Electrode Localization Demo for Suthana Lab
1. Install RAVE
2. Create your First RAVE Subject
3. Imaging Pre-processing
4. Electrode Localization
5. Preview the localization results

* Some extending topics may have not been covered in the demo session

1. Install RAVE
The installation guide can be found at <https://rave.wiki/>

Please make sure you meet all the prerequisites before installing.

Follow the step 1-3 to install RAVE & it’s Python interpreter

If you have installed RAVE before, please check How to update RAVE.

(Please always use the website for most up-to-date instructions. I simply copy-paste the R command for demo use)

1. Installs a manager package that helps you

install.packages('ravemanager', repos = '<https://rave-ieeg.r-universe.dev'>)
ravemanager::install()
ravemanager::configure\_python(python\_ver = "auto")
Just in case, restart R to take everything into effect after installation/upgrade.

2. Create your First RAVE Subject
Go to your Home directory. In my case, it’s /Users/dipterix , you will see rave\_data folder

Go to rave\_data -> raw\_dir , create a subject folder using subject code (e.g. SuthanaDemo )

Launch RAVE using

rave::start\_rave2()
In the RAVE app, go to Import Signals > Native Structure

Create a project name based on your objectives (e.g. electrodeloc )

Choose the subject you have just created

Click on Create Subject button

Now you have a new RAVE subject SuthanaDemo created under project electrodeloc for electrode localization purpose-only.

3. Imaging Pre-processing
Upload & import imaging files
In RAVE app, go to Surface & Electrodes > Reconstruction & Co-registration module,

Choose the project electrodeloc and subject SuthanaDemo

Choose proper pre-surgery MRI and post-implant CT

If this is the first time, click on dropdown menu and select [Upload] to upload imaging files accordingly
Click on Check data and command-line tools .

It’s OK to leave command-line tools blank and ignore the warnings. They are only needed for advanced features
In the pop-up modal, click Proceed

Click and expand panel Import DICOM Folders or Nifti Images (only need to run this step once)

Click on Run from RAVE (T1 MRI) to instruct RAVE to use the uploaded MRI files

Then click Run from RAVE (CT) to let RAVE use the uploaded CT files

Set up surface reconstruction (even if surface is not needed)
Expand panel Surface Reconstruction

Choose MRI file from dropdown menu. If you cannot find any choices, click on Refresh button

Choose command simple-import for direct import (no surface reconstruction)

If you would like to reconstruct surface models, please check the supp materials in the end
Click Run from RAVE if you choose simple-import

CT to MRI co-registration
Expand panel Co-registrate CT to T1

Choose CT file from dropdown menu. If you cannot find any choices, click on Refresh button

Choose a proper MR image from the dropdown menu

Choose ANTs or NiftyReg (whichever you prefer, personally I recommend ANTs), click on Run from RAVE

You may choose FSL , since FSL is very big, RAVE rely on you to install it separately. Also make sure you link the FSLDIR and use Save & run by yourself to generate terminal scripts.

If you use ANTs or NiftyReg , it usually takes around 1~3 min to finish the co-registration

4. Electrode Localization
Go to Surface & Electrodes > Electrode Localization , again, select proper project and subject code.

The Localization method should be filled in automatically (assuming you use RAVE for co-registration)

If you see blank values in dropdowns, please click on Refresh file list to let RAVE rescan files
Make Electrode Plan
Electrode planning allows you to localize groups of contacts independently, or using different configurations (e.g. surface vs. depth). Enter the groups in the same order as the channel order (your data acquisition jackbox configuration).

In this demo, we have two groups, each contains 4 contacts. To create the first group,

Group label: G1

Dimension: 4

Type: sEEG for depth or ECoG for surface, or iEEG if undetermined

Hemisphere: auto if undetermined (RAVE should be able to figure it out in the most of cases)

Click on + button to add the second group, enter the group information following the same instructions

Click on Load Subject once finished

Register electrodes
The localization viewer consists of two parts:

Left: electrode group & coordinate table (simplified preview)

Right: 3D viewer

Gray MRI slices

Green CT voxels (you can dynamically set threshold)

To register electrodes,

Click a group button (e.g. G1.4.iEEG[1-4] ) from the left panel

A subset of electrode table for this group will be displayed
In the 3D viewer, turn off controller (3D Viewer Control Panel > Electrode Localization > Auto Refine) if it’s checked. (it’s experimental and may result in unexpected behavior)

Click on green voxel blobs that represent electrode contacts. The contact locations will be calculated and orange spheres representing the contacts will be generated in the viewer

Save electrode file
Click on Stage & Show Electrode Table at the bottom-right of the app

In the pop-up modal dialogue, check that all electrodes are registered

Click on Save to subject button

The exported electrode table will be displayed in ~/rave\_data/data\_dir/electrodeloc/SuthanaDemo/rave/meta/electrodes.csv . (Replace electrodeloc/SuthanaDemo with your actual project and subject code)

5. Preview the localization results
In RAVE app, click on Subject 3D Viewer module,

Choose proper subject code. The electrode table should be displayed on the right panel

If you don’t see the table or if an error is thrown, please specify a project name
Click on Load Subject button to view the brain with electrodes in 3D

If you have analysis results, you can upload the result table to show the statistics/classifications on brain.

* Some extending topics may have not been covered in the demo session

Reconstruct surface models
If you want to create surface models in step 3 -> Set up surface reconstruction , RAVE provides two approaches that work for different scenarios:

Scenario 1: MRI has low-resolution (e.g. 22 sagittal slices)

You will need

FreeSurfer >= 7.4.1 (as of Jun 25, 2023, this is latest version). Old versions have bugs
A x86 CPU (ARM such as M1/M2 mac won’t work)
An operating system that allows you to run bash commands, e.g.
OSX (Intel chip only), Linux

Windows subsystem for linux

Scenario 2: High-res MRI (e.g. 256x256x189 resolution)

You will need

FreeSurfer (can be old versions like 6.x)
An operating system that allows you to run bash commands, e.g.
OSX (both Intel chip and ARM chip), Linux

Windows subsystem for linux

During the “Set up surface reconstruction” step, do this:

Expand panel Surface Reconstruction

Choose MRI file from dropdown menu. If you cannot find any choices, click on Refresh button

Choose proper commands

for scenario 1, choose recon-all-clinical.sh

for scenario 2, choose recon-all -all

Open a shell terminal on your machine

Go back to RAVE, click Save & run by yourself button, the corresponding script will be generated and a notification will pop up

Click on the command from the notification, the command will be copied to your clipboard automatically

Go back to shell terminal, paste the command and run

The whole process may take hours to run. Please wait patiently.

Adjust electrodes
If you would like to fine-tune the electrode locations, RAVE provides 2 manual approaches and 1 experimental auto-adjustment.

Method 1: Use anatomical slices
Go to viewer control center, expand Volume Settings , make sure Show Panels is checked.
You will see slices displaying coronal, axial, and sagittal planes
In the left table, click on the electrode that is to be adjusted,
you will see text “To re-localize this electrode, click here”, click word “here” to start tuning
Find the electrode contact you want to tune in 3D viewer, right-click in 3D viewer, the 2D slice will be centered at this contact
Click on 2D slice images to center the crosshair at the new location. The CT density value of the crosshair will be displayed on 2D slice viewers
In the viewer control center, Electrode Localization , click on Register from Crosshair , the new position will be registered
Repeat 2-6 until all contacts are adjusted
Method 2: Use keyboard shortcuts
Go to viewer control center, expand Electrode Localization , make sure Edit Mode is refine.
Go to 3D viewer, double click on the contact to modify, the electrode contact will be highlighted in red color
Use keyboard shortcut:
1 moves contact to the right, shift+1 moves to the left

2 moves contact to the anterior, shift+2 moves to the posterior

3 moves contact to the superior, shift+3 moves to the inferior

Repeat 2-3 until all contacts are adjusted
Method 3: Auto-adjust (TBA)
This feature is experimental now (This part is to be added).
