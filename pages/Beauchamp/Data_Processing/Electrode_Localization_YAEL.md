---
layout: default
title: Electrode Localization in YAEL
date_created: 2026-07-15
parent: Data Processing and Analysis
grand_parent: Beauchamp
---
## Imaging Preprocessing

_Date created: 2026-07-15_

1. Open RAVE_2.0:
	- Check [RAVE Wiki](https://rave.wiki/posts/installation/installation.html) if you haven't installed RAVE
	- Copy: `rave::start_rave2()` into RStudio
2. On the left sidebar, click “MRI/CT Processing”
	- Select Project (`automated` for Penn subjects) and Subject and confirm MRI file
		-If this is the first time, choose Subject option: `[New Subject]`, and in the pop-up modal dialogue, enter the subject code
	- Click `Check data and command-line tools` and then `Proceed`
3. Select “Import DICOM Folders or Nifti Images”
	- Run from RAVE (T1 MRI)
4. Select “ACPC Re-alignment”
	- Click on “refresh”button if the filename is missing
	- Select the proper MRI NIfTI file, click on “start re-alignment” (it will take ~10s to load)
		- You will see T1 in 3D and a folder called “ACPC realign” to the right (in the 3D control panel)
	- Click on “Click to register AC” button
		- Navigate the anatomical side panels, focus the crosshairs to AC
		- Click on `Confirm Updating AC`
	- Click on “Click to register PC” button
		- Navigate the anatomical side panels, focus the crosshairs to PC
		- Click on `Confirm Updating PC`
	- Click to set rotation
		- Rotate the brain, in the meanwhile, look at the coronal slices
		- Make sure the vertical green line splits the brain in half
		- Click on `confirm updating rotation`
	- If everything is correct, you should be able to see a matrix ”ScannerRAS to ACPC transform:”
	- Click on Save ACPC alignment results in the bottom
5. Click MRI Preprocessing on left hand side
	- Click Refresh
	- Select the proper MRI NIfTI file
		- If you cannot see any file, click on `refresh` link
		- IMPORTANT: if you did ACPC realignment, please choose `MRI_acpc.nii.gz` and always use this image rather than the original one because the image orientation has changed
	- For Command, choose `YAEL+recon-all`
	- Save and run by yourself
		-Copy to terminal
6. (Do this after recon-all: coregistration not needed) for quality control, do the followings. Let Zhengjia know if you find any inconsistency (Do not hesitate).
	- Go back to `MRI/CT Preprocessing` module, load the subject
		- Click on `Generate Reports` from the bottom right group buttons, next to the subject code
		- In the pop up modal, only choose “Normalization quality report”
		- Generate the report: it will take around 1min. RAVE will show notification once it’s done, then click on “View report” (green button from the notification)
		- Make sure you check all the views (axial, sagittal, coronal) and all the templates (MNI152 a/b/c). You should check if the brain matches with the template, focus on the following areas:
			1. Ventricle, cingulate, putamen, … (deep structure)
			2. STG/STS, insula, hippocampus, visual cortex
		- You can save the report, or copy the report from the following path and include in the final EMU folder `rave_data/data_dir/automated/<subject_code>/reports/report-normalization_datetime-<xxxx>_yael_preprocess/report.html
	- Make rave_slices.nii.gz from the following steps
		- Go to /Volumes/RAVE/rave_data/raw_dir/<subject_code>/ rave-imaging/fs/mri/, and remove rave_slices.nii.gz
		- Copy the image from the following path `/Volumes/RAVE/rave_data/raw_dir/<subject_code>/rave-imaging/inputs/anat/sub-<subject_code>_ses-preop_desc-preproc_T1w.nii.gz` to `rave-imaging/fs/mri/` 
		- Rename the copied file from the previous sub-step (ii) to “rave_slices.nii.gz”
	- Go to RAVE GUI, launch “Subject 3D viewer” module, load the brain. For quality control, toggle on "Side Panels" (Keyboard shortcut `p`) from the control panel, slide through the slices and check whether the brain matches with the volume images.
		- Also check brainmask by opening up the side control panel -> volume settings -> slice Mask. Default value is 0, change to 1. This step is to check if the brainmask is correct'
7. Click Coregistration CT and T1
	- Select MRI_acpc.nii.gz
8. Once you finish everything (YAEL+recon-all and coregistration), click on “Generate Reports”
	- in the popup modal, make sure all proper reports are selected
	  > EDIT: Since you have already generated normalization report, you only need one – coregistration report. However, if you forgot to create normalization report, this is a good time to include it too}
	- Confirm generating report (this will take ~ 5min)
	- Once the reports are generated, open them up (if there are multiple reports, open separately), save them to your final folder for sharing
		-If you accidentally closed the RAVE tab, go to `rave_data/data_dir/automated/<subject>/reports` to find the report folder, copy the report.html out and rename
9. For quality control, please check the coregistration report, make sure the CT (Red) aligns with the MRI (gray) in all slices and all views (axial sagittal coronal). Again, let Zhengjia know if there is any issues


## Localize Electrodes

1. Open RAVE 2.0:
2. On the left sidebar, click “Electrode Localization”
	- Choose “automated” project, and desired subject code
3. Locate subject’s surgical plan with electrode map as well as montage of electrodes
4. Indicate group label for each electrode shaft, dimension (8 or 12). Enter the group surgical label for each shaft, number of electrodes, for type, enter the electrode product name instead of iEEG, such as `AdTECH- RD12R-SP05X-000`. Set hemisphere to “`auto`” because it will save your time
	- Double-check the plan, especially the number of shafts and number of contacts. If you need to correct it later, you will need to re-localize.
5. Load subject
6. Click on group label (ex. `RQ.12.sEEG[1-12]`) on left side
7. Since we entered the electrode product name in step 4, here you localize the inner-most electrode, then click on anywhere along the shaft, then click on “`interpolate`” button from Electrode Localization controller panel.
	- Use settings on side for better visualization:
		- Under Default: change background color
		- Under Volume Settings: change opacity of voxels with slider bar
8. Repeat 6 and 7 until all the electrodes are localized
	- If you are worried about losing the localization, click on “`stage & show electrode table`” button at the bottom-right of the screen after localizing each shaft. This will temporarily save your results, then click on “Dismiss” button in the pop-up (don’t save to subject). And YAEL will restart from this saved copy if you accidentally quit RAVE
9. Once all the electrodes are localized, click on “`stage & show electrode table`” button at the bottom-right of the screen, and check
	1. All the electrode contacts have coordinates
	2. Check Freesurfer labels for each shaft, especially the first 5 contacts: typically they should not be unknown
	3. If 1) and 2) passes, check all the post-process options
	4. Press “`Save to Subject`” to save the electrodes.csv – it might take 2-5 min to calculate all the results and generate an electrode anatomical slice report (save the report because you will need to send it to everyone)
10. Go to “Subject 3D viewer” module, load this subject again,
	1. make sure you hit “re-generate the viewer ->” link to load surgical labels to the viewer
	2. Copy the following string into the control panel “Default -> Paste to set State”
	3. Click “re-generate the viewer ->” link again to burn the controller state into the viewer
	4. Download the viewer for sharing

```json
{
  "isThreeBrainControllerData": true,
  "controllerData": {
    "controllers": {},
    "folders": {
      "Default": {
        "controllers": {
          "Background Color": "#000000"
        },
        "folders": {}
      },
      "Volume Settings": {
        "controllers": {
          "Show Panels": true,
          "Crosshair Gap": 2,
          "Coronal (P - A)": 22.4,
          "Overlay Coronal": true
        },
        "folders": {}
      },
      "Surface Settings": {
        "controllers": {
          "Left Hemisphere": "mesh clipping x 0.3",
          "Right Hemisphere": "mesh clipping x 0.3",
          "Left Opacity": 0.1,
          "Right Opacity": 0.1,
          "Left Mesh Clipping": 0.3,
          "Right Mesh Clipping": 0.3
        },
        "folders": {}
      },
      "Electrode Settings": {
        "controllers": {
          "Visibility": "all visible",
          "Electrode Shape": "contact-only",
          "Outlines": "on",
          "Text Scale": 3.8,
          "Electrode Text": "label_prefix"
        },
        "folders": {}
      },
      "Data Visualization": {
        "controllers": {
          "Display Data": "LabelPrefix",
          "Show Legend": true,
          "Show Time": false,
          "Highlight Box": true,
          "Info Text": true
        },
        "folders": {}
      }
    }
  },
  "cameraState": {
    "up": {
      "x": 0,
      "y": 0,
      "z": 1
    },
    "position": {
      "x": 0,
      "y": -500,
      "z": 0
    }
  }
}
```
