> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# LocalizeElectrodes

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/LocalizeElectrodes/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

### Localizing electrodes in RAVE

**1. Complete, step-by-step guide (with screenshots), created by Aayushi Sangani and Zhengjia Wang.** Will eventually be copied to wiki as individual steps. Note: contains some steps that are specific to the clinical workflow at UPenn; modify to suit your institution.

```
Click here to download PDF
```

2. Less complete text guide without screenshots:
First, click on "Surface & Electrodes" tab which reveals two options: "Reconstruction & Coregistration" and "Electrode Localization."
"Reconstruction & Coregistration" calls AFNI or FSL to register the pre-operative MRI with the post-operative CT; and calls FreeSurfer to transform the MRI into standard space and (optionally) create a cortical surface model.

If you have already done these steps, you do not need to redo them; just move the resultant files into the correct location in the RAVE directory tree. If you do the steps within RAVE, RAVE will place the output files in the correct directory automatically.

```
 https://github.com/dipterix/threeBrain/issues/22
```

Next, click on "Electrode Localization". This module has two screens: "Stage & Show Electrode Table" for defining electrode groups and "Localizing [SubjectName] with CT" for localizing the electrodes within each group. The default first screen is "Stage & Show Electrode Table."
Select the correct Project and Subject using the pull-down menus. Then, select the aligned CT, e.g.

```
 CT_RAI_res_al.nii
```

Next, create Electrode Plans. A separate electrode plan is created for a different group of electrodes: usually one shaft for sEEG, or one grid or strip for ECoG. Using the OR worksheet (e.g. "JackSheetMaster.csv", enter multiple plans with the correct number of electrodes and the appropriate label (e.g. "PST" with 4 contact).
Click

```
 Load subject
```

in the bottom right of the screen or

```
 Load Data
```

in the top of the screen. This will take you to the other screen, "Localizing [SubjectName] with CT"
Click

```
 Stage & Show Electrode Table
```

to go back to the Electrode Planning screen.
Next, go to the interactive 3D viewer. Make sure "Edit Mode" is set to

```
 CT/volume
```

For ECoG electrodes, click on the first and last electrodes in the strip, or in a row or column of electrodes in a grid.
Then, click

```
 Interpolate from Recently Added.
```

RAVE will guess the approximate locations of the electrodes in the row or column. RAVE will try to guess how many electrodes to interpolate, based on the electrode plan. Manually override by entering a value in the "interpolate" text box".
Repeat for the remaining rows or columns.
The next step is to refine the electrode locations. Change "Edit mode" to

```
 Refine
```

1/Shift 1: move electrode Right or Left

There are two different co-ordinate spaces:

```
 T1RAS
```

is the native coordinates of the MRI of this particular participant.

```
 tkrRAS
```

is the FreeSurfer normalized coordinate for this participant.

```
 MNI305, MNI152
```

Are the FreeSurfer estimates for these MNI standard spaces.
The CT is aligned to the tkrRAS so that everything is in FreeSurfer space.

When you are finished, click

```
 Stage & Show Electrode Table
```

then click

```
 Save to subject
```

This saves the file

```
 electrodes.csv
```

In the specified directory, e.g.

```
 data_dir/NIH_070/NIH_070/rave/meta/electrodes.csv
```

### Electrodes.CSV

RAVE uses the file **electrodes.csv** to store information about each electrode, one row per electrode. Because electrode locations are different in every subject, each subject has a different electrodes.csv file, located in the directory tree

```
 proj_name/subj_name/rave/meta/electrodes.csv
```

Here is the contents of a sample electrodes.csv file:

```
   Electrode   Coord_x     Coord_y   Coord_z    Label
       13      -68.86721   7.1108970 15.57871   G13
       14      -70.83457  -0.7146498 17.87189   G14
       15      -71.80737  -9.9609583 22.41152   G15
```

There are five required columns in each electrodes.csv file. The first column must be labelled "Electrode" and lists a unique number for each electrode (typically, the clinical channel number used to record data from that electrode). The second column must be labelled "Coord\_x" and contains the x-coordinate of the electrode in the tk-RAS (FreeSurfer) coordinate system. The third column and fourth columns are the y and z co-ordinates. The fifth column must be called "Label" and contains the name of electrode. Additional columns may also be present in the file. For instance, the cortical surface vertex closest to the electrode; the anatomical location of the electrode; and so on. If there are additional columns, RAVE will read them and allow you to filter electrodes accordingly (e.g. "only electrodes with label = superior temporal").

### Automatic Label Generation

RAVE provides tools to generate additional electrode labels automatically if FreeSurfer or SUMA files are provided. The following script calculates MNI305 coordinates and nearest hemisphere etc. Simply replace `project\_name` and `subject\_code` before executing.

```
project_name <- "demo"
subject_code <- "YAB"
brain <- rave::rave_brain2(sprintf('%s/%s', project_name, subject_code))
brain$electrodes$raw_table$SurfaceElectrode <- TRUE
tbl <- brain$calculate_template_coordinates()
rave::save_meta(data = tbl, meta_type = 'electrodes', project_name, subject_code)
```

The fully expanded electrodes.csv with optional columns looks like this.

```
Electrode   Coord_x     Coord_y  Coord_z    Label  MNI305_x  MNI305_y  MNI305_z SurfaceElectrode      SurfaceType Radius VertexNumber Hemisphere
13         -68.86721   7.1108970 15.57871   G13    -75.58190 -11.96114 -7.205155 TRUE                  pial         2       139280       left
14         -70.83457  -0.7146498 17.87189   G14    -77.13832 -21.71118 -2.563521 TRUE                  pial         2       144135       left
15         -71.80737  -9.9609583 22.41152   G15    -77.52183 -33.03184  5.295971 TRUE                  pial         2       144936       left
```

Columns MNI305\_x, MNI305\_y, MNI305\_z are MNI305 coordinates. Column SurfaceElectrode is logical TRUE/FALSE indicating whether the electrode is grid electrode floating on the surface (TRUE) or depth electrode inserted (FALSE). Column SurfaceType is for surface electrodes only, indicating the nearest surface structure. Column Radius will affect electrode render sizes. Column Hemisphere is the nearest hemisphere (left/right). If SUMA standard 141 brain is used, column VertexNumber will be the vertex number of corresponding hemisphere that is closest to the electrode. If SUMA standard 141 brain is missing, or the electrode is marked as depth electrode, VertexNumber will be -1.

### Other Links

1. [Karas Lab at UTMB tutorial on electrode localization.](../Karas_Lab/RAVE_Electrode_Localization.md "Karas Lab:RAVE Electrode Localization")
2. <https://github.com/dipterix/threeBrain/issues/22>
3. [Older information on imaging data](vignettes_electrode-localization.md "RAVE:vignettes:electrode-localization")
4. [Beauchamp:Electrode Localization and Naming](../Beauchamp/Electrode_Localization_and_Naming.md "Beauchamp:Electrode Localization and Naming")
5. [Creating a Surface Model and Electrode Localization (by Muge Ozker Sertel)](../Beauchamp/Creating_a_Surface_Model_and_Electrode_Localization_(by_Muge_Ozker_Sertel).md "Beauchamp:Creating a Surface Model and Electrode Localization (by Muge Ozker Sertel)")
6. [Electrode Localization using iELVis (by Buffy Nesbitt)](../Beauchamp/BuffyElectrodeNotes.md "Beauchamp:BuffyElectrodeNotes")
7. [Electrode Localization using steps from the ALICE package](../Beauchamp/ALICE.md "Beauchamp:ALICE")
8. [Electrode Localization using steps from the img\_pipe package](../Beauchamp/img_pipe.md "Beauchamp:img pipe")
9. [Overview of imaging data and electrode localization](vignettes_electrode-localization.md "RAVE:vignettes:electrode-localization")
10. [Import volumetric MRI data and cortical surface models](Imaging_Data_Formats.md "RAVE:Imaging Data Formats")

---

*[Return to preprocessing overview](ravepreprocess.md "RAVE:ravepreprocess")*
